---
name: golang-implementation-idioms
description: Implements or reviews Go function shape, error contracts, context propagation, nil handling, and API behavior. Use for code changes, reducing nesting, or idiom-specific reviews while preserving compatibility.
license: MIT
---

# Go Implementation Idioms

Follow the user's scope and repository instructions. Reviews are read-only unless fixes are requested.

## Workflow

1. Inspect the target code, callers, and tests. Preserve architecture, dependency choices, useful nil behavior, and public contracts.
2. Prefer early error returns and explicit data flow. Extract a helper when its responsibility has a useful name and coherent inputs/results, not merely to pass a metric.
3. Wrap errors with `%w` deliberately: it exposes the underlying error to callers. Preserve stable classification and log an error once at the boundary that handles it.
4. Use existing standard-library and project idioms. Choose concrete types or small consumer-owned interfaces for actual needs; avoid speculative generics, utilities, dependencies, and optimizations.
5. For implementation, format changed files and run relevant repository checks. For review, report concrete behavioral or readability consequences and the smallest remediation; do not rewrite code to match a preference.

## References

For a straightforward fix, use the workflow above. Read [idioms.md](references/idioms.md) only to resolve an unanswered question about function responsibilities, errors, context, interfaces, nil behavior, or API contracts. Use `golang-quality-linting` only when quality-gate selection or complexity adoption needs clarification.
