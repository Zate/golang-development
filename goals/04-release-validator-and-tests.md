# G04 - Add A Repository Release Validator

Status: planned

## Objective

Add one repository-owned validation command that checks the complete cross-host package before release.

## Source / context

- The README currently refers to a machine-specific plugin-creator validator path.
- Codex CLI has marketplace install commands but no current `codex plugin validate` command.
- The official `skills-ref` command is useful but is not installed on every machine.

## Scope

- Add a dependency-free release validator under `scripts/`.
- Add automated tests and invalid fixtures for the validator.
- Validate all JSON manifests and cross-file names, versions, and source paths.
- Validate all Agent Skills frontmatter constraints required by this repository.
- Validate required references and OpenAI metadata file placement.
- Validate that the Claude marketplace does not use the known strict-mode conflict.
- Return a nonzero exit code and clear messages for each failure.

## Non-goals

- Do not replace official Claude Code or `skills-ref` validators.
- Do not install host CLIs or external packages.
- Do not run live marketplace installation.
- Do not modify files while validating.

## Implementation notes

- Use a standard-library-only runtime that is available on supported development systems.
- Keep validation deterministic and offline.
- Tests must cover malformed JSON, version drift, invalid source paths, invalid skill names, missing descriptions, missing licenses, overlong descriptions, missing references, and the Claude strict-mode conflict.
- Make output useful to a human and to CI.

## Acceptance criteria

- One documented command validates the complete repository package.
- A valid checkout exits zero.
- Every required negative fixture exits nonzero with a specific diagnostic.
- The validator checks all eight skills without a hard-coded skill count that hides additions or removals.
- The validator makes no repository changes.

## Definition of done

- Acceptance criteria are met.
- Focused tests are added.
- The validator help and failure output are clear.
- Required verification commands pass.
- Status is changed to `complete`.
- `goals/index.md` marks this goal complete.
- The work is committed in one focused commit.

## Verification

- `python scripts/validate_release.py`
- `python -m unittest discover -s tests`
- `claude plugin validate . --strict`
- `claude plugin validate ./plugins/golang-development --strict`
