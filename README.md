# Golang Development

Golang Development is one shared bundle of eight Agent Skills for building and auditing Go projects. The repository supports three installation forms:

- A Codex plugin from a local or GitHub marketplace.
- A Claude Code plugin from a local or GitHub marketplace.
- Standard skill directories for agents that scan the cross-client `.agents/skills` convention.

The plugin provides two workflows:

- Build mode plans, implements, tests, checks, builds, and deploys Go changes.
- Audit mode reviews an existing repository, package, diff, service, or release path and reports findings first.

## Included Skills

- `golang-development-workflow`: Routes broad Go requests into build or audit mode.
- `golang-code-audit`: Provides a findings-first audit for existing Go code.
- `golang-planning-layout`: Covers modules, repositories, packages, and commands.
- `golang-architecture-patterns`: Covers boundaries, dependencies, interfaces, services, adapters, and concurrency.
- `golang-implementation-idioms`: Covers naming, errors, context, nil handling, generics, comments, and the standard library.
- `golang-testing`: Covers table tests, subtests, fuzzing, benchmarks, race checks, fakes, and integration boundaries.
- `golang-quality-linting`: Covers formatting, vetting, static analysis, golangci-lint, security checks, and completion gates.
- `golang-build-deploy`: Covers builds, releases, containers, CI/CD, runtime readiness, and deployment.

## Install In Codex From GitHub

Add the GitHub repository as a marketplace, then install the plugin:

```powershell
codex plugin marketplace add Zate/golang-development
codex plugin add golang-development@golang-development-marketplace
codex plugin list
```

Start a new Codex task after installation. This loads the new skill catalog.

Refresh or remove the GitHub marketplace with these commands:

```powershell
codex plugin marketplace upgrade golang-development-marketplace
codex plugin remove golang-development@golang-development-marketplace
codex plugin marketplace remove golang-development-marketplace
```

## Install In Codex From A Local Clone

Clone the repository, then add its root directory as the marketplace source:

```powershell
git clone https://github.com/Zate/golang-development.git
codex plugin marketplace add C:\path\to\golang-development
codex plugin add golang-development@golang-development-marketplace
codex plugin list
```

On macOS or Linux, use the local POSIX path instead:

```bash
codex plugin marketplace add /path/to/golang-development
codex plugin add golang-development@golang-development-marketplace
codex plugin list
```

## Install In Claude Code From GitHub

Add the same GitHub repository as a Claude Code marketplace, then install the plugin:

```powershell
claude plugin marketplace add Zate/golang-development
claude plugin install golang-development@golang-development-marketplace
claude plugin details golang-development@golang-development-marketplace
```

Refresh or remove the GitHub marketplace with these commands:

```powershell
claude plugin marketplace update golang-development-marketplace
claude plugin uninstall golang-development@golang-development-marketplace
claude plugin marketplace remove golang-development-marketplace
```

Use `/reload-plugins` in a running Claude Code session after you change a local plugin. A new installation is available in the next session.

## Install In Claude Code From A Local Clone

Clone the repository, then add its root directory as the marketplace source:

```powershell
git clone https://github.com/Zate/golang-development.git
claude plugin marketplace add C:\path\to\golang-development
claude plugin install golang-development@golang-development-marketplace
claude plugin details golang-development@golang-development-marketplace
```

On macOS or Linux, use the local POSIX path instead:

```bash
claude plugin marketplace add /path/to/golang-development
claude plugin install golang-development@golang-development-marketplace
claude plugin details golang-development@golang-development-marketplace
```

## Install For Generic Agent Skills Clients

The installer copies the eight canonical skill directories. It does not copy or create a generic plugin marketplace. Generic Agent Skills clients use the skill directories directly.

The default target is the user-level `~/.agents/skills` directory. Check the exact targets first:

```powershell
python scripts\install_agent_skills.py --dry-run
python scripts\install_agent_skills.py
```

On macOS or Linux:

```bash
python3 scripts/install_agent_skills.py --dry-run
python3 scripts/install_agent_skills.py
```

Use `--target` for a project-level installation:

```powershell
python scripts\install_agent_skills.py --target C:\path\to\project\.agents\skills
```

```bash
python3 scripts/install_agent_skills.py --target /path/to/project/.agents/skills
```

The installer stops before it writes files if any target skill name already exists. It never overwrites an installed skill.

## Invoke Skills

Codex uses `$` skill mentions. For example:

```text
$golang-testing Add tests for this Go package.
```

Claude Code namespaces skills that come from plugins. For example:

```text
/golang-development:golang-testing Add tests for this Go package.
```

Generic clients can activate a skill automatically from its description or use the invocation form that the client provides.

The `agents/openai.yaml` file in each skill contains optional OpenAI interface metadata. It does not change the standard `SKILL.md` format. Claude Code and generic clients can ignore it.

## Usage Examples

Build-oriented prompts:

```text
Build this Go feature idiomatically and add the right tests.
Refactor this package while preserving the existing Go architecture.
Prepare this Go service for release and deployment.
```

Audit-oriented prompts:

```text
Audit this Go repository against idiomatic Go architecture, testing, and quality guidance.
Review this Go diff for correctness, maintainability, and release readiness.
Find places where this service does not follow the Golang Development guidance.
```

## Repository Layout

```text
.agents/plugins/marketplace.json                    Codex marketplace manifest
.claude-plugin/marketplace.json                     Claude Code marketplace manifest
plugins/golang-development/                         Shared plugin root
plugins/golang-development/.codex-plugin/plugin.json
plugins/golang-development/.claude-plugin/plugin.json
plugins/golang-development/skills/                  Canonical Agent Skills
scripts/install_agent_skills.py                     Safe generic installer
scripts/validate_release.py                         Offline release validator
scripts/validate_skills_ref.py                      Official skills-ref runner
tests/                                               Installer and release tests
.github/workflows/validate.yml                       Windows and Ubuntu CI gates
```

## Validate A Release

Run the repository-owned offline checks:

```powershell
python scripts\validate_release.py
python -m unittest discover -s tests -v
claude plugin validate . --strict
claude plugin validate .\plugins\golang-development --strict
```

The CI workflow also installs `skills-ref` from a pinned commit in the official Agent Skills repository, then runs:

```powershell
python scripts\validate_skills_ref.py
```

The release validator checks both marketplaces, both plugin manifests, version and repository consistency, skill metadata, references, and OpenAI interface metadata.

## License

MIT
