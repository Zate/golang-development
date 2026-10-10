---
name: golang-planning-layout
description: Plans Go file, package, module, and command organization. Use when splitting oversized files, choosing package boundaries, moving code, or planning layout migrations; preserve cohesive code and existing APIs.
license: MIT
---

# Go Planning And Layout

Follow the user's scope and repository instructions. Planning and layout reviews are read-only unless changes are requested.

## Workflow

1. Inspect the relevant package, its callers, tests, `go.mod`, and existing conventions. Inspect `go.work` and commands only when the proposed change affects them.
2. Prefer the smallest structure that solves the current problem. For navigation alone, move cohesive groups into focused files in the same package; do not create a package merely to reduce line count.
3. Create a package only for a distinct responsibility with clear ownership, a useful narrow API, and acyclic dependencies. Keep tightly coupled unexported types together.
4. Use `internal/` for non-public packages. Reserve public packages for intended external imports; use `cmd/<name>` for multiple commands or substantial binary support code.
5. Plan small, behavior-preserving moves, including build tags, callers, tests, and relevant repository verification commands. Report concrete cohesion/coupling consequences when reviewing layout.

## References

Read [repo-layout.md](references/repo-layout.md) for file-size review, file-versus-package decisions, module layout, or workspace changes. Use `golang-architecture-patterns` only when the decision requires interface, ownership, or dependency design beyond file organization.
