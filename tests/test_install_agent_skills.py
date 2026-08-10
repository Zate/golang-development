from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "scripts" / "install_agent_skills.py"
SPEC = importlib.util.spec_from_file_location("install_agent_skills", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)


class InstallAgentSkillsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.source = REPOSITORY_ROOT / "plugins" / "golang-development" / "skills"
        self.expected_names = sorted(path.name for path in self.source.iterdir() if path.is_dir())
        self.assertEqual(8, len(self.expected_names))

    def test_default_target_uses_cross_client_user_directory(self) -> None:
        home = self.root / "home"
        self.assertEqual(home / ".agents" / "skills", INSTALLER.default_target(home))

    def test_dry_run_reports_all_targets_without_writes(self) -> None:
        target = self.root / "project" / ".agents" / "skills"
        output = io.StringIO()

        destinations = INSTALLER.install_skills(
            self.source, target, dry_run=True, output=output
        )

        self.assertEqual(self.expected_names, [path.name for path in destinations])
        self.assertEqual(8, output.getvalue().count("[dry-run]"))
        self.assertFalse(target.exists())

    def test_install_copies_complete_skill_directories(self) -> None:
        target = self.root / "custom-skills"

        destinations = INSTALLER.install_skills(self.source, target, output=io.StringIO())

        self.assertEqual(self.expected_names, [path.name for path in destinations])
        for name in self.expected_names:
            source_files = sorted(
                path.relative_to(self.source / name)
                for path in (self.source / name).rglob("*")
                if path.is_file()
            )
            target_files = sorted(
                path.relative_to(target / name)
                for path in (target / name).rglob("*")
                if path.is_file()
            )
            self.assertEqual(source_files, target_files)
            self.assertTrue((target / name / "SKILL.md").is_file())

    def test_collision_stops_before_any_new_skill_is_written(self) -> None:
        target = self.root / "skills"
        collision = target / self.expected_names[3]
        collision.mkdir(parents=True)
        marker = collision / "existing.txt"
        marker.write_text("preserve", encoding="utf-8")

        with self.assertRaises(INSTALLER.InstallError):
            INSTALLER.install_skills(self.source, target, output=io.StringIO())

        self.assertEqual([collision], [path for path in target.iterdir() if path.is_dir()])
        self.assertEqual("preserve", marker.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
