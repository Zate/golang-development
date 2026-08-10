# G08 - Verify GitHub Marketplace Installation

Status: complete

## Objective

Prove that Codex and Claude Code can add the published GitHub repository as a marketplace and install the same plugin from it.

## Source / context

- The user wants either host to accept an `owner/repo` marketplace source such as `Zate/golang-skill`.
- The final repository name can differ from the current local remote.
- This goal depends on the completed changes being available in a public or authenticated GitHub repository.

## Scope

- Confirm the canonical GitHub repository URL and default branch.
- Confirm that README and manifest repository metadata use that URL.
- Use fresh isolated Codex configuration to add the `owner/repo` marketplace and install the plugin.
- Use fresh isolated Claude Code configuration to add the same `owner/repo` marketplace and install the plugin.
- Confirm plugin identity, version, and all eight skills in both hosts.
- Record the tested commit and summarized results.

## Non-goals

- Do not create, rename, make public, push, tag, or release the GitHub repository without explicit user authority.
- Do not use normal user host profiles for the smoke test.
- Do not submit the plugin to the OpenAI or Anthropic public directory.
- Do not require a model task when inventory checks prove registration.

## Implementation notes

- If the repository is not available at the required GitHub URL, set this goal to `blocked` and ask the user to publish or identify the correct repository.
- Use the same `owner/repo` input in both hosts.
- Pin or record the tested Git commit so later failures can be compared with known evidence.
- Keep network activity read-only after the repository is published.

## Acceptance criteria

- `codex plugin marketplace add <owner>/<repo>` succeeds in an isolated configuration.
- `codex plugin add golang-development@golang-development-marketplace` succeeds and exposes eight skills.
- `claude plugin marketplace add <owner>/<repo>` succeeds in an isolated configuration.
- `claude plugin install golang-development@golang-development-marketplace` succeeds and exposes eight skills.
- Both hosts load the same plugin version from the same tested Git commit.
- README commands match the successful commands exactly.
- No normal user configuration changes occur.

## Definition of done

- Acceptance criteria are met.
- The tested repository URL and commit are recorded.
- All release, unit, and host validation checks pass.
- Status is changed to `complete`.
- `goals/index.md` marks this goal complete.
- The work is committed in one focused commit.

## Verification

- `python scripts/validate_release.py`
- `python -m unittest discover -s tests`
- Run the documented isolated Codex GitHub-marketplace test.
- Run the documented isolated Claude Code GitHub-marketplace test.
- Confirm both host inventories contain the expected eight skills.

## Completion notes

- The canonical GitHub source is `Zate/golang-development`, with `main` as its default branch.
- The user authorized publication of the completed commits.
- Codex and Claude Code added the same GitHub source and installed `golang-development@golang-development-marketplace` in isolated host profiles.
- Both hosts loaded version `0.1.0`, the same eight skills, and Git commit `15b90cbf047cb4a2855e1124845a1c23ef262793`.
- Normal user host profile changes were zero.
- The README GitHub commands match the successful commands.
- GitHub Actions run `31356286623` passed all release, unit, installer, and Agent Skills validation steps on Windows and Ubuntu.
