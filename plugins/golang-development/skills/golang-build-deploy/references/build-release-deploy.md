# Go Build, Release, And Deploy Reference

Sources distilled: Go `cmd/go`, Go module docs, Go security best practices, and common production Go service practice.

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

```Dockerfile
FROM golang:1.24 AS build
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

## Service Runtime Checklist

- Accept config from environment/files/flags according to repo convention.
- Use `context.Context` for request lifecycle and shutdown.
- Configure HTTP server timeouts.
- Handle `SIGINT`/`SIGTERM` with graceful shutdown.
- Expose health/readiness endpoints when deployed behind orchestration.
- Log structured errors without leaking secrets.
- Avoid global mutable config after startup.

## Release Checklist

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
