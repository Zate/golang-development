# Go Repo Layout Reference

Use these as design defaults; existing repository policy and the user's scope take precedence.

## Layout Rules

- Start simple: one module, one package, tests beside code.
- Use one directory per package. Directory path controls import path; package name controls call-site readability.
- Use `internal/` to prevent imports outside the parent tree.
- Use `cmd/<binary>/main.go` for multi-command repos or binaries with support packages.
- Avoid a public `pkg/` dumping ground. Create public packages only for stable APIs intended for imports by other modules.
- Keep package dependency direction acyclic. If two packages import each other's concepts, move the shared abstraction nearer the consumer or merge packages.
- Use `go.work` for local multi-module development. Do not commit a workspace file unless the repo intentionally coordinates several modules.

## Common Shapes

```text
go.mod
client.go
client_test.go
internal/auth/auth.go
internal/auth/auth_test.go
```

```text
go.mod
cmd/tool/main.go
internal/config/
internal/run/
```

```text
go.mod
cmd/api/main.go
internal/httpapi/
internal/service/
internal/store/
internal/config/
```

## Planning Checklist

- Identify commands, importable packages, internal-only packages, generated code, and `testdata`.
- Confirm package names read well with exported identifiers: `json.Encoder`, not `json.JSONEncoder`.
- Keep important code first: package docs/build tags, imports, exported types/functions, helpers.
- Use `doc.go` when package documentation would otherwise clutter implementation files.
- Make packages independently testable; avoid hidden globals and heavy `init`.
- Prefer small migration steps: create package, move code, preserve public API, update imports, run tests.

## File Size And Cohesion

Review handwritten production Go files above 800 physical lines as a navigation
and cohesion advisory, not a failing gate or proof of complexity. Exclude tests
and files with the standard `// Code generated ... DO NOT EDIT.` marker from
this initial inventory. Review test structure separately when fixtures or cases
become difficult to navigate. Count physical lines including blanks/comments;
do not confuse this with function complexity or the linter's function-line count.

A long cohesive declaration table can stay intact. When navigation is the
problem, group related behavior into focused files in the same package; avoid
many tiny files and a one-type-per-file rule. Keep helpers near their primary
responsibility and preserve build tags, generated-file boundaries, and APIs.

Create a package only when it has a distinct responsibility, clear data/behavior
ownership, a useful narrow API, and a sensible acyclic dependency direction.
Keep tightly coupled unexported types together when separating them would expose
implementation details or force callers to import both packages to use either.
Avoid speculative `util`, `common`, or layering packages.

## Sources

- https://go.dev/doc/modules/layout
- https://go.dev/blog/package-names
- https://pkg.go.dev/cmd/go
- https://google.github.io/styleguide/go/best-practices#package-size
