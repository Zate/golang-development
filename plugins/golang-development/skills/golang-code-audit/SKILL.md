---
name: golang-code-audit
description: Reviews Go repositories or diffs for correctness, security, concurrency, API regressions, and maintainability. Use for comprehensive code audits; use specialist skills for focused lint, test, or architecture reviews.
license: MIT
---

# Go Code Audit

Follow the user's scope and repository instructions. Keep the audit read-only unless fixes are requested, including formatting and generated files.

## Workflow

1. Establish the target: repository, diff, package, service, or release path. Inspect relevant source, callers, tests, and configured checks; a small diff does not require a full repository map.
2. Trace actual behavior and ownership. Prioritize correctness, security, races/leaks, API compatibility, and missing behavioral coverage before maintainability or style.
3. Load a specialist only to resolve a concrete question: planning/layout for cohesion, architecture for dependency or concurrency boundaries, idioms for error/API behavior, testing for verification gaps, quality/linting for configured gates or missing golangci-lint recommendations, build/deploy for release readiness. Do not route back through `golang-development-workflow`.
4. Use relevant read-only checks when permitted. Inspect wrappers before running them; do not run installers, formatters that write, or unrelated checks during a read-only review.
5. Distinguish verified defects from hypotheses, advisory size signals, justified exceptions, and checks that could not be run. A convention difference alone is not a defect.

## Output

Lead with findings ordered by severity. Each finding needs a location, concrete consequence, evidence, and the smallest useful remediation. If none are found, state the inspected scope and verification limits. End with relevant checks performed, unrun checks, and open assumptions; do not claim whole-project correctness from partial evidence.
