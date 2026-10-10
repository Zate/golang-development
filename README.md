# Golang Development

Golang Development is one shared bundle of eight Agent Skills for building and auditing Go projects. The repository supports three installation forms:

- A Codex plugin from a local or GitHub marketplace.
- A Claude Code plugin from a local or GitHub marketplace.
- Standard skill directories for agents that scan the cross-client `.agents/skills` convention.

The plugin provides two workflows:

- Implementation mode selects the planning, coding, testing, quality, and release stages the request needs. Publishing and deployment require task authorization.
- Audit and planning modes inspect the requested scope and report findings or a plan without editing files.

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

Use a specialist directly for a narrow task. The workflow skill coordinates broad requests; it is not a prerequisite for every specialist. Skill descriptions support automatic discovery, while explicit invocation makes your intent clear. Avoid installing the same bundle as both a plugin and generic skills in the same host/project.

The `agents/openai.yaml` file in each skill contains optional OpenAI interface metadata. It does not change the standard `SKILL.md` format. Claude Code and generic clients can ignore it.

## Usage Examples

Build-oriented prompts:

```text
Build this Go feature idiomatically and add the right tests.
Refactor this package while preserving the existing Go architecture.
Plan release readiness for this Go service using its existing build wrappers; do not deploy.
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
scripts/validate_lint_config.py                     Pinned real-tool lint fixtures
scripts/run_skill_evals.py                          Isolated host behavioral evaluations
evals/cases.json                                   Shared behavioral cases and rubrics
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

The release validator checks both marketplaces, both plugin manifests, version and repository consistency, the eight canonical skills, references, OpenAI interface metadata, and byte-for-byte parity of the two lint templates. Claude's strict validation covers manifests; the official `skills-ref` validator checks skill format.

With Go and the pinned **golangci-lint 2.14.0** binary already available, also run:

```bash
python3 scripts/validate_lint_config.py --lint /path/to/golangci-lint
```

This verifies both schemas and 20 disposable behavioral fixtures. CI includes that check with Go 1.27.2 and a checksum-pinned Linux binary. It does not install anything into an application module.

## Recommended Quality Policy

Keep existing repository checks and tool versions unless configuration adoption is requested. The template accepts cyclomatic complexity 15, cognitive complexity 20, 80 counted function body lines, and 50 AST statements; larger values report findings. Function line counting explicitly ignores comment tokens and counts blank lines. See the [quality reference](plugins/golang-development/skills/golang-quality-linting/references/linting.md) for exact counting, generated/test exclusions, and justified suppressions.

When a quality review establishes that golangci-lint is missing or unused, the skill raises this and recommends installing/enabling it with the bundled configuration, adapted to existing checks. Adoption remains optional. It honors a prior refusal without repeating the suggestion or making adoption a completion requirement; installation and configuration changes still require authorization.

More than 800 physical lines in handwritten production Go is an advisory cohesion/navigation review, not a failing gate or an automatic package split. Inventory existing debt and compare complete touched functions at base and head with the same tools/configuration. Changed-line-only filtering can miss a body regression reported on an unchanged declaration line.

## Behavioral And Token Evaluation

Run shared cases in disposable workspaces with an authenticated host CLI. These use model calls and account usage; they do not install the plugin globally or publish reports.

```bash
python3 scripts/run_skill_evals.py --host claude --plugin plugins/golang-development --runs 3 --output /tmp/go-claude-eval
python3 scripts/run_skill_evals.py --host codex --plugin plugins/golang-development --runs 3 --output /tmp/go-codex-eval
python3 scripts/run_skill_evals.py --host codex --runs 3 --output /tmp/go-codex-no-plugin
```

Each output directory must be new. Use repeated `--case <name>` options for a bounded subset, `--model <host-model>` to hold the model fixed, and `--keep-temp` when native Claude traces are needed for token/tool inspection. Claude runs its native outcome graders and a no-plugin arm; skill activation is a separate indicator, not evidence of accuracy. Codex records JSONL traces and usage/read metrics for manual review against the same rubrics. Use the same host/model and prompts for before/after comparisons. Confirm changes with repeated runs; inspect judge failures and do not infer quality from activation alone.

Evaluate outcome accuracy, read-only scope, skill/reference loading, input/output/cache tokens, tool calls, and elapsed time separately. Trivial correct answers may appropriately skip automatic skill invocation. Native catalog estimates exclude references and are not measured end-to-end savings. See [validation evidence](docs/validation.md) for current results and limits.

## License

MIT
