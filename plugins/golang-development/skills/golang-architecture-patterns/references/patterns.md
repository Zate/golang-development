# Go Architecture And Pattern Reference

These are design defaults, not mandatory layers. Follow the repository's policy and the user's scope.

Read the relevant section: [principles](#principles), [boundaries](#boundary-patterns), [services](#service-and-repository-guidance), [file/package cohesion](#file-versus-package-boundaries), [options](#functional-options), [concurrency](#concurrency-patterns), [review risks](#red-flags).

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

## File Versus Package Boundaries

For navigation, move cohesive groups into files within the same package. File
length alone does not justify a new import boundary. A new package needs a
distinct responsibility, explicit ownership, a useful narrow API, and a clear
dependency direction. Keep coupled types together if separation would export
internals or require callers to import both packages to use either. Introduce
transport/persistence adapters or logging seams only for demonstrated coupling,
testing, or reuse needs, rather than to satisfy an architectural template.

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
- Identify who starts each goroutine, cancels it, and waits for completion.
- Define shared-state ownership and which sender closes each channel; consumers
  must not close a channel while producers may still send.
- Avoid fire-and-forget goroutines.
- Use `sync.Mutex` for protecting shared memory; use channels for coordination and ownership transfer.
- Use buffered result channels or cancellation selects when early returns could strand senders.
- Buffering is sufficient only when it bounds all outstanding sends. Make
  potentially blocking sends/receives cancellation-aware and prove shutdown with
  completion signals, not sleeps. Do not hold a shared-state lock while waiting
  for a worker that may need that lock.

## Red Flags

Investigate these in context; their presence alone is not a defect.

- Interfaces defined next to implementations instead of consumers.
- Public structs embedding implementation types unintentionally.
- Pointer to interface values.
- Global mutable state.
- `init` doing work that could be explicit setup.
- Generic `interface{}`/`any` where type parameters or concrete types fit.
- Pattern folders added before the repo needs them.

## Sources

- https://go.dev/wiki/CodeReviewComments#interfaces
- https://go.dev/wiki/CodeReviewComments#goroutine-lifetimes
- https://google.github.io/styleguide/go/best-practices#package-size
- https://go.dev/blog/package-names
