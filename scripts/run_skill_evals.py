#!/usr/bin/env python3
"""Run shared behavioral cases in isolated Claude or Codex sessions.

Claude uses its native graders and no-plugin baseline. Codex records traces for
manual rubric review; invoke once with --plugin and once without it to compare.
No global installation or report publishing occurs. Claude uses its normal
authentication and native evaluation isolation; Codex copies auth into a temporary home.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]


def codex_metrics(path: Path) -> dict:
    """Summarize successful tool reads and host-reported usage, not skill-only cost."""
    totals = {key: 0 for key in ("input_tokens", "cached_input_tokens", "output_tokens")}
    skills: set[str] = set()
    references: set[str] = set()
    calls = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue  # CLI notices can precede the JSONL stream.
        if event.get("type") == "turn.completed":
            for key in totals:
                totals[key] += event.get("usage", {}).get(key, 0)
        item = event.get("item", {})
        if event.get("type") == "item.completed" and item.get("type") in (
            "command_execution", "web_search", "mcp_tool_call",
        ):
            calls += 1
        if item.get("type") == "command_execution" and item.get("exit_code") == 0:
            command = item.get("command", "")
            if re.search(r"\bcat\b", command):
                skills.update(re.findall(r"\.agents/skills/(golang-[a-z-]+)/SKILL\.md", command))
                references.update(re.findall(r"\.agents/skills/(golang-[a-z-]+/references/[\w.-]+)", command))
    return {**totals, "tool_calls": calls, "skills_read": sorted(skills),
            "references_read": sorted(references)}


def cases_from(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("cases"), list):
        raise ValueError("Expected schema_version 1 and a cases list")
    cases = data["cases"]
    names: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("Every case must be an object")
        name = case.get("name", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name in names:
            raise ValueError(f"Invalid or duplicate case name: {name}")
        names.add(name)
        for field in ("prompt", "rubric"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                raise ValueError(f"{name}: missing {field}")
        if not isinstance(case.get("skills"), list) or any(
            not isinstance(skill, str) or not skill.startswith("golang-")
            for skill in case["skills"]
        ):
            raise ValueError(f"{name}: invalid skills")
    if not cases:
        raise ValueError("No cases")
    return cases


def write_claude_suite(plugin: Path, cases: list[dict]) -> None:
    """Adapt the shared dataset to native Claude Code evals, in a copied plugin."""
    for case in cases:
        folder = plugin / "evals" / case["name"]
        (folder / "graders").mkdir(parents=True)
        (folder / "prompt.md").write_text(
            "---\nmax_turns: 12\ntimeout_seconds: 180\n"
            "allowed_tools: [Read, Glob, Grep, Skill]\n---\n" + case["prompt"] + "\n",
            encoding="utf-8",
        )
        (folder / "graders" / "outcome.md").write_text(
            "---\ntype: llm\n---\n" + case["rubric"] + "\n", encoding="utf-8"
        )
        if case["skills"]:
            names = "|".join(re.escape(name) for name in case["skills"])
            pattern = rf'"skill"\s*:\s*"(?:[\w-]+:)?(?:{names})"'
            (folder / "graders" / "activation.md").write_text(
                "---\ntype: tool_used\ntool: Skill\ninput_match: '" + pattern + "'\n---\n",
                encoding="utf-8",
            )
        else:
            (folder / "graders" / "no-activation.md").write_text(
                "---\ntype: tool_used\ntool: Skill\nmin: 0\nmax: 0\narm: both\n---\n",
                encoding="utf-8",
            )


def execute(command: list[str], *, cwd: Path, env: dict, output: Path,
            timeout: int) -> tuple[int, float]:
    start = time.monotonic()
    with output.open("w", encoding="utf-8") as stream:
        try:
            result = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=timeout, check=False)
            return result.returncode, round(time.monotonic() - start, 2)
        except subprocess.TimeoutExpired:
            return 124, round(time.monotonic() - start, 2)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=("claude", "codex"), required=True)
    parser.add_argument("--plugin", type=Path,
                        help="Plugin source; omit for a Codex no-plugin baseline")
    parser.add_argument("--cases", type=Path, default=ROOT / "evals" / "cases.json")
    parser.add_argument("--case", action="append", help="Select case name (repeatable)")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--model", help="Explicit host model for repeatable comparisons; otherwise host default")
    parser.add_argument("--keep-temp", action="store_true", help="Keep native Claude trace directories for token/tool inspection")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.runs <= 10:
        parser.error("--runs must be between 1 and 10")
    if args.host == "claude" and args.plugin is None:
        parser.error("Claude needs --plugin; its native eval runs the no-plugin arm")
    cases = cases_from(args.cases)
    if args.case:
        unknown = set(args.case) - {case["name"] for case in cases}
        if unknown:
            parser.error(f"Unknown cases: {sorted(unknown)}")
        cases = [case for case in cases if case["name"] in args.case]
    cases_digest = hashlib.sha256(json.dumps(cases, sort_keys=True).encode()).hexdigest()
    if not shutil.which(args.host):
        parser.error(f"{args.host} is not installed")
    output = args.output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=False)
    versions = subprocess.run([args.host, "--version"], capture_output=True, text=True,
                              check=True).stdout.strip()
    records = []
    plugin_digest = None
    with tempfile.TemporaryDirectory(prefix="go-skill-evals-") as directory:
        temporary = Path(directory)
        env = os.environ.copy()
        plugin = None
        if args.plugin:
            plugin = temporary / "plugin"
            shutil.copytree(args.plugin.resolve(), plugin)
            digest = hashlib.sha256()
            for path in sorted(plugin.rglob("*")):
                if path.is_file():
                    digest.update(path.relative_to(plugin).as_posix().encode() + b"\0")
                    digest.update(path.read_bytes())
            plugin_digest = digest.hexdigest()
        if args.host == "claude":
            assert plugin is not None
            write_claude_suite(plugin, cases)
            # Native plugin eval isolates settings, skills and hooks itself.
            # Keep the normal authentication path; never publish the report.
            command = ["claude", "plugin", "eval", str(plugin), "--trust-plugin",
                       "--no-publish", "--runs", str(args.runs), "--concurrency", "1",
                       "--output-dir", str(output / "native")]
            if args.model:
                command += ["--model", args.model]
            if args.keep_temp:
                command += ["--keep-temp"]
            code, elapsed = execute(command, cwd=temporary, env=env,
                                    output=output / "claude.log", timeout=3600)
            records.append({"exit_code": code, "elapsed_seconds": elapsed})
        else:
            normal_home = Path(env.get("CODEX_HOME", str(Path.home() / ".codex")))
            home = temporary / "codex"
            home.mkdir()
            auth = normal_home / "auth.json"
            if auth.is_file():
                shutil.copyfile(auth, home / "auth.json")
                (home / "auth.json").chmod(0o600)
            env["CODEX_HOME"] = str(home)
            for case in cases:
                for repeat in range(args.runs):
                    work = temporary / f"{case['name']}-{repeat + 1}"
                    work.mkdir()
                    if plugin:
                        shutil.copytree(plugin / "skills", work / ".agents" / "skills")
                    log = output / f"{case['name']}-{repeat + 1}.jsonl"
                    command = ["codex", "exec", "--ignore-user-config", "--ignore-rules",
                               "--ephemeral", "--skip-git-repo-check", "--sandbox", "read-only",
                               "--json", "-C", str(work), case["prompt"]]
                    if args.model:
                        command[2:2] = ["--model", args.model]
                    code, elapsed = execute(command, cwd=work, env=env, output=log, timeout=240)
                    records.append({"case": case["name"], "run": repeat + 1,
                                    "exit_code": code, "elapsed_seconds": elapsed,
                                    "trace": log.name, "metrics": codex_metrics(log)})
                    print(f"{case['name']} run {repeat + 1}: exit {code}, {elapsed}s", flush=True)
    (output / "run.json").write_text(json.dumps({
        "host": args.host, "version": versions,
        "model_requested": args.model or "host default",
        "cases_sha256": cases_digest,
        "plugin_sha256": plugin_digest,
        "plugin": str(args.plugin.resolve()) if args.plugin else None,
        "cases": [case["name"] for case in cases], "runs": args.runs,
        "records": records, "grading": "native" if args.host == "claude" else "manual rubric review",
    }, indent=2) + "\n", encoding="utf-8")
    return 0 if all(record["exit_code"] == 0 for record in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
