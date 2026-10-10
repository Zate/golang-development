---
name: golang-build-deploy
description: Plans or verifies Go builds, containers, releases, and service runtime readiness. Use for build flags, supported toolchains, packaging, CI release gates, or deployment preparation; preserve repository wrappers.
license: MIT
---

# Go Build And Deploy

Follow the user's scope and repository instructions. Release plans and reviews are read-only unless changes are requested. Preparing a release does not authorize publishing, pushing, or deploying it.

## Workflow

1. Inspect the relevant build/release wrappers, toolchain requirements, CI, and runtime surfaces. Preserve working dependency and packaging conventions.
2. Select a supported Go toolchain compatible with the project and pin repeatable build/tool versions. Review intentional module changes rather than automatically running `go mod tidy`.
3. Build with existing commands. Keep useful version/commit/target metadata explicit; for containers prefer multi-stage builds and a non-root runtime compatible with CGO and OS requirements.
4. For service readiness, verify applicable config validation, timeouts, shutdown, health checks, and existing observability. Report missing features only when their absence creates a concrete deployment risk.
5. Before an authorized release, run relevant quality/security checks, build targets, and smoke tests. State what was executed and what remains unverified; keep release blockers separate from optional hardening.

## References

Read [build-release-deploy.md](references/build-release-deploy.md) for supported-version selection, command examples, containers, or release checks. Load quality/linting or testing companions only when gate selection or test coverage needs clarification.
