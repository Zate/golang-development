# Golang Development goals

This queue makes the Golang Development skill bundle installable as a plugin marketplace for Codex and Claude Code. It also makes each skill installable through the cross-client `.agents/skills` convention.

## Operating Rules

- Work goals in queue order.
- Complete one goal per commit.
- Do not begin the next goal with uncommitted changes from the previous goal.
- Preserve one shared copy of each skill under `plugins/golang-development/skills/`.
- Keep Codex, Claude Code, and generic Agent Skills support additive.
- Do not rename, create, push, or publish a remote repository without user authority.
- Stop and ask the user when blocked by a repository-name decision, credentials, remote access, or unsafe changes.

## Model And Token Guidance

- Use a high-reasoning coding model for manifest design, installation safety, validation rules, and isolated host tests.
- Use a normal coding model for documentation and mechanical metadata changes after the contracts are clear.
- Read only the current goal, this index, and the files that the goal names.
- Load detailed skill references only when the current task needs them.

## Goal File Format

Each goal file contains one objective, source context, scope, non-goals, implementation notes, acceptance criteria, definition of done, and verification commands. Allowed statuses are `planned`, `in_progress`, `blocked`, `complete`, and `retired`.

## Execution Loop

1. Check `git status --short` and preserve unrelated user changes.
2. Select the first unchecked goal that is not blocked or retired.
3. Read this index, the selected goal, repository guidance, and only the required implementation files.
4. Change the goal status to `in_progress`.
5. Implement only the selected goal.
6. Run its focused verification and the available baseline checks below.
7. Change the goal status to `complete`, add useful completion notes, and check the goal in this queue.
8. Commit the complete goal in one focused commit.
9. Confirm that the worktree is clean before the next goal.

## Definition Of Done

- The goal acceptance criteria are met.
- Focused tests are added or updated when behavior changes.
- Relevant installation or maintenance documentation is updated.
- Required verification commands pass.
- No user-level Codex or Claude Code configuration is changed during automated tests.
- The goal status and queue checkbox agree.
- The work is committed in one focused commit.

## Verification

Use the checks that exist at the current point in the queue:

- `claude plugin validate . --strict`
- `claude plugin validate ./plugins/golang-development --strict`
- `python scripts/validate_release.py`
- `python -m unittest discover -s tests`
- `skills-ref validate <skill-directory>` for every directory under `plugins/golang-development/skills/`

The release validator and tests do not exist before G04. The CI workflow does not exist before G05. For earlier goals, use the Claude Code validators and direct JSON and skill checks.

## Blocking And Recovery

- Set a goal to `blocked` only when a required decision, credential, external service, or remote repository is unavailable.
- Add a `Blocked notes` section that states the blocker, checks already completed, and the exact input needed from the user.
- Do not mark a blocked goal complete.
- If a host validator is not installed, run the repository-owned checks and record the missing host gate as residual risk.
- If the public GitHub repository does not exist when G08 starts, block G08. Do not create or rename the repository automatically.

## Queue

- [x] [G01 - Normalize Dual Marketplace Manifests](01-normalize-dual-marketplace-manifests.md)
- [ ] [G02 - Make Skill Metadata Portable](02-portable-agent-skill-metadata.md)
- [ ] [G03 - Add A Safe Generic Skill Installer](03-generic-agent-skill-installer.md)
- [ ] [G04 - Add A Repository Release Validator](04-release-validator-and-tests.md)
- [ ] [G05 - Add Continuous Integration Gates](05-continuous-integration-gates.md)
- [ ] [G06 - Document All Installation Paths](06-installation-and-usage-documentation.md)
- [ ] [G07 - Verify Local Marketplace Installation](07-isolated-local-marketplace-smoke-tests.md)
- [ ] [G08 - Verify GitHub Marketplace Installation](08-github-marketplace-smoke-tests.md)
