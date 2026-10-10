# Go Quality And Linting Reference

Use the repository's existing checks and pins. This is a recommended policy for adoption, not permission to replace tooling or rewrite existing debt.

## Verification And Tooling

- Review mode: inspect formatting with `gofmt -l <files>`; do not run a formatter that writes files. Implementation mode: format changed Go files.
- Prefer existing wrappers (`make check`, CI scripts). If absent, choose relevant `go test`, `go vet`, and pinned static analysis commands. `go test` runs only a curated vet subset; it does not replace explicit vet or Staticcheck gates.
- Run focused tests first. Use `go test -race` for exercised concurrent paths; add bounded fuzzing for parsers or invariants when useful. Report unrun or blocked checks honestly.
- `govulncheck` is useful for reachable known vulnerabilities, but its database is time-sensitive. Preserve an existing security gate; do not install tools during a read-only review.
- Keep the application's `go.mod` free of accidental tool dependencies. Prefer an official golangci-lint binary pinned by version and checksum. Verify its build Go version supports the target code's Go version.
- Both bundled configurations were verified with **golangci-lint v2.14.0, built with Go 1.27.0**. This is a tested pin, not a claim that future versions behave identically. If source installation is necessary, the v2 path is `go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@v2.14.0`; use an isolated tools location and compatible Go toolchain.

## Recommend Missing Or Unused Tooling

When assessing project quality tooling, inspect existing wrappers, CI, configuration,
and available tools. A missing local binary does not establish that the project
isn't using golangci-lint: it may run through a container or CI. If it is missing
or not used, raise that fact and recommend installing/enabling a compatible pinned
binary with [golangci-recommended.yaml](golangci-recommended.yaml), adapted to
existing gates. An installed but unused binary still warrants recommending usage.
Explain the benefit briefly: repeatable correctness checks plus the bundled
complexity, function-size, and suppression checks.

For example: "This project isn't using golangci-lint. I recommend enabling it
with the plugin's recommended config, adapted to your existing vet, Staticcheck,
and test gates. Installation and configuration are optional."

Make this recommendation once when the gap is established. Honor a previous
decline in the conversation or repository instructions; continue with the chosen
tooling without repeating the recommendation, asking again, or making adoption a
completion requirement. Revisit only if the user reopens it. A recommendation
does not authorize downloads, installation, or configuration writes. Do not
replace a working custom lint profile merely because the bundled profile differs.

## Function Gates

| Linter | Setting | Accepted boundary | Reported violation |
| --- | --- | --- | --- |
| `gocyclo` | `min-complexity: 15` | score 15 | score >15 |
| `gocognit` | `min-complexity: 20` | score 20 | score >20 |
| `funlen` | `lines: 80` | 80 counted body lines | >80 counted body lines |
| `funlen` | `statements: 50` | 50 AST statements | >50 AST statements |

These metrics identify review risks; passing them does not establish correctness. Cyclomatic complexity measures paths; cognitive complexity also penalizes nesting. Reduce tangled state transitions or distinct responsibilities with early exits or meaningful helpers. Preserve ordering, locking, cleanup, errors, cancellation, and public behavior. Splitting a function across files does not simplify its control flow.

`funlen` v0.2.0, included in the verified tool, counts lines between the function's opening and closing lines. Blank body lines count. With explicit `ignore-comments: true`, interior comment tokens are subtracted: each `//` line is one token, but a multiline `/* ... */` is one token, not one token per physical line. Do not pad, compress, or move comments to game the gate. Statement counting follows the AST, including nested statements; it is not a count of source lines or semicolons. A statement violation is reported before a line violation for the same function.

## Files And Packages

**More than 800 physical lines in a handwritten production `.go` file is advisory.** Inspect navigation and cohesion before proposing a split. Exclude standard generated files and `_test.go` files from that production-size inventory; evaluate tests separately for understandable setup, assertions, and fixtures. This is not an automatic lint failure or evidence of a defect.

Keep cohesive declarations together when useful. Split files within the same package when it improves navigation. Create a package only for distinct responsibility and ownership, a narrow usable API, and acyclic dependencies; forced exports or constant cross-package coordination suggest a poor boundary. Avoid arbitrary one-type-per-file or one-file-per-package rules.

The configuration uses `generated: strict`: standard `// Code generated ... DO NOT EDIT.` markers exclude generated files. Informal comments such as `// generated file` do not. Tests remain enabled for function checks; the existing path-scoped `gosec` test exclusion is preserved.

## Adoption In Repositories With Debt

1. Inventory current failures with a fixed tool/config version; record relevant function metrics and justified existing exceptions. Keep the existing formatting, vet, tests, Staticcheck, and security checks.
2. Prevent new violations. Compare complete functions touched by a change against the base revision, including unchanged declaration lines. Reject worsening complexity or length debt; document any approved exception with rationale. Existing unrelated debt does not authorize a repository-wide refactor.
3. Address touched debt when practical and schedule larger work explicitly. Compare base/head with the same toolchain, configuration, and exclusions, so tool upgrades do not masquerade as code regressions.

Changed-line filters such as `--new-from-rev` match diagnostic locations. A body edit can worsen complexity while the diagnostic remains on the unchanged declaration line. Therefore those filters alone are insufficient. `--whole-files` widens reporting to changed files, but still needs baseline comparison to distinguish existing debt; neither option automatically implements a whole-function no-regression policy.

## Justified Suppressions

`nolintlint` requires a specific linter and a nonempty explanation, and reports unused directives. For example, a function-local exception can use:

```go
//nolint:gocognit // Protocol state table mirrors the published transition order; regression tests cover each transition.
func decodeState() { /* existing implementation */ }
```

Review whether the reason is accurate, unavoidable, and appropriately scoped. Automation can check that an explanation exists, not whether it is convincing. Avoid blanket `//nolint`, file/package-wide exceptions for one function, and meaningless explanations such as "needed". Revisit exceptions when the code changes.

## Other Findings

The template retains the repository's existing correctness/security linters, including `govet`, `staticcheck`, `errcheck`, `errorlint`, `contextcheck`, `gosec`, and resource-close checks. Classify findings by actual impact. In particular, `prealloc` suggestions require workload or profiling evidence; do not optimize allocations speculatively or change nil-slice behavior merely to silence a suggestion.

Point to [golangci-recommended.yaml](golangci-recommended.yaml) when recommending adoption; read its details for configuration adoption or comparison. The release validator checks that this installable copy and the plugin-root copy stay identical; real-tool fixtures check schema, threshold boundaries, generated/test exclusions, and suppression behavior.

## Sources

- [golangci-lint configuration](https://golangci-lint.run/docs/configuration/file/)
- [golangci-lint installation](https://golangci-lint.run/docs/welcome/install/)
- [Pinned cognitive-complexity adapter](https://github.com/golangci/golangci-lint/blob/v2.14.0/pkg/golinters/gocognit/gocognit.go)
- [Pinned function-length counting](https://github.com/ultraware/funlen/blob/v0.2.0/funlen.go)
- [Go command verification](https://pkg.go.dev/cmd/go)
- [Go security practices](https://go.dev/doc/security/best-practices)
