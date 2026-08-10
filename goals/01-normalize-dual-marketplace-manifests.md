# G01 - Normalize Dual Marketplace Manifests

Status: complete

## Objective

Make the repository and plugin manifests follow the current Codex and Claude Code marketplace rules from one shared plugin tree.

## Source / context

- The user requires local-path and GitHub marketplace installation in Codex and Claude Code.
- The current Claude marketplace sets `strict: false` while the plugin manifest declares skills.
- The current Git remote is an input, but the user can publish this repository under a different final GitHub name.

## Scope

- Normalize `.agents/plugins/marketplace.json` for Codex.
- Normalize `.claude-plugin/marketplace.json` for Claude Code.
- Normalize both plugin manifests under `plugins/golang-development/`.
- Remove or correct the Claude Code `strict: false` conflict.
- Keep plugin names, marketplace names, versions, descriptions, authors, licenses, and source paths consistent.
- Add useful repository and homepage metadata when the canonical public URL is known.

## Non-goals

- Do not rename or publish the GitHub repository.
- Do not add the generic `.agents/skills` installer.
- Do not submit the plugin to a public OpenAI or Anthropic directory.
- Do not merge the Codex and Claude Code manifest files.

## Implementation notes

- Keep `plugins/golang-development/skills/` as the only canonical skill source.
- Codex must continue to use `.agents/plugins/marketplace.json` and `.codex-plugin/plugin.json`.
- Claude Code must continue to use `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`.
- Use `strict: true` or omit `strict` in the Claude marketplace.
- Keep every marketplace source inside the repository and relative to the marketplace root.
- Determine the canonical GitHub URL from the real remote at implementation time. If the user changes it from `Zate/golang-development` to `Zate/golang-skill`, update all public metadata in one change.

## Acceptance criteria

- Both marketplace files resolve `plugins/golang-development` from the repository root.
- The Codex manifest exposes all eight skills from `./skills/`.
- The Claude Code manifest exposes all eight skills from `./skills/`.
- The Claude marketplace does not use the documented invalid `strict: false` and component-manifest combination.
- Plugin and marketplace versions agree.
- Names and source paths support local repository installation and an `owner/repo` GitHub marketplace source.
- Both Claude Code strict validation commands pass.

## Definition of done

- Acceptance criteria are met.
- Focused checks cover all four manifests.
- Required verification commands pass.
- Status is changed to `complete`.
- `goals/index.md` marks this goal complete.
- The work is committed in one focused commit.

## Verification

- `claude plugin validate . --strict`
- `claude plugin validate ./plugins/golang-development --strict`
- Parse all four JSON files with a standard JSON parser.
- Confirm that both marketplace source paths resolve to `plugins/golang-development`.

## Completion notes

- Verification: Both Claude Code strict validators passed. Direct JSON checks confirmed matching paths, versions, repositories, and eight skills.
- Follow-ups: G08 will prove installation from the published GitHub source.
