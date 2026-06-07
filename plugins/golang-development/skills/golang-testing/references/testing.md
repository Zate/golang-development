# Go Testing Reference

Sources distilled: local Uber Go Style Guide test tables, Clean Go TDD, official `testing` package docs, Go fuzzing docs, security best practices, and `cmd/go`.

## Commands

```powershell
go test ./...
go test ./pkg/name -run TestName -count=1 -v
go test ./... -race
go test ./... -cover
go test ./... -coverprofile=coverage.out
go test ./pkg/name -bench=. -benchmem
go test ./pkg/name -fuzz=FuzzName -fuzztime=30s
```

## Table Tests

```go
func TestParse(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    Config
        wantErr error
    }{
        {name: "empty", input: "", wantErr: ErrEmpty},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Parse(tt.input)
            if !errors.Is(err, tt.wantErr) {
                t.Fatalf("Parse() error = %v, want %v", err, tt.wantErr)
            }
            if !reflect.DeepEqual(got, tt.want) {
                t.Fatalf("Parse() = %#v, want %#v", got, tt.want)
            }
        })
    }
}
```

Use `cmp.Diff` if `go-cmp` is already a dependency.

## Helpers And Fixtures

- Mark helpers with `t.Helper()`.
- Use `t.TempDir()` for filesystem tests.
- Use `t.Setenv()` for environment changes.
- Use `t.Cleanup()` to close servers, restore globals, and stop goroutines.
- Put golden files and fixtures under `testdata/`; the go tool ignores it for package builds.

## Fakes And Mocks

- Prefer hand-written fakes for small interfaces.
- Keep fake behavior explicit in the test.
- Do not introduce an interface only to mock a concrete type unless the boundary is useful in production too.

## Fuzz Tests

Fuzzing is built into Go since 1.18. A fuzz target starts with `Fuzz`, accepts `*testing.F`, seeds with `f.Add`, and calls `f.Fuzz`.

Use fuzzing for parsers, decoders, validators, protocol handlers, and security-sensitive input handling.

## Benchmarks

Use benchmarks to compare known alternatives or guard hot paths. Include allocations with `-benchmem`. Reset timers after expensive setup.

## Integration Tests

- Use build tags such as `//go:build integration` for tests requiring real services.
- Prefer containers or local fakes only when the repo already uses them.
- Keep unit tests runnable with plain `go test ./...`.

## Sources

- https://pkg.go.dev/testing/
- https://go.dev/doc/security/fuzz/
- https://pkg.go.dev/cmd/go
