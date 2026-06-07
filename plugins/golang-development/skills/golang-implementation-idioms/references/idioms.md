# Go Implementation Idioms Reference

Sources distilled: Effective Go, Uber Go Style Guide, Clean Go, Idiomatic Go, Go Proverbs, and official Go docs.

## Names And Comments

- Package names: short, lowercase, no underscores, no stutter.
- Exported identifier comments should begin with the identifier name unless there is a strong reason.
- One-method interfaces usually end in `-er`: `Reader`, `Writer`, `Formatter`.
- Use MixedCaps, not snake_case.
- Keep initialisms consistent: `HTTPServer`, `userID`.
- Avoid names that shadow built-ins in confusing scopes.

## Function Shape

Prefer early error handling:

```go
if err != nil {
    return fmt.Errorf("load config: %w", err)
}
```

Avoid deep nesting and unnecessary `else` after `return`. Keep functions small enough to test and name. Extract helpers when a named step clarifies intent, not just to reduce line count.

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

## Context

- Pass `context.Context` as the first parameter: `func Do(ctx context.Context, ...)`.
- Do not store contexts in structs except for rare lifetime-managed types.
- Do not pass nil context; use `context.Background()` or `context.TODO()`.
- Context values are for request-scoped data crossing APIs, not optional parameters.

## Interfaces

- Define interfaces where they are consumed.
- Accept interfaces, return concrete types.
- Keep interfaces small; combine at call sites only when necessary.
- Avoid `any` unless the API genuinely accepts any value, such as encoding, logging attributes, or generic containers.

## Slices, Maps, And Boundaries

- Copy slices/maps at API boundaries when mutation by caller/callee would be surprising.
- Preallocate when size is known or cheaply estimated.
- Prefer nil slices for empty results unless JSON/API compatibility requires `[]`.
- Do not write to a nil map.

## Defer And Cleanup

- Use `defer` for cleanup close to acquisition.
- Check close errors when close can affect durability, such as file writes.
- Avoid defers inside hot loops unless the cost and lifetime are acceptable.

## Generics

Use type parameters when operations are truly independent of concrete domain types and preserve type safety. Prefer ordinary interfaces for behavior and concrete types for domain concepts.
