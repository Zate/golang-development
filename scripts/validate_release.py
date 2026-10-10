#!/usr/bin/env python3
"""Validate the complete Golang Development dual-host plugin package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_PATTERN = re.compile(r"references/[A-Za-z0-9._/-]+")
EXPECTED_LICENSE = "MIT"
EXPECTED_SKILLS = {
    "golang-development-workflow", "golang-code-audit", "golang-planning-layout",
    "golang-architecture-patterns", "golang-implementation-idioms", "golang-testing",
    "golang-quality-linting", "golang-build-deploy",
}


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _load_json(root: Path, relative_path: str, errors: list[str]) -> dict[str, Any] | None:
    path = root / relative_path
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{relative_path}: file is missing")
        return None
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        errors.append(f"{relative_path}: invalid JSON: {error}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{relative_path}: JSON root must be an object")
        return None
    return data


def _plugin_entry(
    manifest: dict[str, Any], relative_path: str, errors: list[str]
) -> dict[str, Any] | None:
    plugins = manifest.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
        errors.append(f"{relative_path}: plugins must contain one plugin object")
        return None
    return plugins[0]


def _resolve_package_path(
    root: Path, raw_path: Any, label: str, errors: list[str]
) -> Path | None:
    if not isinstance(raw_path, str) or not raw_path.startswith("./"):
        errors.append(f"{label}: path must be a ./-prefixed string")
        return None
    resolved = (root / raw_path).resolve()
    if not _is_within(resolved, root):
        errors.append(f"{label}: path escapes the repository root: {raw_path}")
        return None
    if not resolved.exists():
        errors.append(f"{label}: path does not exist: {raw_path}")
        return None
    return resolved


def _frontmatter(skill_file: Path, errors: list[str]) -> tuple[dict[str, str], list[str]]:
    relative = skill_file.as_posix()
    try:
        lines = skill_file.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        errors.append(f"{relative}: cannot read SKILL.md: {error}")
        return {}, []
    if not lines or lines[0] != "---":
        errors.append(f"{relative}: SKILL.md must start with YAML frontmatter")
        return {}, lines
    try:
        closing = lines.index("---", 1)
    except ValueError:
        errors.append(f"{relative}: SKILL.md frontmatter is not closed")
        return {}, lines

    metadata: dict[str, str] = {}
    for line in lines[1:closing]:
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"{relative}: invalid top-level frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in metadata:
            errors.append(f"{relative}: duplicate frontmatter field: {key}")
        metadata[key] = value.strip("\"'")
    return metadata, lines


def _validate_skill(skill_dir: Path, plugin_root: Path, errors: list[str]) -> None:
    skill_file = skill_dir / "SKILL.md"
    relative = skill_file.relative_to(plugin_root).as_posix()
    metadata, lines = _frontmatter(skill_file, errors)

    name = metadata.get("name", "")
    if not name:
        errors.append(f"{relative}: name is required")
    elif not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        errors.append(f"{relative}: invalid skill name: {name}")
    elif name != skill_dir.name:
        errors.append(f"{relative}: name must match directory {skill_dir.name}")

    description = metadata.get("description", "")
    if not description:
        errors.append(f"{relative}: description is required")
    elif len(description) > 1024:
        errors.append(f"{relative}: description exceeds 1024 characters")

    license_name = metadata.get("license", "")
    if license_name != EXPECTED_LICENSE:
        errors.append(f"{relative}: license must be {EXPECTED_LICENSE}")
    if len(lines) > 500:
        errors.append(f"{relative}: SKILL.md exceeds 500 lines")

    text = "\n".join(lines)
    for reference in sorted(set(REFERENCE_PATTERN.findall(text))):
        reference_path = Path(reference)
        resolved = (skill_dir / reference_path).resolve()
        if ".." in reference_path.parts or not _is_within(resolved, skill_dir.resolve()):
            errors.append(f"{relative}: reference escapes the skill directory: {reference}")
        elif not resolved.is_file():
            errors.append(f"{relative}: referenced file is missing: {reference}")

    openai_files = list(skill_dir.rglob("openai.yaml"))
    expected_openai = skill_dir / "agents" / "openai.yaml"
    if openai_files != [expected_openai]:
        errors.append(f"{relative}: agents/openai.yaml is missing or misplaced")
        return
    try:
        openai_text = expected_openai.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        errors.append(f"{relative}: cannot read agents/openai.yaml: {error}")
        return
    for field in ("interface:", "display_name:", "short_description:", "default_prompt:"):
        if field not in openai_text:
            errors.append(f"{relative}: agents/openai.yaml is missing {field.rstrip(':')}")
    if name and f"${name}" not in openai_text:
        errors.append(f"{relative}: default_prompt must name ${name}")


def validate_repository(root: Path) -> list[str]:
    """Return all release validation errors for a repository root."""

    root = root.expanduser().resolve()
    errors: list[str] = []
    if not root.is_dir():
        return [f"Repository root is not a directory: {root}"]

    codex_market_path = ".agents/plugins/marketplace.json"
    claude_market_path = ".claude-plugin/marketplace.json"
    codex_plugin_path = "plugins/golang-development/.codex-plugin/plugin.json"
    claude_plugin_path = "plugins/golang-development/.claude-plugin/plugin.json"

    codex_market = _load_json(root, codex_market_path, errors)
    claude_market = _load_json(root, claude_market_path, errors)
    codex_plugin = _load_json(root, codex_plugin_path, errors)
    claude_plugin = _load_json(root, claude_plugin_path, errors)
    if None in (codex_market, claude_market, codex_plugin, claude_plugin):
        return errors
    assert codex_market is not None
    assert claude_market is not None
    assert codex_plugin is not None
    assert claude_plugin is not None

    codex_entry = _plugin_entry(codex_market, codex_market_path, errors)
    claude_entry = _plugin_entry(claude_market, claude_market_path, errors)
    if codex_entry is None or claude_entry is None:
        return errors

    plugin_root = root / "plugins" / "golang-development"
    codex_source = codex_entry.get("source")
    if not isinstance(codex_source, dict) or codex_source.get("source") != "local":
        errors.append(f"{codex_market_path}: source must use the local source type")
    else:
        resolved = _resolve_package_path(
            root, codex_source.get("path"), f"{codex_market_path}: source.path", errors
        )
        if resolved is not None and resolved != plugin_root.resolve():
            errors.append(f"{codex_market_path}: source.path must resolve to {plugin_root}")

    resolved = _resolve_package_path(
        root, claude_entry.get("source"), f"{claude_market_path}: source", errors
    )
    if resolved is not None and resolved != plugin_root.resolve():
        errors.append(f"{claude_market_path}: source must resolve to {plugin_root}")

    expected_plugin_name = plugin_root.name
    expected_market_name = f"{expected_plugin_name}-marketplace"
    if codex_market.get("name") != expected_market_name:
        errors.append(f"{codex_market_path}: unexpected marketplace name")
    if claude_market.get("name") != expected_market_name:
        errors.append(f"{claude_market_path}: unexpected marketplace name")
    for label, manifest in (
        (codex_market_path, codex_entry),
        (claude_market_path, claude_entry),
        (codex_plugin_path, codex_plugin),
        (claude_plugin_path, claude_plugin),
    ):
        if manifest.get("name") != expected_plugin_name:
            errors.append(f"{label}: plugin name must be {expected_plugin_name}")

    versions = {
        codex_plugin.get("version"),
        claude_plugin.get("version"),
        claude_entry.get("version"),
    }
    if len(versions) != 1 or None in versions:
        errors.append("Plugin and marketplace versions must match")

    repositories = {
        codex_plugin.get("repository"),
        claude_plugin.get("repository"),
        claude_entry.get("repository"),
    }
    if len(repositories) != 1 or None in repositories:
        errors.append("Plugin and marketplace repository URLs must match")

    if claude_entry.get("strict") is False and claude_plugin.get("skills"):
        errors.append(
            f"{claude_market_path}: strict false conflicts with plugin-defined skills"
        )

    skill_roots: list[Path] = []
    for label, manifest in (
        (codex_plugin_path, codex_plugin),
        (claude_plugin_path, claude_plugin),
    ):
        skill_root = _resolve_package_path(
            plugin_root, manifest.get("skills"), f"{label}: skills", errors
        )
        if skill_root is not None:
            skill_roots.append(skill_root)
    if skill_roots and any(path != skill_roots[0] for path in skill_roots[1:]):
        errors.append("Codex and Claude plugin manifests must use the same skills directory")

    skills_root = plugin_root / "skills"
    if not skills_root.is_dir():
        errors.append("Plugin skills directory is missing")
        return errors
    skill_directories = sorted(path for path in skills_root.iterdir() if path.is_dir())
    if {path.name for path in skill_directories} != EXPECTED_SKILLS:
        errors.append("Plugin must contain exactly the eight canonical Go skills")
    for skill_dir in skill_directories:
        if not (skill_dir / "SKILL.md").is_file():
            errors.append(f"{skill_dir.relative_to(root)}: skill directory has no SKILL.md")
            continue
        _validate_skill(skill_dir, plugin_root, errors)

    lint_files = [
        plugin_root / "golangci.yaml",
        skills_root / "golang-quality-linting" / "references" / "golangci-recommended.yaml",
    ]
    contents = []
    for path in lint_files:
        try:
            contents.append(path.read_bytes())
        except OSError as error:
            errors.append(f"{path.relative_to(root)}: cannot read lint configuration: {error}")
    if len(contents) == 2 and contents[0] != contents[1]:
        errors.append("Plugin and installable lint configurations must be identical")

    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the dual-host plugin release package.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root. Default: parent of this script directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    errors = validate_repository(args.root)
    if errors:
        print(f"Release validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Release validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
