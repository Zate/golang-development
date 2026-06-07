---
name: golang-code-audit
description: Audit existing Go and Golang codebases, pull requests, diffs, packages, services, CLIs, tests, build pipelines, and repository layouts against idiomatic Go development guidance. Use when reviewing, auditing, assessing, evaluating, inspecting, checking best-practice compliance, finding violations, identifying risks, or producing findings for already-built Go code.
---

# Go Code Audit

## Workflow

1. Determine the audit scope: whole repo, diff, package, command, service, tests, CI/build, or release path.
2. Inspect `go.mod`, `go.work`, package layout, relevant source files, tests, build scripts, and configured quality commands before judging.
3. Select companion skills by risk area:
   - `golang-planning-layout` for module layout, package boundaries, command structure, and naming.
   - `golang-architecture-patterns` for dependency direction, interfaces, services, adapters, repositories, APIs, and concurrency boundaries.
   - `golang-implementation-idioms` for naming, errors, context, nil handling, generics, comments, and standard library usage.
   - `golang-testing` for coverage gaps, test boundaries, fakes, determinism, benchmarks, fuzzing, and race checks.
   - `golang-quality-linting` for format, vet, static analysis, security, linter configuration, and completion gates.
   - `golang-build-deploy` for release, packaging, Docker, CI, runtime config, graceful shutdown, and deployment readiness.
4. Run or request the narrowest verification commands that are safe and relevant. If a command cannot be run, state that as residual risk.
5. Produce findings first, ordered by severity, with file and line references when possible.
6. Separate correctness, security, race/leak, API breakage, test gaps, maintainability, and style findings.
7. Do not include broad rewrites, unrelated refactors, or stylistic preferences unless they materially affect maintainability or match the requested audit scope.

## Output Shape

- Start with findings. If none, say no issues found.
- For each finding include severity, location, concrete risk, and the smallest useful remediation.
- Add open questions or assumptions only after findings.
- End with verification performed and remaining test or inspection gaps.
