---
name: golang-testing
description: Designs, adds, or reviews Go behavioral tests. Use for coverage gaps, deterministic asynchronous tests, cancellation, race checks, fuzzing, or benchmarks; match existing test tools and boundaries.
license: MIT
---

# Go Testing

Follow the user's scope and repository instructions. Test plans and reviews are read-only unless test changes are requested.

## Workflow

1. Inspect the target behavior and nearby tests. Match existing assertions, fixtures, fakes, and package style; prefer standard `testing` tools when no convention exists.
2. Test observable success, failure, error classification, cancellation, and changed contracts at the lowest useful boundary. Do not mirror helpers or implementation details simply to add coverage.
3. Use controlled synchronization/time and stable comparisons. Avoid elapsed sleeps, order dependence, shared mutable fixtures, and external services in unit tests.
4. Use small explicit fakes where useful; do not add mock frameworks or production interfaces solely to make a test convenient.
5. Run focused tests, then the repository's appropriate broader checks. Use focused `-race` checks for changed concurrency/shared state, fuzzing for suitable input boundaries, and benchmarks for evidence-backed performance questions.
6. When reviewing, explain what behavior remains unproven. Report tests actually run and any host, service, or tool limitations separately.

## References

Read [testing.md](references/testing.md) for behavioral assertions, deterministic worker tests, race/fuzz commands, or integration boundaries. Use `golang-architecture-patterns` only if production ownership or dependencies prevent meaningful tests.
