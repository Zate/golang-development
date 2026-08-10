#!/usr/bin/env python3
"""Run the official Agent Skills reference validator on every bundled skill."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "plugins" / "golang-development" / "skills"


def main() -> int:
    executable = shutil.which("skills-ref")
    if executable is None:
        print(
            "error: skills-ref is not installed. Use the pinned installation command "
            "from .github/workflows/validate.yml.",
            file=sys.stderr,
        )
        return 2

    skills = sorted(
        path for path in SKILLS_ROOT.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    )
    if not skills:
        print(f"error: no skills found in {SKILLS_ROOT}", file=sys.stderr)
        return 2

    failures = 0
    for skill in skills:
        print(f"Validating {skill.name} with skills-ref")
        result = subprocess.run(
            [executable, "validate", str(skill)],
            cwd=REPOSITORY_ROOT,
            check=False,
        )
        if result.returncode != 0:
            failures += 1

    if failures:
        print(f"skills-ref failed for {failures} skill(s).", file=sys.stderr)
        return 1
    print(f"skills-ref passed for {len(skills)} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
