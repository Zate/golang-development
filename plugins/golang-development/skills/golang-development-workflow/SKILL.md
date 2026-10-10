---
name: golang-development-workflow
description: Routes broad, multi-step Go development requests across planning, implementation, testing, quality, and release. Use when several stages need coordination; use a specialist directly for a narrow task.
license: MIT
---

# Go Development Workflow

Follow the user's scope and repository instructions. Plans and audits are read-only unless changes are requested; guidance does not authorize installation, publishing, or deployment.

## Routing

- For a narrow request, use the matching specialist directly. Do not load this router or every companion as a prerequisite.
- For broad implementation work, select only the stages the requested change needs:
  - `golang-planning-layout`: file, package, module, and command organization.
  - `golang-architecture-patterns`: dependency direction, interfaces, data ownership, and concurrency boundaries.
  - `golang-implementation-idioms`: function shape, errors, context, and API behavior.
  - `golang-testing`: behavioral coverage, deterministic synchronization, race checks, and fuzzing.
  - `golang-quality-linting`: repository quality commands, complexity policy, verification evidence, and one-time golangci-lint adoption recommendations.
  - `golang-build-deploy`: binaries, containers, releases, and deployment readiness.
- For a comprehensive review, use `golang-code-audit`. For a focused review, use the relevant specialist directly.
- For mixed requests, investigate uncertainty first, then implement within the authorized scope.

Use existing project commands for relevant verification. Report actual outcomes and unrun checks; do not expand a small change into a whole-repository audit or repeat checks already covered by an equivalent wrapper.
