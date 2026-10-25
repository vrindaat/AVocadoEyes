# Editable pipeline workbench

Recorded: 2026-10-25.

Status: Proposed architecture following an assistant and subagent review. The
user requested this record; that request does not establish team acceptance of
the architecture or product specification.

Audience: AVocadoEyes contributors and reviewers. Accountable owner and reviewer:
unassigned; record actual assignments and acceptance in the implementation issue.
Related issue: none supplied or created for this documentation request; link the
real originating issue before acceptance or implementation.

## Context and requested capability

The user wants a pipeline that accepts video, allows models to be interchanged,
accepts editable prompts and additional model inputs, permits new processing
steps between models, and displays intermediate outputs and explanations.

This workbench supports developing AVocadoEyes: choosing **who to approach** from
video and known user information, with the aim of worthwhile conversations within
a limited energy budget. The attendee-facing result must locate suggested people
in the original scene and show personalized reasons, evidence, and uncertainty.
A generic workflow editor alone would not deliver that outcome. Uploaded clips
are an initial milestone; live event video remains the intended product input.

Authoritative context and evidence:

- [Project context](../project-context.md): inference only, local GB10 execution,
  proposed two-pass flow, working model shortlist, and unverified runtime state.
- [Research decisions](research-scope-and-evidence-decisions.md): user direction,
  candidate attributes, and selections that remain open.
- [Agent design and validation](../research/agent-design-and-validation.md):
  observation, interpretation, personalized outcome, and energy distinctions.
- [Draft event-room spec](../specs/event-room-assistant.md) and
  [architecture](../architecture.md): current scope and implementation status.

## Options considered

| Option | Assessment |
| --- | --- |
| Hardcoded video-to-ranking script | Small, but insufficient for the requested insertion of steps, model swapping, and inspection. |
| Ordered Python steps with configuration and a local control panel | Proposed starting point: preserves requested flexibility with a bounded implementation. |
| LangGraph-based general graph runner and editor | Defer until demonstrated needs for branching, loops, or resumable execution justify it. Not inherently unsuitable, but unnecessary for the initial sequence. |

## Proposed decision

Build a small ordered Python step runner and a local control panel. Each step is
a registered function with explicit inputs, settings, and outputs. Configuration
selects step order, model aliases, prompt files, input mappings, and options.
Inserting a step means registering its function and adding it to the sequence;
swapping a model means changing its configured alias/settings after checking
modality and output compatibility.

```text
Local control panel
  -> ordered Python step runner
  -> video -> timestamped frames -> observe -> validate -> rank
  -> scene-linked candidate ordering, evidence, and unknowns

Optional human correction -> new input revision -> rerun downstream steps
Model steps -> one verified local inference adapter
Run inspection -> inputs, prompts, responses, parsed outputs, errors, timings
```

Start with one multimodal model reused for observation and reasoning. A second
model is a comparison option, not a required second service. The recorded model
shortlist remains a candidate list until verified on the GB10; this record does
not select or download a model.

Gradio is a candidate local control panel, not an accepted dependency. Initial
controls should include video/frame preview, step configuration, model selection,
prompt and additional-input editors, output inspection, and **Run step**, **Run
from here**, and **Run all**. Keep the same execution functions for experimentation
and the attendee-facing demo.

### Research behavior to preserve

- Keep the initial observation pass independent of attendee preferences. Preserve
  ordered timestamps, stable person IDs where possible, source frames, recipients,
  visibility, ambiguity, and alternative explanations. Retain frames for targeted
  reinspection when the observation summary omits needed evidence.
- Distinguish visible observations, inferred/apparent traits, user impressions,
  and outcome estimates. Distinguish presence, observed absence, and unobservable
  evidence. Observation confidence does not establish outcome confidence.
- Feed explicit user personality/preferences, goals, current state, and a
  research-based rubric into personalized reasoning. Keep enjoyment/connection
  and effort/fatigue considerations distinct; candidate animation alone does not
  establish energy cost.
- Make candidate personality inference optional. Permit comparison of direct
  cue-based reasoning with reasoning through uncertain trait estimates. Final
  cues, instruments, weights, and cutoffs remain open user/team selections.
- Treat scores as experimental preference indices. Do not import paper
  coefficients as production weights or report calibrated success probabilities
  without supporting evaluation. Research citations motivate hypotheses rather
  than certify an individual prediction.
- Require traceable evidence and insufficient-evidence behavior. Sparse sampled
  frames cannot establish precise motion measurements or silent speech content.
- Request concise explanations with evidence references and uncertainty. Preserve
  any explanation/reasoning field actually returned by the backend; full internal
  model reasoning is not guaranteed or required for the workbench.

### Inspection, editing, and reruns

Capture exact step inputs, model identity/settings, prompts, raw responses, parsed
outputs, errors, and elapsed time. Preserve original model outputs. A human edit
creates a separately identified revision; downstream outputs record the revision
they consumed. Corrected observations must not be presented as unassisted model
accuracy.

Initially, keep completed outputs available within the run and provide explicit
reruns from a chosen step. Mark affected downstream results as stale when an
upstream input, prompt, setting, or output revision changes. Changing only user
preferences can reuse observations and rerun ranking. Automatic content-based
caching and cross-run dependency tracking are deferred.

Inspection does not imply unrestricted disk persistence. Decide consent, storage,
retention, access, and deletion before retaining identifiable video, frames, or
personal profiles. Keep private inputs and runtime artifacts out of Git.

### Local inference and NemoClaw boundary

The runner explicitly controls the processing sequence. NemoClaw is not assumed
to schedule every Python step. The context's proposed model-request path is
application/OpenClaw -> managed OpenShell inference route -> local host model
server -> GB10 GPU.

Implement one adapter against the selected, verified local route. Verify image
forwarding, text requests, model selection, exposed settings, and any required
actual tool execution. The adapter must not silently bypass the selected managed
route or fall back to cloud inference. Exact process placement, backend, versions,
and model-switching behavior remain unselected pending target-machine evidence.

## Scope deliberately deferred

Defer arbitrary graphs, drag-and-drop editing, dynamic branching, parallel model
scheduling, automatic plugin discovery, a catalog of backend implementations,
persistent automatic cache invalidation, and a database-backed run service.
Preserve small extension points without building these systems in advance.
Training, fine-tuning, and reinforcement learning are outside the recorded
inference-only direction.

## Verification before claiming delivery

Record outcome, ownership, acceptance criteria, and verification in the real
implementation issue and update the draft spec before feature implementation.
Define the minimum machine-readable contracts needed for supported interfaces
or persisted formats, and update architecture when boundaries are adopted.

Verify that a user can upload a clip, inspect sampled frames, change a model or
prompt, insert a processing step, inspect original outputs, make a marked human
correction, and rerun the affected sequence. Demonstrate that preference changes
reuse observations and that stale results are not presented as current.

For the product scenario, demonstrate a scene-linked personalized ordering and
evidence, plus weak/occluded input, ambiguous candidate IDs, malformed model
output, and unavailable-inference behavior. Record exact versions, inputs,
commands, outputs, and end-to-end timings on the GB10. Host model listing or a
successful text response alone does not prove the complete managed video path.

Evaluate observation quality separately from ranking usefulness. Compare rankings
using identical frozen observations and user inputs; separate human-edited runs.
Research-guided versus unguided prompts and direct-cue versus trait-mediated
reasoning are useful comparisons. A successful pipeline execution does not prove
that recommendations improve actual conversation enjoyment or reduce fatigue.
No runtime, accuracy, latency, or user-outcome results have been established by
this review.

## Consequences and revisit conditions

This approach preserves the requested experimentation controls while prioritizing
the complete AVocadoEyes flow over a general workflow platform. Adding a new
processing type initially requires Python code; a model alias alone cannot make
incompatible models interchangeable.

Revisit the runner choice if actual experiments need conditional loops, branching,
durable resume, or parallel execution. Revisit the local UI when live capture and
attendee usability requirements are agreed. Record actual owner/reviewer
acceptance and measured evidence rather than treating this proposal or its
assistant/subagent review as team approval.
