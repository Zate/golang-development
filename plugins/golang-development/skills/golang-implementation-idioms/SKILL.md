---
name: golang-implementation-idioms
description: Implement or audit idiomatic Go code using effective naming, errors, context, interfaces, generics, nil handling, slices/maps, documentation comments, and standard library conventions. Use when writing, refactoring, cleaning, or reviewing Golang code; reducing nesting; improving API ergonomics; checking idiomatic implementation style; or finding non-idiomatic Go in existing code.
license: MIT
---

# Go Implementation Idioms

## Build Workflow

1. Prefer straightforward code over abstraction. Make the happy path read down the page by handling errors early.
2. Use the standard library idioms already present in the repo: `context`, `errors`, `fmt`, `io`, `testing`, `slog`, `net/http`, and so on.
3. Keep names short but explanatory at their scope. Avoid package-name stutter in exported identifiers.
4. Wrap errors with context using `%w` when callers need `errors.Is` or `errors.As`.
5. Accept small interfaces and return concrete types. Avoid pointers to interfaces.
6. Use type parameters for real type relationships; do not use generics to avoid writing clear domain code.
7. Treat nil carefully: nil slices are usually fine for empty collections; maps must be made before writes.
8. Document exported packages, types, functions, methods, and non-obvious behavior for users.
9. Run `gofmt`/`goimports` after edits and keep generated code separate.

## Audit Workflow

1. Inspect call sites before judging names, exported APIs, interfaces, or generic types.
2. Flag error handling that loses classification, context, wrapping, cancellation, or caller actionability.
3. Check context usage, nil handling, map writes, slices, pointer/interface choices, and generated-code boundaries.
4. Treat style-only issues as low priority unless they obscure correctness or API intent.
5. Report concise remediations that preserve the repo's existing style.
6. Pair with `golang-code-audit` when producing a full findings-first review.

## Load References

- Read `references/idioms.md` when implementing APIs, error behavior, comments, interfaces, generics, or cleanup refactors.
- Pair with the companion `golang-quality-linting` skill before claiming the implementation is complete.
