# Marketplace validation evidence

This file records repeatable marketplace smoke tests. The tests use isolated host configuration directories. They do not use the normal Codex or Claude Code profiles.

## Local marketplace smoke test

- Date: 2026-08-10
- Source commit: `96ad257`
- Plugin version: `0.1.0`
- Operating system: Windows
- Codex CLI: `0.146.0`
- Claude Code: `2.1.225`
- Marketplace: `golang-development-marketplace`
- Plugin: `golang-development`

### Isolation

- Codex used a new temporary `CODEX_HOME`.
- Claude Code used a new temporary `CLAUDE_CONFIG_DIR`.
- Claude Code plugin storage used `CLAUDE_CODE_PLUGIN_CACHE_DIR` under the same temporary root.
- The test compared normal Codex and Claude Code configuration and plugin-state signatures before and after installation.
- The temporary root was removed after the test.

### Commands

The test used the repository root as `<repo-root>` and new directories under `<temporary-root>`:

```powershell
$env:CODEX_HOME = '<temporary-root>\codex'
codex plugin marketplace add '<repo-root>' --json
codex plugin add golang-development@golang-development-marketplace --json
codex plugin list --marketplace golang-development-marketplace --json

$env:CLAUDE_CONFIG_DIR = '<temporary-root>\claude'
$env:CLAUDE_CODE_PLUGIN_CACHE_DIR = '<temporary-root>\claude\plugins'
claude plugin marketplace add '<repo-root>'
claude plugin install golang-development@golang-development-marketplace
claude plugin details golang-development@golang-development-marketplace
```

### Results

- Codex added the marketplace and installed an enabled plugin at version `0.1.0`.
- The Codex installed package contained eight valid skill directories.
- Claude Code added the marketplace and installed the plugin at user scope inside the isolated configuration.
- Claude Code component details listed the same eight skills.
- Normal host profile changes: `0`.
- A Codex warning said that it would not create PATH aliases under a temporary directory. Plugin installation and inventory checks still passed.

The eight registered skills were:

1. `golang-architecture-patterns`
2. `golang-build-deploy`
3. `golang-code-audit`
4. `golang-development-workflow`
5. `golang-implementation-idioms`
6. `golang-planning-layout`
7. `golang-quality-linting`
8. `golang-testing`

## GitHub marketplace smoke test

### Current published source

- Date: 2026-08-10
- Source: `Zate/golang-development`
- Default branch: `main`
- Tested commit: `15b90cbf047cb4a2855e1124845a1c23ef262793`
- Plugin version: `0.1.0`
- Codex CLI: `0.146.0`
- Claude Code: `2.1.225`
- Codex skills: `8`
- Claude Code skills: `8`
- Normal host profile changes: `0`

The test used new temporary `CODEX_HOME`, `CLAUDE_CONFIG_DIR`, and `CLAUDE_CODE_PLUGIN_CACHE_DIR` directories. Both hosts added the GitHub repository as a marketplace, installed `golang-development@golang-development-marketplace`, and loaded the same version and skill inventory from the same commit.

### Hosted validation

[GitHub Actions run 31356286623](https://github.com/Zate/golang-development/actions/runs/31356286623) passed on Windows and Ubuntu for the tested commit. Both jobs passed release validation, six unit tests, the generic installer dry-run, installation of the pinned official Agent Skills validator, and validation of all eight skills.


## Version 0.2.0 local verification

- Date: 2026-10-10
- Source: local changes on `b433e9c03937d54de059dcdc334ce1c687ae2fc5`; not published
- Host: macOS, amd64
- Codex CLI: `0.162.0`
- Claude Code: `2.1.296`
- Go: `1.27.1`
- golangci-lint: `2.14.0`, built with Go `1.27.0`, commit `114493f9`
- Official skill validator: the existing pinned Agent Skills commit `69ef37e9424c0a7ea9dd2293b559e43ec8176379`, installed in a disposable virtual environment

### Package, policy, and installation checks

| Check | Result |
| --- | --- |
| `python3 -B scripts/validate_release.py` | PASS: manifests, eight skills, references, interface metadata, lint-template parity |
| `python3 -B -m unittest discover -s tests -v` | PASS: 10 tests, including release failure diagnostics and eval adapter checks |
| `python3 -B scripts/validate_skills_ref.py` with the pinned validator on PATH | PASS: all eight skills |
| `claude plugin validate . --strict --json` and the plugin directory equivalent | PASS: zero manifest warnings/errors; this command does not validate skill contents |
| `python3 -B scripts/validate_lint_config.py --lint <verified-binary>` | PASS: both schemas and 20 real-tool behavioral fixtures |
| Generic installer dry-run and disposable installation | PASS: all eight complete skill trees, including the installable lint configuration |
| Codex local marketplace add/install/inventory in fresh `CODEX_HOME` | PASS: enabled version 0.2.0, eight installed skill trees matching current source bytes |
| Claude local marketplace add/install/details in fresh `CLAUDE_CONFIG_DIR` and plugin cache | PASS: version 0.2.0, eight installed skill trees matching current source bytes |

The lint binary came from the official release archive. Its Darwin amd64 SHA256
was `a5667c1c3536be1740133213e1e822bfb8f0d98ea12903174d6d5f635e4ed68d`.
The fixture suite checks exact accepted/rejected complexity, length, and statement
boundaries; single-line versus block-comment counting; standard versus informal
generated markers; test complexity and security exclusions; justified, missing,
blanket, and unused suppressions; and an ordinary function against the full policy.

Installation smoke tests compared SHA256 signatures of normal Codex configuration
and plugin storage plus normal Claude settings and plugin storage before and after
installation: zero changes to those checked paths. Temporary profiles hold the test
installations. This is not a global installation or a claim about every cache,
authentication, telemetry, or account-usage file.

The Docker Hub official `golang:1.27.2` tag was verified active with Linux amd64
and arm64 images. The example still requires a reviewed digest and platform choice
for an actual reproducible release.

### Behavioral and token evidence

At the 0.2.0 verification, the shared suite in `evals/cases.json` covered all eight skills with ten cases.
The comparison below uses its first eight unchanged cases: narrow fix, read-only
audit, cohesive large file, nested function, existing lint debt, cancellation tests,
release planning, and unrelated translation. An untouched 0.1.0 plugin snapshot,
updated plugin, and no-plugin arm received identical prompts. Prompts allow guidance
reads while forbidding edits and project execution. Native Claude ran Opus 5.5 in
both arms; Codex used a fresh-home CLI default with user configuration/rules ignored.
The Codex JSON stream does not identify its resolved model, so exact model identity
was not independently established; use `--model` for future reproducible runs.

| One run per case, eight cases | Original plugin | Updated plugin | No plugin |
| --- | ---: | ---: | ---: |
| Codex manual outcome review | 8/8 | 8/8 | 8/8 |
| Codex input tokens, including cache hits and repeated conversation input | 388,802 | 350,869 | 318,725 |
| Codex cached input tokens | 318,208 | 284,544 | 262,912 |
| Codex output tokens | 3,949 | 4,004 | 3,459 |
| Codex tool calls | 18 | 20 | 8 |
| Codex distinct skills read, summed per case | 24 | 8 | 0 |
| Codex distinct references read, summed per case | 7 | 7 | 0 |
| Codex elapsed seconds, summed per case | 185.85 | 190.95 | 170.09 |
| Claude native outcome grading | 8/8 | 8/8 | 8/8 in updated suite's baseline arm |
| Claude total input tokens: uncached + cache creation + cache reads | 222,283 | 216,335 | 136,161 in updated suite's baseline arm |
| Claude output tokens | 13,779 | 13,264 | 12,180 in updated suite's baseline arm |
| Claude tool calls | 13 | 13 | 7 in updated suite's baseline arm |
| Claude skill invocations | 6 | 5 | 0 |
| Claude reference reads | 5 | 5 | 0 |
| Claude elapsed seconds, summed per case, excluding judge time | 191 | 184 | 187 in updated suite's baseline arm |

Claude's native `plugin details` projected always-on catalog cost fell from about
850 to 497 tokens (about 42%). Those are host estimates, exclude references, and
are not interchangeable with measured per-run totals. These small samples show
less catalog/routing overhead, but do not establish an accuracy increase or a
consistent latency improvement. No-plugin outcomes were often already correct.
An earlier exploratory Claude run scored the original plugin's release answer
7/8 overall; its finalized-prompt comparison passed 8/8. Do not treat that noisy
exploratory result as a demonstrated before/after accuracy gain.

Trace review found a redundant reference read for the trivial fix. After narrowing
the idioms reference trigger, three Codex repeats each read one specialist and no
references, returned the correct fix, and used one tool call (30,250–30,252 input
tokens). Three nested-function repeats selected two relevant specialists rather
than the broad router. Three unrelated-request repeats returned only `Bonjour`
and used no skills/references/tools. Three explicit error-contract repeats invoked
the idioms skill and preserved deliberate `%w` exposure and single-boundary logging.
Broad-workflow routing also selected relevant stages without requiring all skills.

Claude confirmation ran three repetitions each of narrow fix, nested function,
release plan, explicit error contract, and unrelated translation: all 15 with-plugin
outcomes passed, and explicit invocation succeeded 3/3. All three unrelated runs
had zero Skill calls. Narrow fixes correctly skipped invocation 3/3. The two added
cases (explicit contract and broad workflow) also passed a final run with outcome
rubrics separate from activation; their no-plugin outcomes passed too. Earlier
exploratory explicit/routing rubrics mixed invocation with outcome and are not used
as evidence of an accuracy gain.

Activation is recorded separately from answer quality. Claude may correctly skip
a trivial natural-language request; explicit invocation is checked as a separate
indicator. The unrelated-request native grader requires zero Skill calls in both
arms. Codex metrics count successful `cat` reads visible in its command traces;
manual inspection remains necessary for other read mechanisms and rubric grading.

### Reproduction and boundaries

Use the commands in the README; select a new output directory and hold the model,
prompts, host version, and tool/config pins fixed. Claude reports include native
judge votes and baseline arms. Codex traces and `run.json` include actual usage,
timing, and read metrics, but the exit code establishes execution success rather
than automatic rubric correctness. Repeated cases reduce noise; a judge verdict
alone does not establish correctness. Model evaluations use authenticated host
account usage and are not an automatic CI job.

The updated Ubuntu lint-policy job is configured, including the official Linux
binary checksum, but has not run on GitHub. Updated Windows verification is also
pending hosted CI. Historical Windows/published evidence above remains historical.
No Docker build, application deployment, GitHub publication, global plugin install,
or other-repository adoption was performed. Local use is verified; hosted release
acceptance follows a separately authorized push and passing CI.

The guidance follows current [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills),
[OpenAI skill evaluation guidance](https://developers.openai.com/blog/eval-skills),
[Claude skills documentation](https://code.claude.com/docs/en/skills), and
[Claude native eval guidance](https://code.claude.com/docs/en/plugin-evals).


## Version 0.2.1 adoption recommendation update

- Date: 2026-10-10; local source, not published.
- Quality setup reviews now recommend a compatible pinned golangci-lint binary
  and the bundled profile when tooling is missing or unused, while preserving
  existing gates. Wrappers, CI, and containers count as usage.
- A prior refusal is honored without renewed suggestions or adoption requirements.
  Recommendations do not authorize installation or configuration writes.
- Workflow/audit routing points to the quality skill for this recommendation.
- The suite now has 13 cases: the original ten plus missing-tool recommendation,
  installed-but-unused recommendation, and respect for a previous refusal.
- Package validation, all 10 unit tests, official validation of all eight skills,
  and isolated Codex/Claude local installs passed. Installed skill trees matched
  current source bytes; checked normal settings/plugin-state signatures were
  unchanged. Version 0.2.1 gives installed caches a distinct package version.

The three focused cases ran once per host against the new recommendation text:
all three passed in both hosts. Codex responses were reviewed against the shared
rubrics. Claude used its native
outcome and activation graders with a no-plugin arm; reports stayed local. These
runs copied the updated policy before the manifest-only patch version bump, so
their recorded plugin version is 0.2.0. The packaged 0.2.1 installation was checked
separately. These focused runs establish the observed policy behavior, not a
statistical accuracy or performance improvement.
