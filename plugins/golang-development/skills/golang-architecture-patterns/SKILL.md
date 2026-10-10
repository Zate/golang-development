---
name: golang-architecture-patterns
description: Designs or reviews Go dependency direction, interfaces, data ownership, and concurrency boundaries. Use for architectural decisions and coupling problems; use planning-layout for file and module organization.
license: MIT
---

# Go Architecture Patterns

Follow the user's scope and repository instructions. Architecture reviews and plans are read-only unless implementation is requested.

## Workflow

1. Trace the relevant dependency and data flow. Preserve established architecture unless there is a concrete coupling, testing, or ownership problem.
2. Define boundaries around behavior and ownership. Prefer small consumer-owned interfaces where substitution is useful; do not introduce interfaces or pattern folders speculatively.
3. Separate transport, persistence, framework, or logging details when doing so removes real coupling. These are design choices, not mandatory layers for every Go program.
4. Prefer synchronous APIs when callers can own concurrency. For necessary goroutines, identify who starts, cancels, waits, protects shared state, and closes channels.
5. Explain the narrow API, dependency direction, behavioral tests, and simpler alternative for a proposed boundary. Report concrete risks when reviewing; avoid pattern-name compliance findings.

## References

Read [patterns.md](references/patterns.md) when designing package ownership, adapters, interfaces, functional options, or concurrency lifetimes. Use `golang-planning-layout` only for an unresolved file/module layout question and `golang-testing` only for an unresolved behavioral test strategy.
