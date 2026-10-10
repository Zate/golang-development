# Go Implementation Idioms Reference

Apply these idioms within the existing repository's conventions and public contracts.

## Names And Comments

- Package names: short, lowercase, no underscores, no stutter.
- Exported identifier comments should begin with the identifier name unless there is a strong reason.
- One-method interfaces usually end in `-er`: `Reader`, `Writer`, `Formatter`.
- Use MixedCaps, not snake_case.
- Keep initialisms consistent: `HTTPServer`, `userID`.
- Avoid names that shadow built-ins in confusing scopes.

## Function Shape

Prefer early error handling; use `%w` here only when exposing the cause matches the API contract:

```go
if err != nil {
    return fmt.Errorf("load config: %w", err)
}
```

Avoid deep nesting and unnecessary `else` after `return`. Keep functions small enough to test and name. Extract helpers when a named step clarifies intent, not just to reduce line count.

Identify the function's responsibilities and state transitions first. Prefer
coherent inputs/results and explicit mutation over helpers that capture unrelated
state or merely divide a long function into arbitrary chunks. Preserve error,
cancellation, ordering, locking, and cleanup behavior; verify observable outcomes
before and after extraction. A shorter function can still have difficult nesting.

## Errors

- Errors are values. Return them; do not panic for ordinary failures.
- Error strings should not be capitalized or end with punctuation unless they include a proper noun or sentence from another source.
- Use sentinel errors when callers need stable classification:

```go
var ErrNotFound = errors.New("not found")
```

- Wrap with `%w` when preserving classification:

```go
return fmt.Errorf("read user %q: %w", id, err)
```

- Use `errors.Is` for sentinel/class errors and `errors.As` for typed errors.
- Do not compare `err.Error()` strings.
- Wrapping exposes the underlying error as part of your API. Do not expose a
  database/implementation error accidentally; preserve deliberate sentinel or
  typed-error contracts and add context without changing caller behavior.
- Return errors through lower layers; log once at the boundary that handles the
  failure rather than logging and returning the same error repeatedly.

## Context

- Pass `context.Context` as the first parameter: `func Do(ctx context.Context, ...)`.
- Do not store contexts in structs except for rare lifetime-managed types.
- Do not pass nil context; use `context.Background()` or `context.TODO()`.
- Context values are for request-scoped data crossing APIs, not optional parameters.

## Interfaces

- Define interfaces where they are consumed.
- Accept small interfaces when callers need substitution; otherwise prefer concrete types. Return concrete types when that fits the existing API.
- Keep interfaces small; combine at call sites only when necessary.
- Avoid `any` unless the API genuinely accepts any value, such as encoding, logging attributes, or generic containers.

## Slices, Maps, And Boundaries

- Copy slices/maps at API boundaries when mutation by caller/callee would be surprising.
- Preallocate when size is known and it helps readability or measured performance;
  do not add speculative optimization merely to satisfy a suggestion.
- Prefer nil slices for empty results unless JSON/API compatibility requires `[]`.
- Do not write to a nil map.

## Defer And Cleanup

- Use `defer` for cleanup close to acquisition.
- Check close errors when close can affect durability, such as file writes.
- Avoid defers inside hot loops unless the cost and lifetime are acceptable.

## Generics

Use type parameters when operations are truly independent of concrete domain types and preserve type safety. Prefer ordinary interfaces for behavior and concrete types for domain concepts.

## Sources

- https://go.dev/wiki/CodeReviewComments
- https://go.dev/blog/go1.13-errors
- https://go.dev/doc/effective_go
