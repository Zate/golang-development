# G07 - Verify Local Marketplace Installation

Status: planned

## Objective

Prove that a clean local clone can act as a marketplace and install the plugin in both Codex and Claude Code without changing the user's normal configuration.

## Source / context

- Schema validation does not prove that each host can resolve, install, cache, and register all skills.
- Both hosts support local marketplace paths.

## Scope

- Use isolated temporary configuration and cache directories for Codex.
- Use isolated temporary configuration and cache directories for Claude Code.
- Add the repository root as a local marketplace in each host.
- Install `golang-development@golang-development-marketplace` in each host.
- Confirm that the plugin is enabled and exposes exactly the expected eight skills.
- Record repeatable commands and summarized results in repository validation documentation.
- Confirm that the real user profiles do not change.

## Non-goals

- Do not use or modify existing installed copies as proof.
- Do not test the GitHub marketplace source.
- Do not publish or push anything.
- Do not run a model task or consume API credits when inventory commands are sufficient.

## Implementation notes

- Check current Codex and Claude Code documentation for their isolated configuration environment variables before running tests.
- Pre-create temporary home/config directories when a host requires them.
- Resolve and inspect every cleanup target. Remove only the exact temporary test directory after successful inspection.
- A host inventory command must show all eight skill names.

## Acceptance criteria

- A fresh isolated Codex configuration adds the local marketplace and installs the plugin.
- A fresh isolated Claude Code configuration adds the local marketplace and installs the plugin.
- Both inventories show the same plugin name, version, and eight skills.
- The tests do not change normal user-level host configuration or caches.
- Repeatable evidence is recorded without personal secrets or unstable temporary paths.

## Definition of done

- Acceptance criteria are met.
- The repository validator and unit tests pass before and after the smoke tests.
- Validation documentation is updated.
- Status is changed to `complete`.
- `goals/index.md` marks this goal complete.
- The work is committed in one focused commit.

## Verification

- `python scripts/validate_release.py`
- `python -m unittest discover -s tests`
- Run the documented isolated Codex local-marketplace test.
- Run the documented isolated Claude Code local-marketplace test.
- Compare user configuration state before and after the tests.
