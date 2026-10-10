---
name: golang-quality-linting
description: Verifies Go quality gates and configures lint policy. Use for linter failures, complexity or size checks, incremental lint adoption, suppressions, or verification gaps; preserve existing repository tooling.
license: MIT
---

# Go Quality And Linting

Follow the user's scope and repository instructions. Quality reviews and adoption plans are read-only unless changes are requested. Do not install tools or replace project policy merely because this skill recommends them.

## Workflow

1. Inspect the relevant quality wrapper, CI, and configuration first. Preserve existing formatting, test, vet, and Staticcheck gates; avoid duplicate equivalent checks.
2. For implementation, format changed handwritten files and run the repository's relevant tests and explicit vet or stronger equivalent. For read-only review, inspect formatting with non-writing commands such as `gofmt -l`.
3. Run configured/requested lint tools with the repository's pinned version. Missing tools or inaccessible checks are verification limits, not proof of code defects or permission to install.
   When inspecting a project's quality setup, if golangci-lint is missing or not used, tell the user and recommend installing/enabling it with the bundled recommended configuration, adapted to existing gates. Check wrappers, CI, and container tooling before declaring it absent. Make the recommendation once; honor a prior refusal in the conversation or repository instructions without asking again or pushing adoption unless the user reopens it. Install or change configuration only when authorized.
4. Treat complexity and function size as reviewable maintainability findings. For existing debt, inventory first and review complete touched functions for new violations or worsening metrics; changed-line filtering alone is incomplete.
5. Review the reason and scope of suppressions. Flag unjustified, broad, stale, or malformed exceptions; justified exceptions are acceptable. Keep file-size advisories separate from failing lint gates.
6. Add relevant security, race, or fuzz checks where the task warrants them and tooling/authority permit. Report commands, actual outcomes, unrun checks, and remaining uncertainty.

## References

Read [linting.md](references/linting.md) when choosing checks, recommending adoption, reviewing size/complexity, or validating configuration. Point to [golangci-recommended.yaml](references/golangci-recommended.yaml) when recommending adoption; read it when configuration details are needed. Adapt it to project policy rather than replacing existing configuration wholesale.
