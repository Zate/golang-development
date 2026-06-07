# Go Repo Layout Reference

Sources distilled: Effective Go, Twelve Go Best Practices, Go Proverbs, Go module layout docs, Go package-name blog, and `cmd/go` docs.

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

## Sources

- https://go.dev/doc/modules/layout
- https://go.dev/blog/package-names
- https://pkg.go.dev/cmd/go
