# Go Quality And Linting Reference

Sources distilled: local `golangci.yaml`, Uber Go Style Guide linting, Effective Go formatting, Go `cmd/go` vet docs, and Go security best practices.

## Baseline Verification

```powershell
gofmt -w <files>
go test ./...
go vet ./...
golangci-lint run
```

Use `go test -json` or `go build -json` when an agent/tool needs structured output.

## Formatting

- `gofmt` is authoritative for Go formatting.
- `goimports` adds/removes/sorts imports and applies gofmt.
- Keep import groups: standard library, third-party, local module.

## Vet And Static Analysis

- `go test` runs a curated vet subset. Run `go vet ./...` for explicit vet checks.
- `staticcheck` catches broader correctness and simplification issues.
- `govulncheck` reports reachable known vulnerabilities when installed.

## Golangci-Lint Guidance

Good default high-signal linters:

- Correctness: `govet`, `staticcheck`, `errcheck`, `ineffassign`, `unused`, `errorlint`, `nilerr`, `nilnil`, `bodyclose`, `rowserrcheck`, `sqlclosecheck`.
- Maintainability: `revive`, `gocyclo`, `unparam`, `unconvert`, `prealloc`, `exhaustive`.
- Security/style: `gosec`, `misspell`, `copyloopvar`, `contextcheck`, `nolintlint`, `sloglint`, `usestdlibvars`.

Use exclusions sparingly and prefer path-scoped test exclusions for noisy security rules.

## Review Checklist

- Errors are handled, wrapped, and classified correctly.
- Context cancellation/deadlines are propagated.
- Goroutines have shutdown paths; channels cannot strand senders on early return.
- Shared state is protected; race-prone changes get `go test -race`.
- Public API names and package names avoid stutter.
- Tests cover success, errors, edge cases, and changed contracts.
- Linter suppressions include a clear reason.

## Sources

- https://pkg.go.dev/cmd/go
- https://go.dev/doc/security/best-practices
