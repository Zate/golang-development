# Golang Development quality improvement handoff

Prepared for the next coding agent on 10 October 2026.

Improve this plugin's guidance for maintainable Go code, particularly complex
functions and oversized files. Preserve the existing eight-skill structure and
Codex, Claude Code, and generic Agent Skills compatibility. Make contained changes
to the existing skills, references, recommended configuration, and validation.

## Context and scope

The user is concerned about long, complex Go files and wants actionable guidance
and automated checks. Research found that their own plugin is already public at
[Zate/golang-development](https://github.com/Zate/golang-development), but it was
not installed in the Codex environment used for the research.

The motivating project, Nyx, currently uses pinned Staticcheck, go vet, and gofmt;
it has no configured complexity or length limits. Its production files included
codex.go at 1,782 lines and service.go at 1,645 lines. Those counts indicate places
to inspect; they do not prove complexity. This task concerns the plugin, not Nyx.

Before editing, inspect this checkout's instructions, working tree, skills,
references, manifests, tests, and validation scripts. Preserve existing changes.
Briefly identify the exact change points and implementation plan. Do not install
the plugin globally, modify other repositories, commit, push, or publish unless
the user explicitly requests that action in the new session.

## Verified starting point

The local checkout was clean at commit
`b433e9c03937d54de059dcdc334ce1c687ae2fc5` dated 10 August 2026. Its eight skills are:

- golang-development-workflow
- golang-code-audit
- golang-planning-layout
- golang-architecture-patterns
- golang-implementation-idioms
- golang-testing
- golang-quality-linting
- golang-build-deploy

Native plugin manifests and a safe generic skill installer exist. The latest
[hosted validation run](https://github.com/Zate/golang-development/actions/runs/31356494622)
passed. Existing installation evidence in docs/validation.md is historical:
isolated Windows tests with Codex CLI 0.146.0 and Claude Code 2.1.225. Preserve it;
do not treat it as current macOS acceptance.

## Exact improvement points

| Existing file | Work needed |
| --- | --- |
| plugins/golang-development/skills/golang-quality-linting/SKILL.md | Clarify required checks, adoption behavior, exceptions, and reporting. |
| plugins/golang-development/skills/golang-quality-linting/references/linting.md | Explain complexity measures, function size, incremental adoption, version pinning, and config validation. |
| plugins/golang-development/golangci.yaml | Add selected, justified complexity and function-size checks. |
| plugins/golang-development/skills/golang-quality-linting/references/golangci-recommended.yaml | Keep consistent with the plugin-level configuration; these files currently match. |
| plugins/golang-development/skills/golang-planning-layout and golang-architecture-patterns | Add explicit file-versus-package splitting criteria and cohesion guidance in their existing references. |
| plugins/golang-development/skills/golang-implementation-idioms/references/idioms.md | Connect function extraction to readable responsibilities rather than line-count gaming. |
| plugins/golang-development/skills/golang-build-deploy/references/build-release-deploy.md | Refresh the Go 1.24 Docker example and supported-toolchain guidance. |
| README.md, docs/validation.md, tests, and validation scripts | Document the resulting policy and add only focused verification where needed. |

## Complexity and size policy

The recommended golangci-lint configuration already uses version 2 and enables
gocyclo with min-complexity 15. It does not enable gocognit or funlen, and there is
no explicit file-size policy. The quality skill currently says to use
golangci-lint when configured or requested; it does not mandate installing or
adding it to every existing repository.

These are proposed starting settings, not official Go standards. Evaluate them
against representative examples, explain any adjustment, and document exact
threshold semantics for the selected linter version.

| Concern | Proposed starting policy |
| --- | --- |
| Cyclomatic complexity | Retain gocyclo min-complexity 15. |
| Cognitive complexity | Add gocognit min-complexity 20 to highlight nesting and difficult control flow. Explain the overlap with cyclomatic checks. |
| Function size | Add funlen with 80 lines and 50 statements; document comment counting. |
| File size | Advisory review above 800 physical lines for handwritten production Go files. Exclude generated files and tests from this initial signal; review tests separately when their structure becomes difficult to maintain. |

File length is a navigation and cohesion signal. A long cohesive declaration
table may be reasonable; a shorter function with nested state transitions may
need attention. Do not force arbitrary file splitting or create extra packages
just to satisfy a number. Prefer moving cohesive groups into focused files in
the same package when only navigation is the problem.

Give explicit guidance for choosing a new package: a distinct responsibility,
clear ownership, a useful narrow API, and a sensible dependency direction.
Keep tightly coupled types together when separation would expose implementation
details or require callers to import both packages to use either.

## Adoption and maintainability guidance

- Start existing repositories with an inventory of findings. Keep existing
  quality checks working and prevent new violations or worsening complexity
  without demanding an immediate whole-repository refactor.
- Explain that filtering only changed lines can miss a complex function whose
  changed body is elsewhere than the reported location. Do not promise complete
  regression prevention unless the selected mechanism actually provides it.
- Distinguish advisories from failing gates. Provide a practical adoption path
  and documented exceptions without a blanket suppression policy.
- Suppressions should identify the specific linter and explain the reason.
  Verify that nolintlint settings enforce the intended requirements.
- Prefer early error returns, explicit data flow, focused helpers, small
  consumer-owned interfaces, and synchronous APIs where practical.
- Make goroutine exit, cancellation, shared-state ownership, channel closure,
  and completion responsibilities explicit.
- Preserve stable error contracts. Wrapping an implementation error with %w
  exposes it to callers; do so deliberately. Avoid duplicate error logging.
- Keep tests behavioral and deterministic. Use controlled synchronization/time,
  stable result comparisons, focused race checks, and fuzzing where useful.
- Avoid speculative abstractions, dependencies, generic utility packages, and
  optimization without evidence. Preserve useful nil-slice behavior and API
  compatibility rather than imposing universal serialization rules.

## Tool freshness and compatibility

Refresh installation examples against the official golangci-lint documentation.
Version 2 source installation uses the /v2/ module path. The maintainers recommend
binary installation and caution against adding the tool's dependencies directly
to an application's module. Pin repeatable tool and CI versions and check their
compatibility with the target Go version.

As researched on 10 October 2026, Go 1.26 and 1.27 were the supported release
series. Recheck the release policy before choosing a replacement Docker example.
Teach supported-version selection rather than leaving an unexplained stale pin.

Preserve existing repository wrappers and dependency conventions. Do not imply
that an agent should install tools or override project policy without authority.

## External references and cautions

Use primary sources to settle behavior and configuration:

- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments): function shape, interfaces, contexts, goroutine lifetimes, and nil slices.
- [Google Go package and file size guidance](https://google.github.io/styleguide/go/best-practices#package-size): avoid enormous files and excessive tiny files; no one-type-per-file convention.
- [Go module layout](https://go.dev/doc/modules/layout) and [package names](https://go.dev/blog/package-names): cohesion, internal packages, and naming.
- [Errors as API contracts](https://go.dev/blog/go1.13-errors).
- [Go testing guidance](https://go.dev/wiki/TestComments) and [testing asynchronous behavior](https://go.dev/blog/testing-time).
- [golangci-lint settings](https://golangci-lint.run/docs/linters/configuration/) and [installation](https://golangci-lint.run/docs/welcome/install/local/).
- [Go release history and policy](https://go.dev/doc/devel/release).

Useful community comparisons, to review selectively:

- [Samber's lint configuration](https://github.com/samber/cc-skills-golang/blob/main/skills/golang-lint/assets/.golangci.yml): gocyclo 13, funlen 120 lines/80 statements, and nestif; explicitly disables gocognit. Its lint skill still had an old installation path, and its style skill universally forbade nil slices, conflicting with official general guidance. Do not import the entire bundle's rules or automatic parallel autofix behavior.
- [Netresearch's lint reference](https://github.com/netresearch/go-development-skill/blob/main/skills/go-development/references/linting.md): gocyclo 15, gocognit 30, funlen 80 lines/50 statements, and nestif. It mixed a v2 configuration with a v1.62 CI example. Check examples against current upstream documentation.
- [Jeffallan's golang-pro](https://github.com/Jeffallan/claude-skills/blob/main/skills/golang-pro/SKILL.md): compact general guidance, but no bundled complexity/length policy.

Recent repository activity alone does not prove the technical guidance is current.

## Verification and completion

Use the existing offline package validation and tests from the repository root:

```bash
python3 scripts/validate_release.py
python3 -m unittest discover -s tests -v
python3 scripts/install_agent_skills.py --dry-run --target /private/tmp/golang-development-skills-preview
```

With an appropriate golangci-lint v2 binary available, verify both configurations:

```bash
golangci-lint config verify --config plugins/golang-development/golangci.yaml
golangci-lint config verify --config plugins/golang-development/skills/golang-quality-linting/references/golangci-recommended.yaml
cmp plugins/golang-development/golangci.yaml plugins/golang-development/skills/golang-quality-linting/references/golangci-recommended.yaml
```

Schema validation alone does not prove thresholds work. Use disposable small Go
fixtures to verify an ordinary function passes, intended complexity/size cases
are reported, and documented exclusions and justified suppressions behave as
claimed. Avoid broad implementation-mirroring tests or installing tools merely
to check Markdown. Run official skill validation or isolated installation smoke
tests when relevant prerequisites and authorization are present; report unavailable
checks separately. Do not change the user's normal agent configuration to test
installation.

Finish with the changed files, final policy and thresholds, verification commands
and outcomes, any residual limitations, and the next installation/release step.
Keep historical evidence dated. Do not claim the plugin is installed, published,
or fully verified on a host that was not tested.
