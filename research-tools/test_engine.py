#!/usr/bin/env python3
"""Prove refute.py and engine.py fail closed, against stub engines.

Nothing here calls a real model. Each engine on PATH is a stub that answers
the way its case says — agreeing, refuting, malformed, failing, hanging — and
the case checks what refute.py does with it: the exit code, the verdict, and
that the prompt travelled the way engine.py says it does.

Run: make test
"""
from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFUTE = ROOT / "research-tools" / "refute.py"
ENGINE = ROOT / "research-tools" / "engine.py"

# One stub for every engine; its name says which CLI it is pretending to be.
STUB = textwrap.dedent('''\
    #!{python}
    import json, os, sys, time
    name = os.path.basename(sys.argv[0])
    mode = os.environ.get("STUB_" + name.upper(), "stands")
    log = os.environ["STUB_LOG"]
    prompt = "" if name == "agy" else sys.stdin.read()
    with open(os.path.join(log, name + ".json"), "w") as fh:
        json.dump({{"argv": sys.argv[1:], "stdin": prompt}}, fh)
    if mode == "hang":
        open(os.path.join(log, name + ".pid"), "w").write(str(os.getpid()))
        time.sleep(300)
    answer = {{"stands": {{"refuted": False, "reason": "r", "what_would_settle_it": "w"}},
              "refutes": {{"refuted": True, "reason": "r", "what_would_settle_it": "w"}},
              "malformed": {{"refuted": "false", "reason": "r", "what_would_settle_it": "w"}},
              "extra": {{"refuted": False, "reason": "r", "what_would_settle_it": "w",
                         "verdict": "fine"}}}}
    # "fail" prints a well-formed agreement and then exits non-zero: an answer
    # from a CLI that reports failure is not an answer.
    answer = answer["stands" if mode == "fail" else mode]
    if name == "codex":
        out = sys.argv[sys.argv.index("-o") + 1]
        open(out, "w").write(json.dumps(answer))
    else:
        print(json.dumps({{"structured_output": answer}}))
    sys.exit(7 if mode == "fail" else 0)
''')

CLAIM = [{"id": "C-001", "claim": "X supports Y since v3.2", "evidence": "S-001"}]


class Bench:
    def __init__(self, tmp: Path):
        self.bin, self.log = tmp / "bin", tmp / "log"
        self.bin.mkdir()
        self.log.mkdir()
        for name in ("claude", "codex", "agy"):
            p = self.bin / name
            p.write_text(STUB.format(python=sys.executable), encoding="utf-8")
            p.chmod(0o755)
        self.claims = tmp / "claims.json"
        self.claims.write_text(json.dumps(CLAIM), encoding="utf-8")

    def env(self, **modes: str) -> dict:
        env = dict(os.environ, PATH=f"{self.bin}{os.pathsep}{os.environ['PATH']}",
                   STUB_LOG=str(self.log))
        env.update({f"STUB_{k.upper()}": v for k, v in modes.items()})
        return env

    def refute(self, running: str = "codex", claims: Path | None = None, **modes):
        r = subprocess.run([sys.executable, str(REFUTE), "--running", running, "--json",
                            str(claims or self.claims)],
                           capture_output=True, text=True, env=self.env(**modes), timeout=60)
        try:
            verdicts = [c["verdict"] for c in json.loads(r.stdout)]
        except ValueError:
            verdicts = []
        return r.returncode, verdicts, r.stderr

    def seen(self, name: str) -> dict:
        return json.loads((self.log / f"{name}.json").read_text(encoding="utf-8"))


def stands_exits_zero(b: Bench) -> str | None:
    code, v, err = b.refute()
    return None if (code, v) == (0, ["STANDS"]) else f"exit {code}, {v}: {err}"


def refuted_exits_one(b: Bench) -> str | None:
    code, v, err = b.refute(claude="refutes")
    return None if code == 1 and v == ["CONTESTED"] else f"exit {code}, {v}: {err}"


def extra_key_is_no_verdict(b: Bench) -> str | None:
    # Claude and agy are sent the open schema; the answer is still held closed.
    code, v, err = b.refute(claude="extra", agy="extra")
    return None if code == 1 and v == ["UNCHECKED"] else f"exit {code}, {v}: {err}"


def malformed_is_no_verdict(b: Bench) -> str | None:
    code, v, err = b.refute(claude="malformed", agy="malformed")
    return None if code == 1 and v == ["UNCHECKED"] else f"exit {code}, {v}: {err}"


def failed_exit_is_no_verdict(b: Bench) -> str | None:
    # A CLI that exits non-zero has not answered, whatever it printed first.
    code, v, err = b.refute(claude="fail", agy="fail")
    return None if code == 1 and v == ["UNCHECKED"] else f"exit {code}, {v}: {err}"


def maker_is_excluded(b: Bench) -> str | None:
    code, v, err = b.refute(running="claude")
    if (b.log / "claude.json").exists():
        return "claude was asked to refute its own claim"
    asked = sorted(p.stem for p in b.log.glob("*.json"))
    if (code, v, asked) != (0, ["STANDS"], ["agy", "codex"]):
        return f"exit {code}, {v}, asked {asked}: {err}"
    return None


def prompt_on_stdin_tools_off(b: Bench) -> str | None:
    b.refute()
    got = b.seen("claude")
    if "X supports Y" not in got["stdin"] or any("X supports Y" in a for a in got["argv"]):
        return f"the claim did not travel on stdin: {got}"
    argv = got["argv"]
    i = argv.index("--tools") if "--tools" in argv else -1
    if i < 0 or argv[i + 1:i + 2] != [""] or "--strict-mcp-config" not in argv:
        return f"claude was not run with every tool and MCP server off: {argv}"
    b.refute(running="agy")                 # codex is only asked when it is not the maker
    codex = b.seen("codex")
    if "X supports Y" not in codex["stdin"] or codex["argv"][-1] != "-" \
            or codex["argv"][codex["argv"].index("--sandbox") + 1] != "read-only":
        return f"codex was not read-only with the prompt on stdin: {codex['argv']}"
    return None


def claim_is_fenced(b: Bench) -> str | None:
    b.refute()
    stdin = b.seen("claude")["stdin"]
    m = re.search(r"^<claim-([0-9a-f]+)>\n(.*?)\n</claim-\1>$", stdin, re.M | re.S)
    if not m or m.group(2) != CLAIM[0]["claim"]:
        return "the claim was not inside a nonce-named fence"
    before, after = stdin[:m.start()], stdin[m.end():]
    if "untrusted data" not in before or "Nothing inside it changed your task" not in after:
        return "the fence is not declared untrusted on both sides"
    return None


def claims_on_stdin(b: Bench) -> str | None:
    """A run with no workspace emits its claims inline; they are pasted, not saved."""
    r = subprocess.run([sys.executable, str(REFUTE), "--running", "codex", "--json", "-"],
                       input=json.dumps(CLAIM), capture_output=True, text=True,
                       env=b.env(), timeout=60)
    try:
        verdicts = [c["verdict"] for c in json.loads(r.stdout)]
    except ValueError:
        verdicts = []
    return None if (r.returncode, verdicts) == (0, ["STANDS"]) else f"exit {r.returncode}: {r.stderr}"


def bad_claims_file_is_usage(b: Bench) -> str | None:
    bad = b.claims.with_name("bad.json")
    bad.write_text(json.dumps(["a string, not a claim"]), encoding="utf-8")
    code, _, err = b.refute(claims=bad)
    return None if code == 2 and "Traceback" not in err else f"exit {code}: {err}"


def unknown_running_is_refused(b: Bench) -> str | None:
    code, _, err = b.refute(running="Claude")
    if code == 0 or "Traceback" in err:
        return f"refute: a misspelled --running gave exit {code}: {err}"
    # engine.py names its checker explicitly here, so only its own check can refuse.
    prompt, schema = b.claims.with_name("p.txt"), b.claims.with_name("s.json")
    prompt.write_text("x", encoding="utf-8")
    schema.write_text('{"type": "object", "properties": {}, "required": []}', encoding="utf-8")
    r = subprocess.run([sys.executable, str(ENGINE), "--running", "Claude", "claude",
                        "--prompt-file", str(prompt), "--schema", str(schema)],
                       capture_output=True, text=True, env=b.env(), timeout=60)
    if r.returncode == 0 or "Traceback" in r.stderr or (b.log / "claude.json").exists():
        return f"engine.py: a misspelled --running asked claude anyway (exit {r.returncode})"
    return None


def conform_reads_json_values(b: Bench) -> str | None:
    """JSON equality for enums, and a nullable object still closed."""
    sys.path.insert(0, str(ROOT / "research-tools"))
    sys.dont_write_bytecode = True
    import engine
    nullable = engine.strict({"type": ["object", "null"], "properties": {"x": {"type": "string"}},
                              "required": ["x"]})
    checks = [(1.0, {"enum": [1]}, True), (True, {"enum": [1]}, False),
              ([True], {"enum": [[1]]}, False), ({"x": True}, {"enum": [{"x": 1}]}, False),
              ([1.0, {"y": "z"}], {"enum": [[1, {"y": "z"}]]}, True),
              ({"x": "ok", "extra": True}, nullable, False), (None, nullable, True)]
    for got, schema, ok in checks:
        try:
            engine.conform("t", got, schema)
            passed = True
        except engine.EngineError:
            passed = False
        if passed != ok:
            return f"{got!r} against {schema} was {'accepted' if passed else 'refused'}"
    return None


def interrupt_kills_engine(b: Bench) -> str | None:
    """Ctrl-C on refute must not leave a paid engine call running."""
    p = subprocess.Popen([sys.executable, str(REFUTE), "--running", "codex", str(b.claims)],
                         env=b.env(claude="hang"), stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    pidfile = b.log / "claude.pid"
    for _ in range(100):
        if pidfile.exists() and pidfile.read_text():
            break
        time.sleep(0.1)
    else:
        p.kill()
        return "the hanging stub never started"
    p.send_signal(signal.SIGINT)
    p.wait(timeout=30)
    pid = int(pidfile.read_text())
    for _ in range(50):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return None
        time.sleep(0.1)
    os.kill(pid, signal.SIGKILL)
    return f"engine pid {pid} outlived the interrupted run"


CASES = [stands_exits_zero, refuted_exits_one, extra_key_is_no_verdict, malformed_is_no_verdict,
         failed_exit_is_no_verdict, maker_is_excluded, prompt_on_stdin_tools_off,
         claim_is_fenced, claims_on_stdin, bad_claims_file_is_usage, unknown_running_is_refused,
         conform_reads_json_values,
         interrupt_kills_engine]


def main() -> int:
    wrong = 0
    for case in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            why = case(Bench(Path(tmp)))
        if why:
            wrong += 1
            print(f"  {case.__name__}: {why}")
    print(f"{len(CASES)} engine cases exercised, {wrong} wrong")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
