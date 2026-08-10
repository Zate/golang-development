#!/usr/bin/env python3
"""Install the bundled skills into a cross-client .agents/skills directory."""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path
from typing import TextIO


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPOSITORY_ROOT / "plugins" / "golang-development" / "skills"


class InstallError(RuntimeError):
    """A safe installation precondition was not met."""


def default_target(home: Path | None = None) -> Path:
    """Return the user-level cross-client Agent Skills directory."""

    return (home or Path.home()) / ".agents" / "skills"


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def discover_skills(source: Path) -> list[Path]:
    """Return valid skill directories in stable name order."""

    source = source.expanduser().resolve()
    if not source.is_dir():
        raise InstallError(f"Skill source is not a directory: {source}")

    links = [path for path in source.rglob("*") if path.is_symlink()]
    if links:
        names = ", ".join(str(path) for path in links)
        raise InstallError(f"Skill source contains symbolic links: {names}")

    skills = sorted(
        path for path in source.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    )
    if not skills:
        raise InstallError(f"No skill directories were found in: {source}")
    return skills


def install_skills(
    source: Path,
    target: Path,
    *,
    dry_run: bool = False,
    output: TextIO = sys.stdout,
) -> list[Path]:
    """Install every skill after a complete collision preflight."""

    source = source.expanduser().resolve()
    target = target.expanduser().resolve()
    skills = discover_skills(source)

    if target.exists() and not target.is_dir():
        raise InstallError(f"Install target is not a directory: {target}")
    if _is_within(target, source) or _is_within(source, target):
        raise InstallError("Skill source and install target must not contain each other")

    destinations = [target / skill.name for skill in skills]
    collisions = [path for path in destinations if path.exists()]
    if collisions:
        names = ", ".join(path.name for path in collisions)
        raise InstallError(
            f"Install stopped before changes. Target skills already exist: {names}"
        )

    action = "Would install" if dry_run else "Installing"
    print(f"{action} {len(skills)} skills from {source} to {target}", file=output)
    for skill, destination in zip(skills, destinations, strict=True):
        prefix = "[dry-run]" if dry_run else "[install]"
        print(f"{prefix} {skill.name} -> {destination}", file=output)

    if dry_run:
        return destinations

    target_parent = target.parent
    target_parent.mkdir(parents=True, exist_ok=True)
    target_existed = target.exists()
    staging = Path(tempfile.mkdtemp(prefix=".golang-development-", dir=target_parent))
    created: list[Path] = []
    try:
        for skill in skills:
            shutil.copytree(skill, staging / skill.name)

        target.mkdir(parents=True, exist_ok=True)
        for staged, destination in zip(
            sorted(staging.iterdir()), destinations, strict=True
        ):
            staged.replace(destination)
            created.append(destination)
    except Exception:
        for path in reversed(created):
            shutil.rmtree(path)
        if not target_existed and target.exists() and not any(target.iterdir()):
            target.rmdir()
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)

    return destinations


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Install the Golang Development skill directories for agents that scan "
            "the cross-client .agents/skills convention. Existing skill names are "
            "never overwritten."
        )
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=default_target(),
        help="Target skills directory. Default: ~/.agents/skills",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the exact target directories without writing files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        install_skills(args.source, args.target, dry_run=args.dry_run)
    except InstallError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"error: installation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
