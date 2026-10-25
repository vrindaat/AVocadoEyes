# Contributing together

Audience: both contributors. Owner: repository maintainers. Update this document
when development commands, review, or delivery steps change.

## First checkout

Clone the repository using the README instructions. Configure your own identity
locally if it is not already set; do not use your teammate's identity:

```sh
git config user.name "Your Name"
git config user.email "your-address@example.com"
```

Open Codex at the repository root and read `AGENTS.md`. Personal credentials,
Codex account configuration, and local trust settings stay on your own machine.
No shared model selection or permission bypass is needed for this workflow.

## Shared commit skill

The versioned skill lives at
[.agents/skills/loop-stage-and-commit/SKILL.md](../.agents/skills/loop-stage-and-commit/SKILL.md).
It ships with the clone and updates with Git. Open a new Codex session at this
repository root after pulling a skill update if the running session has stale
skill metadata. Invoke it with `$loop-stage-and-commit`; if a personal skill has
the same name, explicitly name the repository path to select the shared version.

This copy preserves atomic commits and explicit staging, adds SDD issue
references, and stops after authorized changes rather than sweeping up another
contributor's edits to force a clean workspace. Review changes to the skill in PRs
like other shared process rules. Publishing the skill does not execute it.

## Work cycle

1. Inspect `git status --short`. Preserve existing edits before switching branches.
2. Fetch with `git fetch origin`. From a clean checkout, update `main` with
   `git switch main` and `git pull --ff-only origin main`.
3. Create `<name>/<short-change>` with `git switch -c`. Open/claim an issue using
   the change template, assign the accountable owner, and agree on overlapping
   files or interface ownership with your teammate in the issue.
4. Select the smallest SDD artifact and record acceptance when required. Both
   people implement from the same accepted spec path on Git, not from chat memory.
5. Implement small changes and run relevant checks. Use targeted staging,
   `git diff --cached`, and meaningful commits with `Refs #<issue>` in the body.
6. Push your branch with `git push -u origin <branch>`. Open a PR using the tracked
   template; include affected document paths, evidence, and any remaining gaps.
7. The other contributor reviews. Resolve feedback, verify the final result,
   merge, and follow the spec lifecycle and delivery rules in `spec-system.md`.

If both work on the same machine, use separate clones or worktrees so branch
switches do not affect the other's files. Never share a live working directory.

## Conflicts and handoffs

Fetch before integrating new `main` commits. On your feature branch, use
`git merge origin/main` to avoid rewriting an already shared branch. Resolve
conflicts against the latest accepted spec and contract; involve their owner if
intent conflicts. Run checks again after resolving conflicts. Do not force-push
shared branches or overwrite the other person's edits.

Record handoffs in the issue/PR: branch and commit, relevant spec/contract paths,
what works, evidence, remaining work, and blockers. Git syncs committed files;
uncommitted edits, local state, and Codex conversations do not transfer.

## Verification and delivery

For this documentation bootstrap, verify relative Markdown links, the guide copy,
ignore patterns, and `git diff --check`. There is currently no app test suite or
CI workflow. Add actual install/build/test commands and suitable CI with the first
runnable implementation; do not invent successful checks or make the demo depend
on a hosted CI runner having a GB10.

The GB10 integration owner must record an actual end-to-end local inference run
in the PR/issue, including source commit, environment, model, command, input, and
result. CPU mocks or laptop-only checks do not establish GB10 readiness. Keep
private data and large output artifacts outside Git, linking safe evidence.

For the demo, rehearse the accepted scenario and failure case on the target
machine. Track the repository submission, video, write-up, and feedback form in
the delivery issue; see `project-context.md` for the supplied event checklist.

Protecting `main`, enforcing PR review, and requiring CI are GitHub settings,
not effects of these files. Enable one approving review and actual required
checks when repository access and the chosen CI are available. Do not require
nonexistent CI checks.
