# Go Architecture And Pattern Reference

Sources distilled: Effective Go, Uber Go Style Guide, Clean Go, Twelve Go Best Practices, Go Proverbs, and Go blog/articles.

## Principles

- Clear is better than clever.
- The bigger the interface, the weaker the abstraction.
- Ask for what you need: accept the smallest interface required by the function.
- Keep independent packages independent. Use local interfaces to break dependency on concrete producers.
- Avoid concurrency in public APIs. Synchronous APIs are easier to test, compose, and run concurrently by callers.
- Make zero values useful where practical. Constructors are still appropriate when invariants or dependencies are required.

## Boundary Patterns

Consumer-owned interface:

```go
type UserStore interface {
    User(ctx context.Context, id string) (User, error)
}

type Service struct {
    store UserStore
}
```

Compile-time interface assertion:

```go
var _ io.Writer = (*Buffer)(nil)
```

Function adapter:

```go
type appHandler func(http.ResponseWriter, *http.Request) error

func withErrors(h appHandler) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        if err := h(w, r); err != nil {
            http.Error(w, "internal error", http.StatusInternalServerError)
        }
    }
}
```

## Service And Repository Guidance

- Use a repository/store interface when persistence is replaceable or expensive to instantiate in tests.
- Keep SQL/driver details in adapter packages; keep transaction semantics explicit.
- Do not create one-method pass-through services for every table.
- Keep HTTP handlers thin: parse/validate request, call service, map domain errors to status codes, encode response.
- Keep domain errors independent of HTTP/gRPC codes.

## Functional Options

Use functional options when constructors have optional settings with sensible defaults:

```go
type Option func(*Client)

func WithTimeout(d time.Duration) Option {
    return func(c *Client) { c.timeout = d }
}

func New(baseURL string, opts ...Option) *Client {
    c := &Client{baseURL: baseURL, timeout: 10 * time.Second}
    for _, opt := range opts {
        opt(c)
    }
    return c
}
```

Avoid options for required dependencies. Required values belong in constructor parameters or a validated config struct.

## Concurrency Patterns

- Use `context.Context` for cancellation, deadlines, and request-scoped values.
- Always define goroutine lifetime and shutdown path.
- Avoid fire-and-forget goroutines.
- Use `sync.Mutex` for protecting shared memory; use channels for coordination and ownership transfer.
- Use buffered result channels or cancellation selects when early returns could strand senders.

## Red Flags

- Interfaces defined next to implementations instead of consumers.
- Public structs embedding implementation types unintentionally.
- Pointer to interface values.
- Global mutable state.
- `init` doing work that could be explicit setup.
- Generic `interface{}`/`any` where type parameters or concrete types fit.
- Pattern folders added before the repo needs them.
