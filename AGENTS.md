# AVocadoEyes: shared Codex instructions

This is a two-person Dell × NVIDIA hackathon repository. These tracked instructions
apply to both contributors and their Codex sessions.

- Start with [README.md](README.md), then read the relevant accepted spec and
  [architecture](docs/architecture.md) before changing behavior.
- Follow [the SDD guide](docs/sdd-guide.md) and
  [local SDD rules](docs/spec-system.md). Use the smallest required artifact.
- [Project context](docs/project-context.md) preserves the founder's intent and
  hackathon constraints. The product focuses on **who** to approach at an event.
  Do not silently replace it with a conversation-opener or profile-matching tool.
- Issues are the work queue. Specs and contracts define supported intent;
  GitHub issues/PRs and Git preserve progress and handoffs. Do not add a parallel
  task board, session memory log, numbered SDD registry, or duplicate plan system.
- Before feature implementation, record outcome and verification in the issue
  and required artifact. Draft specs are proposals, not accepted requirements.
  Record actual owner/reviewer acceptance; never invent agreement or issue IDs.
- Do not create worktrees for any changes unless the user explicitly requests one.
  Work in the current checkout and use one branch per change. Check status and
  fetch before starting; preserve the other contributor's changes. Coordinate
  overlapping files and interfaces in the issue before editing them. This rule
  takes precedence over worktree guidance in linked documents.
- Meaningful implementation commits reference the issue (`Refs #<issue>`).
  PRs list affected specs/ADRs/contracts and verification. Follow
  [contributing](docs/contributing.md) for review, merge, and handoff.
- When staging and committing completed work, use the repository-shared
  [loop-stage-and-commit skill](.agents/skills/loop-stage-and-commit/SKILL.md).
  Use this version for this repo if a personal skill has the same name.
- Application inference and the final demo must run locally on the GB10 per the
  organizer checklist in project context. Do not add a silent cloud fallback.
  Model, framework, and runtime versions are unselected until verified.
- Treat behavioral interpretations as hypotheses. Distinguish observed cues,
  model estimates, and measured outcomes; do not claim validated personality,
  compatibility, or networking value from appearance without evidence.
- Keep credentials, private footage, model weights, runtime state, and personal
  Codex settings out of Git. Track safe configuration examples when needed.
- Run checks appropriate to the change, report exact commands/results and gaps,
  and update affected active specs/contracts/architecture. There is no application
  build or test command yet; do not report one as passing.

Process edits use the same PR review as code so both contributors adopt one SDD.
