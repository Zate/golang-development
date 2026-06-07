# Golang Development

Golang Development is a public marketplace-style plugin containing Codex and Claude skills for building and auditing Go projects.

The plugin is designed for two native agent workflows:

- Build mode: plan, implement, test, lint, build, and deploy Go changes idiomatically.
- Audit mode: review an existing repo, package, diff, service, or release path against the same guidance and report findings first.

## Included Skills

- `golang-development-workflow`: routes broad Go requests into build or audit mode.
- `golang-code-audit`: findings-first audit workflow for existing Go code.
- `golang-planning-layout`: module, repo, package, and command layout.
- `golang-architecture-patterns`: boundaries, dependencies, interfaces, services, adapters, and concurrency.
- `golang-implementation-idioms`: naming, errors, context, nil handling, generics, comments, and standard library use.
- `golang-testing`: table tests, subtests, fuzzing, benchmarks, race checks, fakes, and integration boundaries.
- `golang-quality-linting`: formatting, vetting, static analysis, golangci-lint, security checks, and quality gates.
- `golang-build-deploy`: build flags, cross-compilation, containers, CI/CD, release metadata, and runtime readiness.

## Codex Install

Add this repository as a marketplace, then install the plugin:

```powershell
codex plugin marketplace add Zate/golang-development
codex plugin add golang-development@golang-development-marketplace
```

For local development from a checked-out copy:

```powershell
codex plugin marketplace add C:\path\to\golang-development
codex plugin add golang-development@golang-development-marketplace
```

Start a new Codex thread after installing or reinstalling so the skill metadata is loaded into the session.

## Claude Install

This repository also includes Claude plugin metadata under `.claude-plugin/`. Add the repository as a Claude plugin marketplace using the Claude Code plugin workflow, then enable `golang-development`.

## Usage Examples

Build-oriented prompts:

```text
Build this Go feature idiomatically and add the right tests.
Refactor this package while preserving the existing Go architecture.
Prepare this Go service for release and deployment.
```

Audit-oriented prompts:

```text
Audit this Go repo against idiomatic Go architecture, testing, and quality guidance.
Review this Go diff for correctness, maintainability, and release readiness.
Find places where this service does not follow the Golang Development guidance.
```

## Repository Layout

```text
.agents/plugins/marketplace.json       Codex marketplace manifest
.claude-plugin/marketplace.json        Claude marketplace manifest
plugins/golang-development/            Plugin root
plugins/golang-development/skills/     Skill definitions and references
```

## Validation

The plugin has been validated locally with:

```powershell
python <plugin-creator>/scripts/validate_plugin.py plugins\golang-development
claude plugin validate . --strict
golangci-lint config verify --config plugins\golang-development\golangci.yaml
```

## License

MIT
