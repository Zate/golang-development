---
name: golang-quality-linting
description: Verify, improve, or audit Go code quality with gofmt, goimports, go vet, static analysis, golangci-lint, security checks, code review, lint configuration, and completion verification. Use when reviewing Golang changes, fixing linter failures, setting up golangci-lint, deciding quality gates, auditing existing quality practices, or checking whether Go code is ready to ship.
---

# Go Quality And Linting

## Build Workflow

1. Prefer the repo's existing quality commands from `Makefile`, CI, `golangci.yaml`, `golangci.yml`, or task files.
2. Always format before deeper analysis: `gofmt` and import sorting (`goimports` when available).
3. Run `go test ./...` and `go vet ./...` unless the repo has a stronger equivalent.
4. Use `golangci-lint run` when configured or requested. Treat linter suppressions as code review items; require specific `//nolint:<linter> // reason`.
5. For security-sensitive code, add `govulncheck`, fuzzing, or `gosec` when available and relevant.
6. When reviewing, lead with correctness, race/leak risk, API breakage, missing tests, and security. Style-only findings come last.
7. Do not claim success until verification commands have been run and outputs are known.

## Audit Workflow

1. Inspect configured quality commands and CI before recommending new tools.
2. Check whether format, tests, vet, lint, vulnerability scans, race checks, and generated-code exclusions match the repo's risk profile.
3. Treat `//nolint` suppressions, unchecked errors, security findings, and missing verification as review findings.
4. Report commands run, commands not run, and residual risk separately.
5. Pair with `golang-code-audit` when producing a full findings-first review.

## Load References

- Read `references/linting.md` when configuring or fixing lint/vet/staticcheck/golangci-lint.
- Read `references/golangci-recommended.yaml` when creating a new strict but practical golangci-lint config.
