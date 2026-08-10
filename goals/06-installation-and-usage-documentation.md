# G06 - Document All Installation Paths

Status: complete

## Objective

Give users exact, current commands for GitHub and local installation in Codex, Claude Code, and generic Agent Skills clients.

## Source / context

- The current README has exact Codex commands but only a general Claude Code description.
- Generic `.agents/skills` installation is not documented.
- Plugin invocation syntax differs between Codex and Claude Code.

## Scope

- Update the README with a concise compatibility statement.
- Document Codex GitHub marketplace add, plugin install, refresh, list, and remove commands.
- Document Codex local-clone marketplace add and install commands.
- Document Claude Code GitHub marketplace add, plugin install, reload, details, and uninstall commands.
- Document Claude Code local-clone marketplace add and install commands.
- Document generic user-level and project-level installation with the safe installer.
- Document invocation syntax and the eight installed skill names.
- Document release validation commands.
- Keep the canonical GitHub URL consistent with manifest metadata.

## Non-goals

- Do not claim support for a host that has not passed its applicable validation.
- Do not include destructive copy commands that overwrite existing skills.
- Do not document public directory submission as complete.
- Do not rename or publish the GitHub repository.

## Implementation notes

- Use the actual canonical `owner/repo` value at implementation time. The intended example can be `Zate/golang-skill`, but all examples must match the real published repository before G08 completes.
- Show Windows and POSIX local path examples where syntax differs.
- Explain that generic agents install the eight standard skills, not a generic plugin marketplace.
- Explain that `agents/openai.yaml` is optional OpenAI metadata and does not reduce generic compatibility.

## Acceptance criteria

- A new user can follow one complete GitHub installation path for Codex.
- A new user can follow one complete local-clone installation path for Codex.
- A new user can follow one complete GitHub installation path for Claude Code.
- A new user can follow one complete local-clone installation path for Claude Code.
- A generic client user can install to user or project `.agents/skills` without manual file selection.
- The README shows the correct Codex and Claude Code invocation forms.
- All documented validation commands exist and pass.

## Definition of done

- Acceptance criteria are met.
- Documentation matches the current manifests and scripts.
- Required verification commands pass.
- Status is changed to `complete`.
- `goals/index.md` marks this goal complete.
- The work is committed in one focused commit.

## Verification

- Run every local, offline command shown in the README.
- Check every referenced file path and command name.
- `python scripts/validate_release.py`
- `claude plugin validate . --strict`
- `claude plugin validate ./plugins/golang-development --strict`

## Completion notes

- Verification: Release validation, six tests, generic installer dry-run, both Claude Code strict validators, required README text, and all documented repository paths passed.
- Follow-ups: G07 and G08 will prove the local and GitHub host installation commands in isolated configurations.
