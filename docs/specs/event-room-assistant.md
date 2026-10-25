# Event-room assistant

Status: Draft
Owner: Unassigned; assign the accountable product/code owner in the originating issue.
Related issue: Not created; link the real issue before acceptance/implementation.
Acceptance: Not yet accepted by the team.

## Outcome

Help an attendee choose **who to approach** in a networking room using visible
behavioral observations, with the goal of reducing unproductive interactions and
networking fatigue. Whether these cues improve interaction outcomes requires
evaluation; no personality or compatibility predictor is validated here.

## Proposed scope

- Agree on one room-observation scenario and a concrete user-visible result.
- Run the agreed observation and selection flow using local GB10 inference.
- Show the observations supporting a suggestion and acknowledge uncertainty.
- Rehearse one complete scenario and one insufficient-input/failure scenario.

## Non-goals

Conversation-opener generation and deciding when/how to approach are outside this
initial proposal. A profile-matching service alone does not fulfill the outcome.
Cloud inference is outside the supplied demo constraint.

## Proposed acceptance criteria

These require team agreement and concrete thresholds before `Accepted`.

| Criterion | Required evidence | Location or status |
|---|---|---|
| Given the agreed room input, the attendee can locate the suggested candidate(s) and inspect the supporting observations. | Reproducible demo with annotated expected observations and actual output. | Pending: choose input and output representation. |
| The app reports insufficient evidence or runtime failure without presenting a fabricated confident suggestion. | A weak-input case and an unavailable-inference case. | Pending: define failure behavior. |
| The complete demo's model inference executes locally on the GB10. | Source commit, model/version, config, command, input, output, and observed runtime evidence. | Pending: select and validate runtime. |
| Users can evaluate whether the suggestions help them choose whom to approach. | Agreed evaluation method, sample count, and success threshold. | Pending: owner defines measurable success. |
| The agreed input completes within a useful response time. | Measured end-to-end timings on the GB10. | Pending: set input size and latency target. |

## Risks and failure behavior

Occlusion, ambiguous cues, framing, and model error can make suggestions
unreliable. Define what the system observes versus estimates, and how it abstains.
Select appropriate demo inputs and decide consent, storage, retention, access,
and deletion before using identifiable footage. Privacy/security impact triggers
the guide's full-spec additions and a designated reviewer; this draft does not
authorize collection or decide those requirements.

## Decisions needed before acceptance

The originating issue must assign owner/implementer/reviewer, input and UI scope,
cue definitions, evaluation threshold, model/runtime, and file/interface ownership.
Add full-spec sections when triggered: context/options, dependencies/coordination,
data/compatibility/security/privacy/accessibility, rollout/rollback, observability
and ownership, and open questions with deadlines. Create machine-readable
contracts for supported interfaces or persisted formats when selected.

## Material direction changes

None recorded. Link the issue/PR/ADR rationale for material changes when useful;
Git preserves routine edits.
