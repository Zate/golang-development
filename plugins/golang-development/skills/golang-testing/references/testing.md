# Go Testing Reference

Use the repository's existing test tools. Tests should prove observable behavior, not reproduce implementation details.

Read the relevant section: [commands](#commands), [behavioral assertions](#table-tests), [fixtures](#helpers-and-fixtures), [fakes](#fakes-and-mocks), [asynchronous tests](#deterministic-asynchronous-tests), [fuzzing](#fuzz-tests), [benchmarks](#benchmarks), [integration](#integration-tests).

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

Compare stable values; normalize nondeterministic ordering only when order is
not part of the contract. Preserve meaningful nil-versus-empty distinctions.
For refactoring, assert results, side effects, error classification, and cleanup
rather than helper names or the number of internal calls.

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

## Deterministic Asynchronous Tests

- Control progress with readiness/completion signals or a fake clock. A timeout
  may bound a hung test; elapsed sleep is not proof that a worker reached a state.
- On Go 1.25 or newer, `testing/synctest` can provide fake time and wait for
  durable blocking for suitable in-process goroutines. Preserve older supported
  toolchains with explicit synchronization rather than upgrading for this helper.
- Test cancellation while a send is blocked, when a consumer stops reading, and
  on early error. Assert worker completion and cleanup; identify channel closure
  ownership and ensure no producer sends after closure.
- Use `t.Cleanup` to cancel and wait for test-owned workers. Cancellation alone
  does not prove they have stopped. Avoid assertions from goroutines that outlive
  the test and avoid parallel tests mutating shared environment/global state.
- Run focused race checks for relevant concurrency changes, then the broader
  repository gate where supported. Passing `-race` covers executed paths only;
  it does not prove all possible schedules are safe.

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
- https://go.dev/wiki/TestComments
- https://go.dev/blog/testing-time
- https://pkg.go.dev/testing/synctest
