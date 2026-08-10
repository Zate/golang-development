# G05 - Add Continuous Integration Gates

Status: planned

## Objective

Run portable skill, manifest, installer, and release checks automatically for every proposed change.

## Source / context

- The repository needs durable validation that does not depend on one developer machine.
- The generic installer must work on Windows and a POSIX system.
- Official Agent Skills validation should supplement the repository validator.

## Scope

- Add a GitHub Actions workflow for pull requests and main-branch changes.
- Run the repository validator and unit tests.
- Run installer tests on Windows and Ubuntu.
- Run the official `skills-ref` validator for every skill with a pinned installation method.
- Parse and validate both marketplace formats without credentials.
- Use dependency caching only when it is safe and useful.

## Non-goals

- Do not require OpenAI or Anthropic account credentials.
- Do not install this plugin into a real user profile.
- Do not run the live GitHub marketplace smoke test in normal pull-request CI.
- Do not publish releases or artifacts.

## Implementation notes

- Pin third-party action versions and the `skills-ref` tool version or commit.
- Keep secrets out of logs.
- Use temporary directories for installer tests.
- If Claude Code validation can run without authentication and with a pinned CLI, it can be an additional gate. Do not make CI depend on an unstable unpinned host download.

## Acceptance criteria

- CI runs on Windows and Ubuntu.
- CI validates all skills with the repository validator and `skills-ref`.
- CI tests generic installation without changing a real home directory.
- CI fails for invalid manifests, invalid skill metadata, missing references, or installer regressions.
- CI does not require credentials or remote writes.

## Definition of done

- Acceptance criteria are met.
- Workflow syntax is validated.
- A local equivalent of each CI command passes.
- Required verification commands pass.
- Status is changed to `complete`.
- `goals/index.md` marks this goal complete.
- The work is committed in one focused commit.

## Verification

- `python scripts/validate_release.py`
- `python -m unittest discover -s tests`
- Run each documented CI command locally where the current operating system supports it.
- Inspect the first GitHub Actions run when remote access is available.
