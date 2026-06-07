---
name: golang-build-deploy
description: Build, package, release, containerize, deploy, or audit Go applications and CLIs. Use for Golang build flags, module release checks, cross-compilation, Dockerfiles, CI/CD, version metadata, graceful shutdown, runtime configuration, security updates, production deployment plans, or reviewing existing Go release/deployment readiness.
---

# Go Build And Deploy

## Build Workflow

1. Inspect existing build/release surfaces first: `Makefile`, CI workflows, Dockerfiles, `goreleaser`, task files, `go.mod`, and deployment manifests.
2. Build with the standard go tool unless the repo has a stronger wrapper. Prefer reproducible commands over hidden local state.
3. Keep build metadata explicit: version, commit, date, dirty state, target OS/arch, and module dependency info where useful.
4. For services, verify graceful shutdown, context propagation, health/readiness checks, config loading, logging, and metrics/tracing hooks already used by the repo.
5. For containers, prefer small multi-stage builds, non-root runtime users, CA certificates/timezone needs, and no source/toolchain in final image.
6. Before release/deploy, run tests, vet/lint, vulnerability checks when available, and a local smoke test of the built binary.

## Audit Workflow

1. Inspect build scripts, CI, Dockerfiles, release config, runtime config, service startup/shutdown, and deployment manifests before judging.
2. Check reproducibility, version metadata, module hygiene, vulnerability scanning, container runtime user, image contents, and smoke-test coverage.
3. For services, flag missing graceful shutdown, HTTP timeouts, health/readiness checks, config validation, logging, metrics/tracing, or secret leakage.
4. Report release blockers separately from hardening recommendations.
5. Pair with `golang-code-audit` when producing a full findings-first review.

## Load References

- Read `references/build-release-deploy.md` for command patterns, Dockerfile shape, CI gates, and deployment checklist.
- Pair with the companion `golang-quality-linting` skill for verification and the companion `golang-testing` skill for release test strategy.
