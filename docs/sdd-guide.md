# Practical Specification-Driven Development Guide

## Purpose

This guide helps a person or team turn ideas into safe, verifiable changes without turning documentation into a tax on delivery. It applies to production and internal software. Research, ML, and incident work use the extensions described below only when applicable.

The goal is shared understanding, safe change, and an easy handoff to the next maintainer. Planning scales with risk, uncertainty, reversibility, and coordination—not ceremony. Use the issue tracker, pull requests, and Git as the traceability system already present; do not create a second registry of work.

## Principles

- Use the lightest artifact that meaningfully reduces risk or ambiguity.
- State the intended outcome and evidence of success before implementation begins.
- Keep active specifications current while work is underway. Preserve decisions and investigations as historical records.
- Prefer executable evidence: tests, schema validation, reproducible experiments, deployment checks, and production observations.
- Give each current fact one authoritative home; link instead of duplicating it.
- A document is useful only when it has a clear audience, owner, lifecycle, and purpose.
- Preserve history through Git, issues, pull requests, and releases; record durable rationale in ADRs rather than maintaining manual change logs.

## Minimum Repository Structure

Start with only the directories the project needs:

```text
README.md                       Project entry point
AGENTS.md                       Short rules for coding agents and links to docs/

docs/
  architecture.md               Intended current boundaries, data flow, and ownership
  contributing.md               Setup, development, testing, review, and release process
  spec-system.md                Local rules that supplement this guide
  specs/                        Active and retained useful specifications
  decisions/                    Architecture Decision Records (ADRs)
  contracts/                    Versioned machine-readable supported interfaces
```

Add `investigations/`, `research/`, or `templates/` only when there is an owner and a real workflow for them.

The issue tracker or project board is the authoritative task queue and the entry point for tracked work. Do not create a status document that duplicates it.

## Choose the Planning Level

Start with an issue for a feature, behavior change, non-trivial bug, decision, or work likely to span multiple commits. The issue states the intent and verification. A tiny, isolated maintenance change may use its commit or PR description instead. Add an artifact only when one of the following rules applies.

| Artifact | Create it when | Minimum required content |
|---|---|---|
| No separate artifact | The change is an internal refactor, routine dependency update, typo, or isolated bug fix with no changed supported behavior, data, interface, security posture, or rollout risk. | Issue or PR intent and verification. |
| Change note | Supported behavior changes, but the change is isolated, reversible, and has no trigger below. | Intent, affected area, verification, issue or PR link. |
| Lightweight spec | A new capability, changed user workflow, cross-module change, migration, or non-trivial uncertainty is involved. | Outcome, scope, non-goals, acceptance criteria, risks, verification. |
| Full spec | Any one of these applies: cross-team coordination; an externally consumed interface; an expensive-to-reverse migration; security or privacy impact; production rollout requiring staged release, monitoring, or rollback; or a change spanning more than one independently owned system. | Lightweight spec plus options, dependencies, rollout, rollback, observability, and ownership. |
| ADR | A decision will constrain future architecture, product behavior, data design, or security posture beyond the current implementation. | Context, options, decision, consequences, revisit trigger. |
| Contract | A supported API, event, integration, or persisted format changes. | Versioned machine-readable schema, owner, compatibility policy, validation. |
| Experiment brief | A decision cannot responsibly be made without research, a prototype, or measured evaluation. | Hypothesis, method, evidence threshold, decision rule, reproducibility details. |
| Incident report | A significant failure, near miss, or investigation needs lasting evidence or follow-up. | Timeline, evidence, impact, findings, follow-up links. |

Artifacts combine when their triggers apply. A full spec for an API migration, for example, also requires a contract; add an ADR only if the migration establishes a durable design decision.

When unsure between two levels, choose the lower level and record the reason. Escalate if uncertainty, scope, or risk increases during delivery.

## Standard Workflow

```text
Request or opportunity
  -> select the smallest required artifact
  -> state intended outcome and verification
  -> obtain the required acceptance
  -> implement in small, reviewable increments
  -> validate, release, and observe when applicable
  -> update the active specification if material learning changes it
  -> record durable decisions and retain useful evidence
```

A specification may change during delivery. Record a material change to scope, assumptions, interface behavior, risk, or success criteria only when its reason is not clear from the linked issue, PR, or ADR; Git preserves ordinary edits.

## Traceability and History

Use existing work records as a linked graph. The issue is the hub for a feature or other tracked change; specifications, decisions, contracts, pull requests, commits, and releases remain independent records with their own purpose.

```text
issue
  ├─ specification, when planning is needed
  │    ├─ ADR, when a durable decision is made
  │    └─ contract, when a supported interface or persisted format changes
  └─ PR or closing commit
       ├─ implementation and tests
       ├─ CI and review evidence
       └─ release or incident follow-up, when applicable
```

Do not create a separate SDD identifier, document registry, or manual project history. Use the issue reference, document path, PR, release record, and Git history that already exist.

### Required links

- A specification or ADR links to its originating issue. A contract links to it when its format supports metadata; otherwise the PR or final delivery commit provides that link.
- A team PR links to its issue and lists the specifications, ADRs, and contracts it materially implements or changes.
- A solo engineer's final delivery commit links to the issue and lists those documents once.
- Every meaningful implementation commit references its tracked issue, for example `Refs #482`. Use the tracker syntax appropriate to the project.
- The final PR or delivery commit uses the tracker closing syntax, for example `Closes #482`, only when landing it represents delivery and the work is actually complete. If release happens later, use `Refs #482` and close the issue after release evidence is available.

Do not require documents to link back to every PR or commit. The PR or closing commit, Git history, and issue provide that reverse navigation without document churn.

### Multiple specifications under one issue

An issue may legitimately contain multiple specifications and many commits. In that case, list every materially affected document in the PR or final delivery commit. Prefer separate PRs for independently releasable specifications when practical.

If commit-level precision is necessary for a multi-spec issue—for example, for an audit, migration, or complex investigation—add the relevant path only to the meaningful implementation commit:

```text
feat(billing): add retry eligibility check

Refs: #482
Spec: docs/specs/billing-retry.md
```

For a commit that implements two specifications, use repeated `Spec:` lines or a `Specs:` list. Do not require this for formatting, renames, or other mechanical support commits. A code-only commit cannot be reliably mapped to a requirement after the fact, so record this optional link only when the additional precision is worth its cost.

### Team workflow

```text
Issue -> spec / ADR / contract when triggered -> commits reference issue
      -> PR lists affected docs and verification -> review, merge, release -> issue closes
```

The PR is the normal semantic delivery record. It should contain the issue link, affected document paths, review discussion, CI evidence, and rollout evidence where applicable. Use an issue-closing link only when merge represents delivery; otherwise use a reference link and close the issue after release. Squash and rebase workflows are supported because the durable PR record preserves the mapping even when intermediate commits do not remain on the default branch.

Use this minimum PR body when a tracked change has related documents:

```markdown
Closes #<issue>                  # or Refs #<issue> when release is separate

Documents changed or implemented:
- docs/specs/<spec>.md
- docs/decisions/<decision>.md       # when applicable
- docs/contracts/<contract>          # when applicable

Verification:
- <test, CI run, manual check, metric, or rollout evidence>
```

### Solo-engineer workflow

```text
Issue -> spec / ADR / contract when triggered -> commits reference issue
      -> final delivery commit lists affected docs, verification, and closes issue
```

The final delivery commit is the PR-equivalent. It updates the implementation, tests, and applicable document status, then closes the issue when delivery obligations are complete. For example:

```text
feat(billing): retry eligible failed invoices

Closes #482
Specs: docs/specs/billing-retry.md
Contract: docs/contracts/billing-events.json
```

If the tracker does not close issues from a direct commit, close the issue after the final commit and link that commit in the issue. Do not create a separate delivery-note document.

## Roles and Acceptance

- **Author:** writes and keeps the artifact current.
- **Accountable owner:** accepts scope, tradeoffs, and final outcome. This may be the author.
- **Implementer:** delivers the change and verification evidence. This may be the author.
- **Reviewer:** validates code and the artifact only when a review trigger applies.

For a solo engineer, the author is accountable and may accept their own artifact. The acceptance is the recorded status change and rationale; it does not require a ceremonial self-review.

For a team, the normal code owner accepts a change note or lightweight spec. Obtain an additional reviewer only for the relevant trigger:

| Trigger | Additional reviewer |
|---|---|
| Supported interface or consuming system | Owning or consuming team |
| Security, privacy, or access control | Security owner or designated reviewer |
| Persisted data or migration | Data/system owner |
| Production rollout, capacity, or on-call impact | Operations/on-call owner |

A spec is `Accepted` when its accountable owner and any triggered reviewers agree that its outcome, risks, and verification are sufficient to begin. It is `Shipped` when the applicable definition of done is complete.

## Templates

### Change Note

```markdown
# <Change>
Owner:
Related issue:

## Intent

## Affected area

## Verification
```

### Lightweight Specification

```markdown
# <Feature or change>
Status: Draft | Accepted | Implementing | Shipped | Superseded
Owner:
Related issue:

## Outcome
Who benefits, what observable result changes, and why it matters.

## Scope

## Non-goals

## Acceptance criteria
Use Given/When/Then for behavior where useful. Use measurable statements for
non-functional outcomes such as performance, accessibility, reliability, or operations.

| Criterion | Evidence | Location or status |
|---|---|---|
| | Test, manual check, metric, or reason it cannot be automated | |

## Risks and failure behavior

## Material direction changes
Record only a changed decision, scope, assumption, interface behavior, risk, or success criterion that cannot be understood from the linked issue, PR, or ADR. Git preserves ordinary document edits.
```

### Full Specification Additions

```markdown
## Context and constraints
## Options considered
## Dependencies and coordination
## Data, compatibility, security, privacy, and accessibility impact
## Rollout and rollback
## Observability and operational ownership
## Open questions and decision deadlines
```

### Architecture Decision Record

```markdown
# <Decision>
Status: Accepted | Superseded
Date:
Owner:
Related issue:
Related specification:

## Context
## Options considered
## Decision
## Consequences
## Revisit if
```

Accepted ADRs are not rewritten. A later ADR supersedes an earlier one and links to it.

## Contracts and Compatibility

Use a machine-readable contract for supported APIs, events, persisted data, and integrations. Every contract must define:

- A version and owner.
- Consumers and compatibility expectations.
- What constitutes a breaking change.
- Validation in CI, including compatibility tests where practical.
- A deprecation and migration path for breaking changes.

Source code is not a substitute for an intentionally owned public or persisted contract.

## Definition of Done

Every change is complete only when:

- The intended behavior is stated in the issue, PR, or specification.
- Relevant verification evidence exists and is linked from that artifact.
- Applicable CI checks pass; required code review also passes for team work.
- The team PR is merged, or the solo engineer's final delivery commit is on the delivery branch.

Add these obligations only when their trigger applies:

| Trigger | Additional completion obligation |
|---|---|
| Supported interface or persisted data changed | Contract, compatibility validation, and migration/deprecation path are complete. |
| Architecture, product, data, or security decision will constrain future work | ADR is recorded. |
| Production rollout risk | Rollout, monitoring, and rollback obligations are complete. |
| System boundary, ownership, or data flow changed | `architecture.md` is updated. |
| Research or ML decision | Reproducibility and measured evidence are recorded. |
| Incident or near miss with durable learning | Incident report and follow-up links are recorded. |

Mark an active spec `Shipped` at completion. Close a change note in its issue, PR, or final delivery commit with its verification evidence.

## Source of Truth

Different sources answer different questions:

| Question | Authoritative source |
|---|---|
| What is deployed or happening now? | Deployed configuration and production observation |
| What behavior is intentionally supported? | Current accepted specification or versioned contract |
| Why was a durable choice made? | ADR |
| Does the implementation conform to intended behavior? | Tests, contract validation, and release checks |
| What is the intended current design and ownership? | `architecture.md` |
| What work delivered a feature, and in what order? | Issue, linked PR or closing commit, release record, and Git history |

Tests are evidence of conformance, not the final authority for intended behavior; a passing test can encode an outdated requirement or defect.

When sources disagree, treat the mismatch as a defect: establish actual state, decide intended state with the accountable owner, correct the implementation or documentation, and record an ADR if the decision is durable.

## Lifecycle and Maintenance

- Give a spec, ADR, or contract a short, descriptive kebab-case path. Its path is its lightweight reference; do not introduce a separate document-ID system.
- Avoid renaming an accepted document casually. When its subject materially changes, supersede it or create a new document and link the old one. Git preserves the historical path and content.
- A specification or ADR links to its originating issue. A contract uses that link when its format supports metadata; otherwise the PR or final delivery commit is the source of the relationship. A PR or final delivery commit names the documents it materially implements or changes.
- Review an active spec at team PR merge or in the solo engineer's final delivery commit. Mark it `Shipped`, `Superseded`, or close it as abandoned. Do not leave completed work in an active state.
- Retain a shipped spec only when it explains a supported capability, non-obvious behavior, or durable tradeoff. Otherwise, rely on the closed issue/PR and remove the redundant artifact.
- Update `architecture.md` whenever a system boundary, ownership, deployment topology, or material data flow changes.
- The author owns updating an active artifact. The accountable owner assigns a new owner or archives an artifact when it no longer has a current audience or lifecycle.

## Emergency Changes

For an active incident or urgent security mitigation, stabilize the system first. Record intent, risk, and verification in the incident and team PR or solo final delivery commit before the emergency change is closed. Create any triggered incident report, specification, ADR, contract update, and follow-up work after stabilization.

Urgency changes sequencing; it does not remove accountability.

## Optional Extensions

Use an experiment brief only for work that needs measured discovery before implementation. It should contain the decision it informs, hypothesis, method and controls, data/evaluation plan, success or failure threshold, decision rule, and reproducibility details: source commit, environment, dataset/split version, seed, command/configuration, artifact identifiers, sample count, and results.

Use an incident report only when a failure or near miss has durable learning. It should preserve the timeline, evidence, impact, findings, and follow-up links. It is a historical record and does not silently redefine current architecture.

## Adoption

Adopt this system prospectively. Do not stop delivery to create a complete historical archive. Begin by adding intent and verification to every issue or PR, then make the issue reference part of meaningful commit messages. Add PR-level document links for team work or document links in the final delivery commit for solo work. Use the decision rules for new work, create ADRs for new durable decisions, and document contracts and architecture as the relevant areas are changed.

Do not create documents to satisfy the process. Create them when they help someone make, review, implement, operate, or safely revisit a decision.
