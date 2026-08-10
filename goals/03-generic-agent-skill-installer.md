# G03 - Add A Safe Generic Skill Installer

Status: planned

## Objective

Provide a safe way to install all eight skills for generic agents that scan user-level or project-level `.agents/skills` directories.

## Source / context

- Generic Agent Skills clients commonly scan `~/.agents/skills/` and `<project>/.agents/skills/`.
- The repository stores canonical skills under `plugins/golang-development/skills/`.
- Duplicating those skills elsewhere in the repository would create drift.

## Scope

- Add a cross-platform installation method for user-level and explicit project-level targets.
- Install complete skill directories, including references and optional host metadata.
- Default to `~/.agents/skills/` only when the user does not give a target.
- Add a dry-run mode.
- Detect existing target names before any write.
- Fail safely on collisions by default.
- Add focused installer tests that use temporary target directories.

## Non-goals

- Do not create duplicate canonical skill copies under the repository `.agents/skills/` directory.
- Do not overwrite existing skills without an explicit force or update option.
- Do not write to real user-level agent directories during tests.
- Do not change Codex or Claude Code plugin installation.

## Implementation notes

- Prefer scripts with no external package dependencies.
- Support Windows PowerShell and a common POSIX environment, either with native wrappers or one portable implementation plus thin wrappers.
- Resolve source and target paths before any copy.
- Validate the exact target boundary and target count before an overwrite option runs.
- If update or force mode exists, document its recovery and replacement behavior.

## Acceptance criteria

- A user can install all eight skills into `~/.agents/skills/`.
- A user can install all eight skills into an explicit `<project>/.agents/skills/` path.
- Dry-run reports the exact eight target directories and makes no changes.
- A collision stops the install before partial changes occur.
- A successful test install contains eight valid `SKILL.md` files and every required reference file.
- Tests run only against temporary directories.

## Definition of done

- Acceptance criteria are met.
- Focused tests cover success, dry-run, custom target, and collision failure.
- Installation safety is documented in script help.
- Required verification commands pass.
- Status is changed to `complete`.
- `goals/index.md` marks this goal complete.
- The work is committed in one focused commit.

## Verification

- Run the installer test suite with temporary targets.
- Run dry-run for a user-level target and a project-level target.
- Confirm that no real `~/.agents/skills/` files changed during verification.
