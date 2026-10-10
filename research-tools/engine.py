#!/usr/bin/env python3
"""Run a checker on an engine that did not produce the work.

`routes.yaml` defers every loop route's `checker` to run time, because all three
CLIs read the same SKILL.md and any of them may be the one running. This resolves
it: given the engine that is running, it picks one that is not.

    make engines                     every declared engine answers, or says why
    python3 research-tools/engine.py --running claude --prompt-file p.txt --schema s.json

**The running engine is stated, never sniffed.** codex launched from inside
Claude Code inherits `CLAUDECODE` and `CLAUDE_CODE_*`, so a nested run reads as
its parent and any env heuristic silently mis-identifies it — which would hand
back a verdict from the very engine that was supposed to be excluded. `--running`
is required, and absent it this stops.

**A checker that did not run is not a checker that passed.** Every failure path
here raises. Nothing returns a default verdict, nothing degrades to "assume
fine": an engine missing from PATH, an engine that starts and produces no
parseable object, a response that does not match the schema — each is an error
with the engine's own words attached, because the alternative is a green run
that verified nothing (DESIGN §5.4b).

Engine quirks, re-checked by `make engines` rather than dated:

* `codex exec` rejects a schema without `additionalProperties: false`, at every
  level. Schemas are normalised here so callers write ordinary JSON Schema.
* `agy --print` returns an envelope; the validated object is `structured_output`.
* `claude -p --json-schema` returns an envelope; the validated object is
  `structured_output`, the same field name `agy` uses.
* The prompt reaches codex and claude on stdin, not argv: a long one overruns
  the argument limit, and one starting with `-` reads as a flag. agy takes it as
  `--print=<prompt>`, which no prompt text can turn into another option.

Whatever an engine returns is held to the schema here — an object, required
keys present, declared types right — before anyone reads a field of it. A shape
the caller did not ask for is the engine not answering, never a verdict with a
hole in it.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import signal
import subprocess
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
H = yaml.safe_load((ROOT / "research-registry" / "harness.yaml").read_text(encoding="utf-8"))
ENGINES = H.get("engines") or {}
TIMEOUT = 600


class EngineError(RuntimeError):
    """The engine did not answer. Never a verdict."""


def strict(schema: dict) -> dict:
    """Every object closed, which is what codex requires and agy tolerates."""
    if not isinstance(schema, dict):
        return schema
    out = {k: strict(v) if isinstance(v, dict) else v for k, v in schema.items()}
    if out.get("type") == "object":
        out["additionalProperties"] = False
        out["properties"] = {k: strict(v) for k, v in (out.get("properties") or {}).items()}
    if isinstance(out.get("items"), dict):
        out["items"] = strict(out["items"])
    return out


def run(engine: str, prompt: str, schema: dict) -> dict:
    """Ask `engine` for one object matching `schema`. Raises rather than guessing."""
    known = ENGINES.get("runs_on") or []
    if engine not in known:
        raise EngineError(f"{engine} is not one of {known}")

    with tempfile.TemporaryDirectory(prefix="research-engine-") as tmp:
        d = pathlib.Path(tmp)
        s = d / "schema.json"
        s.write_text(json.dumps(strict(schema)), encoding="utf-8")
        if engine == "codex":
            out = d / "answer.json"
            # `-` reads the instructions from stdin.
            argv = ["codex", "exec", "--output-schema", str(s), "-o", str(out),
                    "--sandbox", "read-only", "--skip-git-repo-check", "-"]
            r = _spawn(engine, argv, stdin=prompt)
            body = out.read_text(encoding="utf-8") if out.exists() else ""
            if not body.strip():
                raise EngineError(f"codex wrote no answer.\n{_tail(r)}")
            return conform(engine, _parse(engine, body), schema)
        if engine == "claude":
            # No positional prompt: `-p` reads it from stdin.
            argv = ["claude", "-p", "--output-format", "json",
                    "--json-schema", json.dumps(schema)]
            r = _spawn(engine, argv, stdin=prompt)
            envelope = _parse(engine, r.stdout)
            got = envelope.get("structured_output")
            if not isinstance(got, dict):
                raise EngineError(f"claude returned no structured_output.\n{_tail(r)}")
            return conform(engine, got, schema)
        if engine == "agy":
            argv = ["agy", f"--print={prompt}", "--output-format", "json",
                    "--json-schema", str(s)]
            r = _spawn(engine, argv)
            envelope = _parse(engine, r.stdout)
            got = envelope.get("structured_output")
            if not isinstance(got, dict):
                raise EngineError(f"agy returned no structured_output object "
                                  f"(status {envelope.get('status')!r}).\n{_tail(r)}")
            return conform(engine, got, schema)
    raise EngineError(f"no invocation is known for {engine}")


# JSON Schema `type` -> what json.loads produces for it. bool is an int to
# Python, so a boolean where a number was asked for is refused explicitly.
TYPES = {"boolean": bool, "string": str, "array": list, "object": dict,
         "integer": int, "number": (int, float), "null": type(None)}


def conform(engine: str, got, schema: dict, at: str = "answer"):
    """`got` if it has the shape `schema` asks for, else EngineError.

    Required keys and declared types, recursively — not the whole of JSON
    Schema, but enough that a caller can read a field without a KeyError.
    """
    want = schema.get("type")
    py = TYPES.get(want) if isinstance(want, str) else None
    if py is not None:
        if not isinstance(got, py) or (isinstance(got, bool) and want in ("integer", "number")):
            raise EngineError(f"{engine}: {at} is {type(got).__name__}, the schema says {want}")
    if isinstance(got, dict):
        missing = [k for k in schema.get("required") or [] if k not in got]
        if missing:
            raise EngineError(f"{engine}: {at} lacks required {missing}")
        for k, sub in (schema.get("properties") or {}).items():
            if k in got and isinstance(sub, dict):
                conform(engine, got[k], sub, f"{at}.{k}")
    if isinstance(got, list) and isinstance(schema.get("items"), dict):
        for i, item in enumerate(got):
            conform(engine, item, schema["items"], f"{at}[{i}]")
    return got


def _spawn(engine: str, argv: list[str], stdin: str | None = None) -> subprocess.CompletedProcess:
    """Run in a session of its own, so a timeout kills whatever it started too."""
    try:
        p = subprocess.Popen(argv, text=True, start_new_session=True,
                             stdin=subprocess.DEVNULL if stdin is None else subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise EngineError(f"{engine} is not on PATH") from None
    except OSError as e:                   # E2BIG, EACCES, ...: it never started
        raise EngineError(f"{engine} could not be started: {e}") from None
    try:
        out, err = p.communicate(stdin, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except OSError:
            pass
        p.communicate()
        raise EngineError(f"{engine} did not answer within {TIMEOUT}s") from None
    return subprocess.CompletedProcess(argv, p.returncode, out, err)


def _parse(engine: str, body: str) -> dict:
    stripped = body.strip()
    try:
        got = json.loads(stripped)
        if isinstance(got, dict):
            return got
    except ValueError:
        pass
    for line in reversed(stripped.splitlines()):
        try:
            got = json.loads(line)
        except ValueError:
            continue
        if isinstance(got, dict):
            return got
    raise EngineError(f"{engine} printed nothing that parses as an object:\n{body[:400]}")


def _tail(r: subprocess.CompletedProcess) -> str:
    return "\n".join((r.stderr or r.stdout or "").strip().splitlines()[-6:])


def other_than(running: str) -> str:
    """An engine that is not the one running. Raises rather than falling back."""
    known = ENGINES.get("runs_on") or []
    if running not in known:
        raise EngineError(f"the running engine {running!r} is not one of {known}; "
                          "state it correctly rather than letting this guess")
    for candidate in known:
        if candidate != running:
            return candidate
    raise EngineError(f"{known} leaves nothing to check {running} with")


SELFTEST = {"type": "object", "properties": {"ok": {"type": "boolean"}},
            "required": ["ok"]}


def selftest() -> int:
    """Ask each declared engine for one object. Reachability, not correctness."""
    bad = 0
    for engine in ENGINES.get("runs_on") or []:
        try:
            got = run(engine, "Reply with ok=true and nothing else.", SELFTEST)
        except EngineError as e:
            print(f"  {engine}: UNAVAILABLE — {e}")
            bad += 1
            continue
        print(f"  {engine}: answered {got}")
    known = ENGINES.get("runs_on") or []
    print(f"engines reachable: {len(known) - bad}/{len(known)} of {known}   "
          f"any of them may be the one running")
    # Unreachable is reported, never fatal: a machine without one of these still
    # runs every other check, and a hook that fails on a missing CLI gets removed.
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("engine", nargs="?", help="the checker; omit to resolve from --running")
    ap.add_argument("--running", help="the engine running this harness — required, never guessed")
    ap.add_argument("--prompt-file")
    ap.add_argument("--schema")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.running:
        # A bare run used to fall through to the selftest, which is a paid call
        # to every engine. That is what --selftest is for; this says how to ask.
        ap.print_usage(sys.stderr)
        print("--running is required (or --selftest)", file=sys.stderr)
        return 2
    if not (a.prompt_file and a.schema):
        print("need --prompt-file and --schema", file=sys.stderr)
        return 2
    try:
        engine = a.engine or other_than(a.running)
        if a.running and engine == a.running:
            raise EngineError(f"{engine} is the engine running this; "
                              "a verdict from it is not a check")
        got = run(engine,
                  pathlib.Path(a.prompt_file).read_text(encoding="utf-8"),
                  json.loads(pathlib.Path(a.schema).read_text(encoding="utf-8")))
    except EngineError as e:
        print(f"{a.engine or 'checker'}: {e}", file=sys.stderr)
        return 1
    print(json.dumps(got, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
