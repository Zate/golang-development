---
name: golang-development-workflow
description: Route Go and Golang development work into the right build or audit workflow. Use for broad Go tasks such as building features, implementing changes, refactoring, planning, reviewing, auditing, assessing an existing codebase, checking against Go best practices, or deciding which Golang Development skills apply.
license: MIT
---

# Go Development Workflow

## Workflow

1. Inspect the user's wording and current repo context before choosing a mode.
2. Use build mode when the user asks to create, implement, modify, refactor, fix, migrate, configure, test, release, or deploy Go code.
3. Use audit mode when the user asks to review, audit, assess, evaluate, inspect, check, compare against guidance, find violations, identify gaps, or report risks in existing Go code.
4. For mixed requests, audit first when risk is unclear, then implement only the fixes the user requested.
5. Load the narrow companion skills needed for the task instead of loading every Go skill.

## Build Mode

- Start with `golang-planning-layout` for module layout, package boundaries, command placement, migrations, or multi-step plans.
- Use `golang-architecture-patterns` for service boundaries, dependency direction, interfaces, adapters, repositories, APIs, or concurrency architecture.
- Use `golang-implementation-idioms` while writing or refactoring Go code.
- Use `golang-testing` when adding, repairing, or planning tests.
- Use `golang-quality-linting` before claiming the implementation is complete.
- Use `golang-build-deploy` for release, packaging, Docker, CI, runtime, or deployment work.

## Audit Mode

- Prefer `golang-code-audit` as the primary audit workflow.
- Pair audit work with the topic skill that matches the risk under review: planning/layout, architecture, implementation idioms, testing, quality/linting, or build/deploy.
- Report findings before summaries. Include file and line references when available.
- Do not rewrite code during an audit unless the user explicitly asks for fixes.
