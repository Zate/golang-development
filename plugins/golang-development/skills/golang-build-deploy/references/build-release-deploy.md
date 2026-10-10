# Go Build, Release, And Deploy Reference

Preserve existing build wrappers and dependency conventions. Examples are starting points, not permission to publish or deploy.

## Build Commands

```powershell
go build ./...
go build -o bin/app ./cmd/app
go install ./cmd/app
go test ./...
go version -m bin/app
```

Cross-compile:

```powershell
$env:GOOS="linux"; $env:GOARCH="amd64"; go build -o bin/app-linux-amd64 ./cmd/app
```

Embed version metadata:

```powershell
go build -ldflags "-s -w -X main.version=$env:VERSION -X main.commit=$env:GIT_COMMIT" -o bin/app ./cmd/app
```

Prefer package-level variables for injected metadata and make missing values safe.

## Modules And Supply Chain

- Commit `go.mod` and `go.sum`.
- Run `go mod tidy` intentionally; review dependency churn.
- Use `go list -m all` or dependency tooling to inspect modules.
- Run `govulncheck ./...` when available for security-sensitive or release work.
- Avoid `@latest` in repeatable release scripts unless the script is intentionally updating tools.

## Container Pattern

Choose a supported Go release compatible with `go.mod`, any `toolchain` directive,
CI, dependencies, and static-analysis tools. Go supports a release series until
two newer series exist. As checked on 10 October 2026, 1.26 and 1.27 are supported;
recheck the release policy when updating this example. Pin the selected patch
version (and image digest for reproducible releases), and deliberately refresh
security fixes rather than silently following `latest`.

```Dockerfile
FROM golang:1.27.2 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/app ./cmd/app

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /out/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

Adjust for CGO, CA certificates, shell needs, migrations, or debug tooling. Do not force distroless if the app needs OS packages.
The runtime image tag above also moves; pin its reviewed digest in a repeatable
release pipeline. Verify the selected platform/image exists before adoption.

## Service Runtime Checklist

- Accept config from environment/files/flags according to repo convention.
- Use `context.Context` for request lifecycle and shutdown.
- Configure HTTP server timeouts.
- Handle `SIGINT`/`SIGTERM` with graceful shutdown.
- Expose health/readiness endpoints when deployed behind orchestration.
- Log structured errors without leaking secrets.
- Avoid global mutable config after startup.

## Release Checklist

Use existing wrappers for these checks and supplement only gaps. Do not repeat equivalent checks or claim planned checks were executed.

- Clean working tree or intentional release metadata.
- `go test ./...`
- `go vet ./...`
- configured linter
- vulnerability scan if installed
- build target binaries/images
- smoke test binary/image
- inspect `go version -m` for module/build info

## Sources

- https://pkg.go.dev/cmd/go
- https://go.dev/doc/modules
- https://go.dev/doc/security/best-practices
- https://go.dev/doc/devel/release#policy
- https://go.dev/doc/toolchain
