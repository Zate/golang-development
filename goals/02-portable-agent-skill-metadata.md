# G02 - Make Skill Metadata Portable

Status: planned

## Objective

Make every bundled skill a complete, portable Agent Skills package when it is installed without the plugin wrapper.

## Source / context

- The eight `SKILL.md` files already meet the required Agent Skills name and description rules.
- A standalone copy of a skill does not carry the plugin-level license file unless the installer copies extra files.

## Scope

- Add `license: MIT` to every skill frontmatter block.
- Preserve valid names and trigger descriptions.
- Confirm that every name matches its parent directory.
- Confirm that descriptions remain within the Agent Skills limit.
- Confirm that all relative reference paths resolve inside the skill directory.
- Keep OpenAI-only UI metadata in `agents/openai.yaml` and out of standard frontmatter.

## Non-goals

- Do not add Claude-only frontmatter that changes invocation policy.
- Do not add tool allowlists.
- Do not require a specific agent product in `compatibility`.
- Do not rewrite the Go guidance unless a compatibility defect requires it.

## Implementation notes

- Use only portable Agent Skills fields in `SKILL.md`.
- Do not add version metadata that can drift from plugin manifests unless automated validation owns the value.
- Preserve progressive disclosure through the existing `references/` files.

## Acceptance criteria

- All eight skills declare `license: MIT`.
- All names match `^[a-z0-9]+(?:-[a-z0-9]+)*$`, do not exceed 64 characters, and match their directories.
- All descriptions are non-empty, describe purpose and trigger conditions, and do not exceed 1,024 characters.
- All `SKILL.md` files remain below 500 lines.
- All referenced files exist.
- Claude Code and Codex continue to discover all eight skills.

## Definition of done

- Acceptance criteria are met.
- Focused skill metadata checks pass.
- Required verification commands pass.
- Status is changed to `complete`.
- `goals/index.md` marks this goal complete.
- The work is committed in one focused commit.

## Verification

- `claude plugin validate ./plugins/golang-development --strict`
- Run direct checks for name, directory match, description length, license, line count, and references on all eight skills.
- Run `skills-ref validate <skill-directory>` for each skill when `skills-ref` is available.
