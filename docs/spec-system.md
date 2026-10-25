# Local SDD rules

Audience: both contributors and coding agents. Owner: both repository
maintainers. Lifecycle: update through a reviewed PR when the process changes.

[sdd-guide.md](sdd-guide.md) is the checked-in, byte-for-byte copy of the guide
provided for this setup. It is the shared baseline; the external Windows path is
not a dependency. Propose guide updates in this repository so both people review
and receive them together. This file adds only local conventions.

## Planning and authority

Use GitHub Issues as the authoritative queue. The
[issue template](../.github/ISSUE_TEMPLATE/change.md) captures intent, ownership,
coordination, and verification. Do not maintain a second backlog in Markdown.

Apply the guide's triggers: routine internal maintenance can use a PR alone;
isolated reversible behavior changes need a change note (which may be in the
issue/PR); new capabilities, workflows, cross-module work, or uncertainty need a
lightweight spec. A full spec is required for supported external interfaces,
security/privacy impact, expensive migrations, cross-team/multi-system work, or
risky production rollout. Two contributors in one team do not alone require a
full spec. Add an ADR or contract only for its applicable trigger.

The initial [event-room spec](specs/event-room-assistant.md) is a draft discovery
starting point. Its privacy and retention choices may trigger full-spec additions
before implementation. No behavior, architecture, model, or acceptance is implied
by scaffolding this repository.

## Ownership and acceptance

Assign a real accountable owner and implementer in each issue/spec. The other
contributor normally reviews the PR. The accountable code owner accepts a change
note/lightweight spec; for an interface, data, privacy/security, or operations
trigger, explicitly name the designated reviewer in the issue. Either contributor
may fill these roles when appropriate; do not invent additional teams.

Use the guide's lifecycle: `Draft` → `Accepted` → `Implementing` → `Shipped`, or
`Superseded`. Record acceptance with the owner's name and issue/PR comment link,
including triggered reviewer agreement. Acceptance can be recorded in the issue;
no separate approval file is needed. Explicitly accepted scope can proceed
without repeatedly requesting the same acceptance. Process/bootstrap maintenance
does not require a product spec.

Use descriptive kebab-case paths and issue references, not a separate SDD ID.
Specs link to their issue. PRs link to the issue and every materially affected
spec/ADR/contract. Meaningful implementation commits contain `Refs #<issue>`.
Never fabricate a tracker reference when one has not been created.

## Shared changes and completion

One issue coordinates file/interface ownership. Parallel work can use separate
branches, but agree on a shared machine-readable interface before building both
sides. Changes to accepted scope or interfaces need owner agreement recorded in
the issue; update the same spec rather than creating personal copies. Keep active
specs current and accepted ADRs historical; supersede ADRs with a linked new ADR.

At review, compare each criterion with test/manual/measurement evidence. Update
architecture when boundaries or data flow change. For ML choices record the
model/version, input dataset/version, configuration, command, sample count, and
measured results needed to reproduce the decision; create an experiment brief
only when measured discovery is needed.

The PR is the delivery record. The other contributor reviews; applicable checks
pass; merge; complete any demo/release obligations; then mark the spec `Shipped`.
Use `Closes #<issue>` only when merge represents actual delivery. Otherwise use
`Refs #<issue>` and close after release evidence is linked. Retain shipped specs
only while they explain supported behavior or useful tradeoffs.
