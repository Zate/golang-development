# Marketplace validation evidence

This file records repeatable marketplace smoke tests. The tests use isolated host configuration directories. They do not use the normal Codex or Claude Code profiles.

## Local marketplace smoke test

- Date: 2026-08-10
- Source commit: `96ad257`
- Plugin version: `0.1.0`
- Operating system: Windows
- Codex CLI: `0.146.0`
- Claude Code: `2.1.225`
- Marketplace: `golang-development-marketplace`
- Plugin: `golang-development`

### Isolation

- Codex used a new temporary `CODEX_HOME`.
- Claude Code used a new temporary `CLAUDE_CONFIG_DIR`.
- Claude Code plugin storage used `CLAUDE_CODE_PLUGIN_CACHE_DIR` under the same temporary root.
- The test compared normal Codex and Claude Code configuration and plugin-state signatures before and after installation.
- The temporary root was removed after the test.

### Commands

The test used the repository root as `<repo-root>` and new directories under `<temporary-root>`:

```powershell
$env:CODEX_HOME = '<temporary-root>\codex'
codex plugin marketplace add '<repo-root>' --json
codex plugin add golang-development@golang-development-marketplace --json
codex plugin list --marketplace golang-development-marketplace --json

$env:CLAUDE_CONFIG_DIR = '<temporary-root>\claude'
$env:CLAUDE_CODE_PLUGIN_CACHE_DIR = '<temporary-root>\claude\plugins'
claude plugin marketplace add '<repo-root>'
claude plugin install golang-development@golang-development-marketplace
claude plugin details golang-development@golang-development-marketplace
```

### Results

- Codex added the marketplace and installed an enabled plugin at version `0.1.0`.
- The Codex installed package contained eight valid skill directories.
- Claude Code added the marketplace and installed the plugin at user scope inside the isolated configuration.
- Claude Code component details listed the same eight skills.
- Normal host profile changes: `0`.
- A Codex warning said that it would not create PATH aliases under a temporary directory. Plugin installation and inventory checks still passed.

The eight registered skills were:

1. `golang-architecture-patterns`
2. `golang-build-deploy`
3. `golang-code-audit`
4. `golang-development-workflow`
5. `golang-implementation-idioms`
6. `golang-planning-layout`
7. `golang-quality-linting`
8. `golang-testing`

## GitHub marketplace smoke test

G08 will add the published GitHub source, tested commit, commands, and results here.
