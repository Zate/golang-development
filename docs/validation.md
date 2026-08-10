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

### Current published source

- Date: 2026-08-10
- Source: `Zate/golang-development`
- Default branch: `main`
- Tested commit: `15b90cbf047cb4a2855e1124845a1c23ef262793`
- Plugin version: `0.1.0`
- Codex CLI: `0.146.0`
- Claude Code: `2.1.225`
- Codex skills: `8`
- Claude Code skills: `8`
- Normal host profile changes: `0`

The test used new temporary `CODEX_HOME`, `CLAUDE_CONFIG_DIR`, and `CLAUDE_CODE_PLUGIN_CACHE_DIR` directories. Both hosts added the GitHub repository as a marketplace, installed `golang-development@golang-development-marketplace`, and loaded the same version and skill inventory from the same commit.

### Hosted validation

[GitHub Actions run 31356286623](https://github.com/Zate/golang-development/actions/runs/31356286623) passed on Windows and Ubuntu for the tested commit. Both jobs passed release validation, six unit tests, the generic installer dry-run, installation of the pinned official Agent Skills validator, and validation of all eight skills.
