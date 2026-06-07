---
name: golang-testing
description: Add, repair, design, or audit Go tests using the standard testing package, table-driven tests, subtests, examples, benchmarks, fuzz tests, race checks, coverage, fakes, and integration-test boundaries. Use when testing Golang code, creating test plans, debugging failing go test output, deciding unit vs integration coverage, reviewing test quality, finding missing coverage, or assessing whether existing tests prove behavior.
---

# Go Testing

## Build Workflow

1. Inspect existing `_test.go` files and match local assertion, fake, fixture, and package style.
2. Prefer standard `testing` tools first: table tests, subtests, `t.Helper`, `t.Cleanup`, `t.TempDir`, `httptest`, `iotest`, `fstest`, benchmarks, and fuzz tests.
3. Add tests at the lowest useful boundary. Use integration tests only when behavior depends on external systems or wiring.
4. Test public behavior, edge cases, error classification, cancellation/timeouts, and concurrency safety where relevant.
5. Use fakes/stubs over broad mocks when interfaces are small. Avoid generating mocks for interfaces that do not exist yet.
6. Run focused tests first, then `go test ./...`. Use `-race` for concurrency/shared-memory changes.
7. Keep tests deterministic: no real time sleeps without control, no network unless explicitly integration-gated, no order dependence.

## Audit Workflow

1. Inspect changed or target code and nearby `_test.go` files before judging coverage.
2. Check whether tests cover public behavior, edge cases, error classification, cancellation/timeouts, concurrency safety, and integration boundaries.
3. Flag brittle tests: sleeps, real network, order dependence, shared state, broad mocks, hidden fixtures, or over-testing internals.
4. Recommend the smallest useful test additions and whether they should be unit, integration, fuzz, benchmark, or race checks.
5. Pair with `golang-code-audit` when producing a full findings-first review.

## Load References

- Read `references/testing.md` for table, fuzz, benchmark, race, coverage, and integration-test patterns.
- Pair with the companion `golang-architecture-patterns` skill when introducing seams for fakes or contract tests.
