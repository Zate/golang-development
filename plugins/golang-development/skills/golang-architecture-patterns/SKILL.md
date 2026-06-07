---
name: golang-architecture-patterns
description: Design or audit Go application architecture, package boundaries, dependency direction, interfaces, adapters, repositories, services, HTTP handlers, concurrency boundaries, and maintainable design patterns. Use for Golang service design, refactors, domain layering, dependency injection, ports/adapters, repository patterns, functional options, API design, concurrency architecture, or reviewing existing Go architecture for coupling and maintainability risks.
---

# Go Architecture Patterns

## Build Workflow

1. Let the existing repo architecture lead. Preserve established package naming, dependency injection, and test style unless there is a concrete problem.
2. Design boundaries around behavior and data ownership, not pattern names.
3. Accept interfaces at the consumer boundary. Return concrete types unless hiding implementation is part of the API.
4. Keep interfaces small. Prefer `io.Reader`-style capability interfaces over broad service interfaces.
5. Keep domain/service packages independent of transport, database, CLI, logging, and framework details.
6. Keep concurrency out of APIs when possible. Expose synchronous functions; let callers decide whether to run them in goroutines.
7. Introduce repositories, ports/adapters, or functional options only when they remove real coupling or constructor complexity.
8. Document tradeoffs in plans: dependency direction, concrete vs interface boundaries, test fakes, and simpler alternatives.

## Audit Workflow

1. Trace dependency direction across packages before judging architecture.
2. Flag transport, database, framework, logging, or CLI details leaking into domain/service packages when they make testing or reuse harder.
3. Check interfaces for consumer ownership, size, needless abstraction, and pointer-to-interface mistakes.
4. Check concurrency APIs for hidden goroutines, cancellation gaps, shared-state races, channel leaks, and shutdown ambiguity.
5. Report findings with the simpler alternative, not just the pattern name.
6. Pair with `golang-code-audit` when producing a full findings-first review.

## Load References

- Read `references/patterns.md` when choosing simple packages, layered services, ports/adapters, repository, functional options, or concurrency patterns.
- Pair with the companion `golang-planning-layout` skill for folder/module layout changes.
- Pair with the companion `golang-testing` skill when architecture choices affect fakes, integration tests, or contract tests.
