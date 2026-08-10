---
name: golang-planning-layout
description: Plan or audit idiomatic Go modules, repository layout, package boundaries, command structure, migration strategy, and implementation plans. Use when working on Go or Golang projects before adding packages, moving code, choosing cmd/internal/pkg layout, splitting modules, introducing workspaces, writing a multi-step implementation plan, or reviewing an existing repo for layout and package-boundary problems.
license: MIT
---

# Go Planning And Layout

## Build Workflow

1. Inspect `go.mod`, `go.work`, `cmd/`, `internal/`, package names, existing build scripts, and tests before proposing layout changes.
2. Prefer the smallest module/package structure that satisfies the current repo. Do not introduce architecture folders by default.
3. Keep packages cohesive around behavior and import boundaries. Split only when it reduces coupling, clarifies ownership, or creates a real reusable package.
4. Put binaries in `cmd/<name>` when there are multiple commands or substantial support code. A single small command can live at module root.
5. Put non-public implementation packages under `internal/`. Use ordinary importable packages only when external reuse is intended.
6. Keep names short, lowercase, and meaningful at the call site. Avoid stutter such as `user.UserService` when `user.Service` is clear.
7. Produce plans that include verification commands: usually `go test ./...`, `go vet ./...`, format/import sorting, and project-specific lint/build commands.

## Audit Workflow

1. Inspect `go.mod`, `go.work`, package tree, command layout, import boundaries, and test locations before judging.
2. Flag unnecessary modules, architecture folders, public packages, `pkg/` usage, or command placement only when they create real coupling or confusion.
3. Check whether package names are cohesive, short, lowercase, and clear at call sites.
4. Report findings with concrete boundary or layout consequences; avoid cosmetic restructuring advice.
5. Pair with `golang-code-audit` when producing a full findings-first review.

## Load References

- Read `references/repo-layout.md` when changing module layout, package boundaries, command placement, or workspace setup.
- Pair with the companion `golang-architecture-patterns` skill when the task involves service boundaries, dependency direction, ports/adapters, or domain layering.
- Pair with the companion `golang-testing` skill when the plan must include test strategy.
