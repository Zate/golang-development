from __future__ import annotations

import importlib.util
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Callable


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "scripts" / "validate_release.py"
SPEC = importlib.util.spec_from_file_location("validate_release", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateReleaseTests(unittest.TestCase):
    def make_repository(self) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        root = Path(temporary_directory.name)
        shutil.copytree(REPOSITORY_ROOT / ".agents", root / ".agents")
        shutil.copytree(REPOSITORY_ROOT / ".claude-plugin", root / ".claude-plugin")
        shutil.copytree(REPOSITORY_ROOT / "plugins", root / "plugins")
        return root

    @staticmethod
    def update_json(path: Path, change: Callable[[dict], None]) -> None:
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def test_current_repository_is_valid(self) -> None:
        self.assertEqual([], VALIDATOR.validate_repository(REPOSITORY_ROOT))

    def test_required_invalid_cases_have_specific_diagnostics(self) -> None:
        cases: list[tuple[str, Callable[[Path], None], str]] = [
            (
                "malformed JSON",
                lambda root: (root / ".agents" / "plugins" / "marketplace.json").write_text(
                    "{", encoding="utf-8"
                ),
                "invalid JSON",
            ),
            (
                "version drift",
                lambda root: self.update_json(
                    root
                    / "plugins"
                    / "golang-development"
                    / ".codex-plugin"
                    / "plugin.json",
                    lambda data: data.__setitem__("version", "9.9.9"),
                ),
                "versions must match",
            ),
            (
                "source escape",
                lambda root: self.update_json(
                    root / ".claude-plugin" / "marketplace.json",
                    lambda data: data["plugins"][0].__setitem__("source", "../outside"),
                ),
                "path must be a ./-prefixed string",
            ),
            (
                "strict conflict",
                lambda root: self.update_json(
                    root / ".claude-plugin" / "marketplace.json",
                    lambda data: data["plugins"][0].__setitem__("strict", False),
                ),
                "strict false conflicts",
            ),
            (
                "invalid skill name",
                lambda root: self.replace_frontmatter(
                    root, r"(?m)^name: .+$", "name: Invalid_Name"
                ),
                "invalid skill name",
            ),
            (
                "missing description",
                lambda root: self.replace_frontmatter(
                    root, r"(?m)^description: .+\n", ""
                ),
                "description is required",
            ),
            (
                "missing license",
                lambda root: self.replace_frontmatter(root, r"(?m)^license: .+\n", ""),
                "license must be MIT",
            ),
            (
                "overlong description",
                lambda root: self.replace_frontmatter(
                    root, r"(?m)^description: .+$", f"description: {'x' * 1025}"
                ),
                "description exceeds 1024 characters",
            ),
            (
                "missing reference",
                lambda root: (
                    root
                    / "plugins"
                    / "golang-development"
                    / "skills"
                    / "golang-testing"
                    / "references"
                    / "testing.md"
                ).unlink(),
                "referenced file is missing",
            ),
            (
                "incomplete OpenAI metadata",
                lambda root: self.remove_openai_field(root),
                "agents/openai.yaml is missing display_name",
            ),
        ]

        for name, mutate, expected in cases:
            with self.subTest(name=name):
                root = self.make_repository()
                mutate(root)
                errors = VALIDATOR.validate_repository(root)
                self.assertTrue(
                    any(expected in error for error in errors),
                    f"Expected {expected!r} in {errors!r}",
                )

    @staticmethod
    def first_skill_file(root: Path) -> Path:
        return (
            root
            / "plugins"
            / "golang-development"
            / "skills"
            / "golang-architecture-patterns"
            / "SKILL.md"
        )

    def replace_frontmatter(self, root: Path, pattern: str, replacement: str) -> None:
        path = self.first_skill_file(root)
        text = path.read_text(encoding="utf-8")
        path.write_text(re.sub(pattern, replacement, text, count=1), encoding="utf-8")

    @staticmethod
    def remove_openai_field(root: Path) -> None:
        path = (
            root
            / "plugins"
            / "golang-development"
            / "skills"
            / "golang-architecture-patterns"
            / "agents"
            / "openai.yaml"
        )
        text = path.read_text(encoding="utf-8")
        path.write_text(re.sub(r"(?m)^\s+display_name:.*\n", "", text, count=1), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
