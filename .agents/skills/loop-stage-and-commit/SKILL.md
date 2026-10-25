---
name: loop-stage-and-commit
description: Split authorized workspace changes into atomic commits using targeted staging. Use when asked to stage and commit completed work, particularly when it contains multiple logical changes. Preserve unrelated collaborator changes.
---

# Loop, stage, and commit

Repository-shared adaptation of the contributor's personal skill. Use this copy
for AVocadoEyes; do not require a collaborator to install the personal version.
Follow the repository's AGENTS.md and docs/spec-system.md for SDD traceability.

## 1. Inspect and establish scope

- Run `git status --porcelain`, `git diff`, and `git diff --cached`. If HEAD
  exists, also inspect `git diff HEAD`; on an unborn branch, inspect the staged
  diff and relevant untracked files directly.
- Identify the changes authorized for this task, including anything already
  staged. Do not assume every dirty file belongs to this task or this contributor.
- If unrelated changes are already staged, stop before committing and report
  them. Do not unstage, stash, reset, or include them without authorization.
- Check that Git author identity is configured. Report missing identity instead
  of inventing one or changing global configuration.

## 2. Isolate one logical batch

- Separate distinct features, fixes, refactors, and formatting changes. Keep code,
  tests, and documentation together when they express one logical change.
- Review accidental debug artifacts and dead code within the authorized changes;
  preserve intentional application logging and unrelated edits.
- Stage explicit file paths with `git add -- <path>`. Never use `git add .`,
  `git add -A`, or wildcard staging. If a file contains unrelated hunks, stage
  only the authorized hunks; report a blocker if they cannot be isolated safely.
- Do not stage credentials, private data, model weights, runtime bundles, or
  dependency directories. Safe tracked configuration examples remain eligible.
- Inspect `git diff --cached` and run `git diff --cached --check`. Run the checks
  appropriate to the batch and report actual results before committing.

## 3. Commit concisely with SDD traceability

Use one imperative subject line, at most 72 characters, capitalized summary,
no trailing period:

```text
<type>: <Short imperative summary> (Refs #<issue>)
```

Types: `feat`, `fix`, `refactor`, `test`, `infra`, `docs`, `eval`, `chore`.
For tracked work, include the real issue reference in the subject so the
single-line convention retains SDD traceability. Do not invent issue numbers.
Tiny maintenance/bootstrap work may omit the reference when allowed by the
repository rules. If required traceability cannot fit in the subject, follow
the repository SDD requirements and include the needed body rather than drop it.
Never imply that a local commit alone represents completed team delivery.

```sh
git commit --cleanup=strip -m "<complete subject>"
```

Do not add unsolicited attribution trailers. `--cleanup=strip` cleans whitespace
and comments; it does not remove trailers or override commit hooks. Honor actual
repository checks and do not bypass hooks, signing, or execution permissions.

## 4. Verify and repeat within scope

After each commit, inspect `git status --porcelain` and the resulting commit.
Repeat for the remaining authorized logical changes only. Stop if a check or
commit fails, identity is missing, ownership is ambiguous, or no progress can
be made; report the blocker instead of retrying indefinitely.

Finish when all authorized changes are committed. A fully clean workspace is
expected only when no unrelated changes existed. List created commit hashes,
summaries, verification, and any remaining changes. This skill does not authorize
pushing, merging, amending others' commits, or rewriting shared history.
