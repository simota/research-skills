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
that verified nothing.

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
import unicodedata

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
H = yaml.safe_load((ROOT / "research-registry" / "harness.yaml").read_text(encoding="utf-8"))
ENGINES = H.get("engines") or {}
TIMEOUT = 600


class EngineError(RuntimeError):
    """The engine did not answer. Never a verdict."""


def strict(schema: dict) -> dict:
    """Every object closed, which is what codex requires and agy tolerates.

    Codex's strict outputs also require every property to be required, so an
    optional one is refused here rather than by the engine mid-run. `anyOf`,
    `oneOf` and `$defs` are not normalised; no schema in this set uses them.
    """
    if not isinstance(schema, dict):
        return schema
    out = {k: strict(v) if isinstance(v, dict) else v for k, v in schema.items()}
    t = out.get("type")
    if t == "object" or (isinstance(t, list) and "object" in t):
        optional = sorted(set(out.get("properties") or {}) - set(out.get("required") or []))
        if optional:
            raise EngineError(f"schema leaves {optional} optional; strict outputs require all")
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

    # Checked once for every engine: in argv, os.fsencode would let a lone
    # \udcXX through as a raw byte, so agy answered on text nobody wrote.
    try:
        prompt.encode("utf-8")
    except UnicodeEncodeError as e:
        raise EngineError(f"the prompt is not UTF-8 text ({e.reason} at {e.start})") from None
    check_schema(schema)
    # Held to the closed form whatever the engine was sent: an extra key from
    # claude or agy is as much "not what was asked" as one from codex.
    closed = strict(schema)
    with tempfile.TemporaryDirectory(prefix="research-engine-") as tmp:
        d = pathlib.Path(tmp)
        s = d / "schema.json"
        s.write_text(json.dumps(closed), encoding="utf-8")
        if engine == "codex":
            out = d / "answer.json"
            # `-` reads the instructions from stdin.
            argv = ["codex", "exec", "--output-schema", str(s), "-o", str(out),
                    "--sandbox", "read-only", "--skip-git-repo-check", "-"]
            r = _spawn(engine, argv, stdin=prompt)
            try:
                body = out.read_text(encoding="utf-8") if out.exists() else ""
            except UnicodeDecodeError as e:
                raise EngineError(f"codex wrote an answer that is not UTF-8 ({e})") from None
            if not body.strip():
                raise EngineError(f"codex wrote no answer.\n{_tail(r)}")
            return conform(engine, _parse(engine, body), closed)
        if engine == "claude":
            # No positional prompt: `-p` reads it from stdin.
            # `--tools ""` disables every built-in tool and `--strict-mcp-config`
            # loads no MCP server: the prompt carries text under attack, and codex
            # gets `--sandbox read-only` for the same reason.
            argv = ["claude", "-p", "--output-format", "json",
                    "--json-schema", json.dumps(schema), "--strict-mcp-config",
                    "--tools", ""]
            r = _spawn(engine, argv, stdin=prompt)
            envelope = _parse(engine, r.stdout)
            got = envelope.get("structured_output")
            if not isinstance(got, dict):
                raise EngineError(f"claude returned no structured_output.\n{_tail(r)}")
            return conform(engine, got, closed)
        if engine == "agy":
            argv = ["agy", f"--print={prompt}", "--output-format", "json",
                    "--json-schema", str(s)]
            r = _spawn(engine, argv)
            envelope = _parse(engine, r.stdout)
            got = envelope.get("structured_output")
            if not isinstance(got, dict):
                raise EngineError(f"agy returned no structured_output object "
                                  f"(status {envelope.get('status')!r}).\n{_tail(r)}")
            return conform(engine, got, closed)
    raise EngineError(f"no invocation is known for {engine}")


# JSON Schema `type` -> what json.loads produces for it. bool is an int to
# Python, so a boolean where a number was asked for is refused explicitly.
TYPES = {"boolean": bool, "string": str, "array": list, "object": dict,
         "integer": int, "number": (int, float), "null": type(None)}


def _is(got, want: str) -> bool:
    py = TYPES.get(want)
    if py is None:
        return False                      # not a JSON type: nothing satisfies it
    if isinstance(got, bool):
        return want == "boolean"
    if want == "integer":
        return isinstance(got, int) or (isinstance(got, float) and got.is_integer())
    return isinstance(got, py)


def json_equal(a, b) -> bool:
    """Equality as JSON defines it, at every depth: `1.0` is the integer 1, but
    `true` is never 1 — which Python's `==` says it is, inside a list too."""
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(json_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(json_equal(a[k], b[k]) for k in a)
    return type(a) is type(b) and a == b


def check_schema(schema, at: str = "schema") -> None:
    """The keywords `strict` and `conform` read have the shapes they read them as.

    That is `type`, `enum`, `required`, `properties` and `items`;
    `additionalProperties` is not checked because `strict` overwrites it.

    Otherwise `{"type": 5}` reached `conform` only after the engine had been
    paid to answer, and ended there in a TypeError.
    """
    if not isinstance(schema, dict):
        raise EngineError(f"{at} is {type(schema).__name__}, not an object")
    t = schema.get("type")
    names = [t] if isinstance(t, str) else t
    if t is not None and not (isinstance(names, list) and names
                              and all(isinstance(x, str) and x in TYPES for x in names)):
        raise EngineError(f"{at}.type is {t!r}; one of {sorted(TYPES)}, or a list of them")
    if "enum" in schema and not (isinstance(schema["enum"], list) and schema["enum"]):
        raise EngineError(f"{at}.enum is not a non-empty list; no answer could match it")
    req = schema.get("required")
    if req is not None and not (isinstance(req, list) and all(isinstance(x, str) for x in req)):
        raise EngineError(f"{at}.required is {req!r}; a list of names")
    props = schema.get("properties")
    if props is not None and not isinstance(props, dict):
        raise EngineError(f"{at}.properties is not an object")
    # `strict` closes every object, so a required key it does not declare is a
    # key no answer can both carry and be allowed to carry. Only when an object
    # is the only answer allowed: `["object", "null"]` is still met by null.
    undeclared = sorted(set(req or []) - set(props or {}))
    if names and set(names) == {"object"} and undeclared:
        raise EngineError(f"{at}.required names {undeclared}, which properties never declares")
    for k, sub in (props or {}).items():
        check_schema(sub, f"{at}.properties.{k}")
    # One schema for every item, the only form `conform` reads; a tuple or a
    # boolean here would be skipped there and checked by nothing.
    if "items" in schema:
        check_schema(schema["items"], f"{at}.items")


def conform(engine: str, got, schema: dict, at: str = "answer"):
    """`got` if it has the shape `schema` asks for, else EngineError.

    The subset held: `type` (one or a list), `enum`, `required`, `properties`,
    `additionalProperties: false` and `items`, recursively. Combinators
    (`anyOf`, `oneOf`, `allOf`) are not read — enough that a caller can read
    a field without a KeyError, not the whole of JSON Schema.
    """
    want = schema.get("type")
    wants = [want] if isinstance(want, str) else list(want or [])
    if wants and not any(_is(got, w) for w in wants):
        raise EngineError(f"{engine}: {at} is {type(got).__name__}, the schema says {want}")
    if "enum" in schema and not any(json_equal(got, e) for e in schema["enum"]):
        raise EngineError(f"{engine}: {at} is {got!r}, not one of {schema['enum']}")
    if isinstance(got, dict):
        missing = [k for k in schema.get("required") or [] if k not in got]
        if missing:
            raise EngineError(f"{engine}: {at} lacks required {missing}")
        extra = sorted(set(got) - set(schema.get("properties") or {}))
        if schema.get("additionalProperties") is False and extra:
            raise EngineError(f"{engine}: {at} carries {extra}, which the schema closes out")
        for k, sub in (schema.get("properties") or {}).items():
            if k in got and isinstance(sub, dict):
                conform(engine, got[k], sub, f"{at}.{k}")
    if isinstance(got, list) and isinstance(schema.get("items"), dict):
        for i, item in enumerate(got):
            conform(engine, item, schema["items"], f"{at}[{i}]")
    return got


def _spawn(engine: str, argv: list[str], stdin: str | None = None) -> subprocess.CompletedProcess:
    """Run in a session of its own, so a timeout kills whatever it started too.

    UTF-8 both ways, as every file here is read, rather than whatever the locale
    says. Text that cannot cross — a NUL in argv, a lone surrogate, output that
    is not UTF-8 — is this engine not answering, never a crash that takes every
    other claim's verdict down with it.
    """
    try:
        p = subprocess.Popen(argv, encoding="utf-8", start_new_session=True,
                             stdin=subprocess.DEVNULL if stdin is None else subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise EngineError(f"{engine} is not on PATH") from None
    except (OSError, ValueError) as e:     # E2BIG, EACCES, a NUL in argv: it never started
        raise EngineError(f"{engine} could not be started: {e}") from None
    try:
        out, err = p.communicate(stdin, timeout=TIMEOUT)
    except BaseException as e:
        # Its own session means the terminal's Ctrl-C never reaches it, so any
        # way out of here — timeout, interrupt — takes the whole group with it.
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except OSError:
            pass
        p.wait()
        if isinstance(e, subprocess.TimeoutExpired):
            raise EngineError(f"{engine} did not answer within {TIMEOUT}s") from None
        if isinstance(e, UnicodeError):
            raise EngineError(f"{engine}: the exchange is not UTF-8 ({e})") from None
        raise
    r = subprocess.CompletedProcess(argv, p.returncode, out, err)
    if r.returncode != 0:
        raise EngineError(f"{engine} exited {r.returncode}.\n{_tail(r)}")
    return r


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


def printable(text: str) -> str:
    """Engine text as one line a person can read and nothing can rewrite.

    What an engine says is data, and it has read the claim under attack: a
    line break in it printed `[STANDS] C-002` where a verdict line goes, an
    escape could erase the real one, a bidi override reordered it. Each control,
    format, separator or surrogate code point is written as its escape (`\\n`,
    `\\x1b`, `\\u202e`), so every line break in a report is the report's own.
    """
    return "".join(ch.encode("unicode_escape").decode("ascii")
                   if unicodedata.category(ch) in ("Cc", "Cf", "Zl", "Zp", "Cs") else ch
                   for ch in text)


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
            print(f"  {engine}: UNAVAILABLE — {printable(str(e))}")
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
        known = ENGINES.get("runs_on") or []
        if a.running not in known:
            raise EngineError(f"the running engine {a.running!r} is not one of {known}")
        engine = a.engine or other_than(a.running)
        if a.running and engine == a.running:
            raise EngineError(f"{engine} is the engine running this; "
                              "a verdict from it is not a check")
    except EngineError as e:
        print(f"{a.engine or 'checker'}: {e}", file=sys.stderr)
        return 1
    # A file that cannot be read is a usage error, as a missing flag is: 2 and a
    # sentence, not a traceback that exits 1 the way a failed check does.
    try:
        prompt = pathlib.Path(a.prompt_file).read_text(encoding="utf-8")
        schema = json.loads(pathlib.Path(a.schema).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"cannot read --prompt-file / --schema: {e}", file=sys.stderr)
        return 2
    try:
        check_schema(schema)               # malformed, or keys left optional: before any engine
        strict(schema)
    except (AttributeError, TypeError, EngineError) as e:
        print(f"{a.schema}: not a schema this can hold an answer to ({e})", file=sys.stderr)
        return 2
    try:
        got = run(engine, prompt, schema)
    except EngineError as e:
        print(f"{a.engine or 'checker'}: {printable(str(e))}", file=sys.stderr)
        return 1
    print(json.dumps(got, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
