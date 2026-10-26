# Editable pipeline workbench

Status: Implementing prototype at the user's explicit request. Team acceptance
and designated reviewer assignment remain pending; this is not a shipped demo.
Requesting contributor: satyagalla. Implementer: Codex.
Related issue: https://github.com/vrindaat/AVocadoEyes/issues/1
Related decision: [workbench proposal](../decisions/editable-pipeline-workbench.md).

The **Replacement requested: video JSON → text reasoning** section below defines
current user-authorized behavior and supersedes the older default workflow.
Earlier sections retain the legacy prototype's scope and verification history.

## Legacy prototype: outcome and scope

Upload an authorized clip, sample timestamped frames, observe visible cues,
validate evidence, extract text attributes and rank scene-linked candidates
against explicit user context.
Edit registered steps, model aliases, prompts, extra inputs and input mappings.
Run one step, a suffix or all steps. Preserve raw responses and original outputs;
human edits create separate revisions. Changes invalidate dependent results.
Preferences can reuse frozen observations. No training, arbitrary graphs, live
capture, automatic cross-run caching or cloud fallback.

## Acceptance criteria and verification

| Criterion | Evidence |
| --- | --- |
| Upload and preview ordered timestamped frames. | Synthetic video decode and HTTP tests. |
| Editable sequence/settings/inputs/prompts/models and registered extension steps. | Runner tests and local browser controls. |
| Clean outputs and optional returned reasoning; exact attempts retained internally for provenance. | Filtered inspection/history and tests. |
| Corrections preserve originals; upstream edits/failures invalidate downstream; preferences reuse observation. | Revision/invalidation tests. |
| Scene references, weak/occluded evidence, ambiguous IDs and malformed outputs validated. | Schema and cross-reference negative tests. |
| Local-only inference route with no automatic fallback. | Adapter tests and actual GB10/local Ollama text + synthetic image check passed; managed-route integration pending. |

## Interfaces and ownership

Version 1 schemas in `docs/contracts/` define editable pipeline configuration and
model output formats. Owner: repository maintainers, individual assignment pending
in issue #1. Breaking changes require a schema version change and migration;
CI validates examples and compatibility fixtures. Internal HTTP routes serve
only this local UI and are not an externally supported service.

## Privacy, access and retention

This full spec records privacy impact. Bind to loopback only; check Host, Origin
and a random session token before mutations. Require upload consent. Use one
local session, not multi-user hosting. Clips, frames, context and history remain
in memory; decoder files live in a temporary directory removed after decoding.
Reset or process exit clears the session. No automatic disk history or telemetry.
OS swapping and inference server retention remain operator concerns: use only
authorized demo clips. No secure-erasure claim. Never include credentials in
inspection. Keep local inputs and runtime configuration out of Git.

Bound video to 64 MiB, the first 60 seconds, 16 frames, width 960 pixels and a
45-second decode timeout. Bound model responses to 8 MiB. Errors halt execution
and invalidate dependent results. Reject invented evidence, ambiguous/duplicate
IDs and invalid boxes. Empty evidence abstains. Scores are experimental indices;
connection/enjoyment and effort/fatigue remain separate uncertain estimates.

## Options, dependencies and runtime

Adopt the proposed ordered runner with a standard-library local browser panel;
avoid a graph engine and an additional UI framework. `imageio-ffmpeg` supplies
video decoding and `jsonschema` validates contracts. One multimodal model can
serve all model passes. A single native Ollama chat adapter sends explicitly
configured image/text requests. The initial implementation used local Ollama
`qwen3.5:9b` for both passes. The requested extension below adds a third pass,
independent model selection, and defaults vision to `qwen3-vl:8b-instruct` while
keeping both text passes on `qwen3.5:9b`. No Internet use by the running pipeline.
Default route: `http://127.0.0.1:11434`. Require a local `/api/show` manifest with model
metadata and without remote model/host fields before every inference request.
Reject cloud model names, public addresses, redirects and external DNS names;
ignore HTTP proxy environment variables. Browser assets are bundled locally.
No runtime model downloads or Internet requests. Package/model installation is
an explicit preparation step before offline use. Set `OLLAMA_NO_CLOUD=1` on the
Ollama server too. Operators must still verify host placement and GB10 GPU use.
A managed proxy is optional and must expose `/api/show` and `/api/chat`; the
workbench does not configure or claim verification of NemoClaw/OpenShell.
Use native Ollama `think:false` by default and constrain observation/attribute/ranking
outputs with their JSON schemas, with those effective settings/prompts captured
for inspection. The initial compatibility-endpoint ranking probe returned no
final JSON, motivating this native-route choice. A second JSON-only probe had an
invalid field type; schema-constrained output addresses the interface error.
Contract and evidence checks still reject malformed or invented results.

## Rollout, rollback and open verification

Start with synthetic/authorized footage. Stop the process to discard session
state; revert the feature to roll back (no migration). Inspection provides concise errors and status; elapsed times remain internal. Before delivery, the other contributor reviews privacy and
interfaces and the team records exact GB10 model/runtime versions, managed-route
image forwarding, observation and ranking runs, latency and quality evidence.
Owner/reviewer assignments and target route remain open in #1. Execution does
not prove improved networking outcomes. Original event-room spec remains Draft.

## Local verification evidence (2026-10-25)

- `.venv/bin/python -m unittest discover -s tests -v`: 19 passed, including
  decoding, contracts, revisions, invalidation, modality checks, cloud manifest
  refusal, HTTP access controls and local adapter requests.
- `PLAYWRIGHT_BROWSERS_PATH=/tmp/avocadoeyes-browsers PYTHONPATH=. .venv/bin/python tests/browser_smoke.py`:
  passed browser upload, decoding, controls, corrections, context reuse, scene
  overlays, mobile layout and reset using synthetic data and a fixture model;
  zero external page requests. Browser development tools only:
  `playwright==1.64.1`, Chromium headless shell 156.
- `PYTHONPATH=. .venv/bin/python tests/local_model_smoke.py`: actual local
  `qwen3.5:9b` text JSON passed in 60.971 s, two-frame observation passed in
  78.4912 s. Synthetic color-pattern video has no people; ranking correctly
  abstained without invoking its model. This does not test real-room observation
  quality or unassisted ranking usefulness.
- Hardware: NVIDIA GB10, driver 580.178.04. `nvidia-smi` observed the local
  Ollama `llama-server` using 15801 MiB during the real ranking probe.
  Ollama 0.32.1; qwen3.5:9b Q4_K_M digest
  `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`.
  Python 3.12.3; imageio-ffmpeg 0.6.0 / FFmpeg 7.0.2-static; jsonschema 4.25.1.
- Launched loopback UI returned HTTP 200. Managed NemoClaw/OpenShell routing,
  real-room recommendation quality and useful demo latency remain unverified.

## Requested stage/output extension (2026-10-25)

The user explicitly requested clean model output with optional returned reasoning,
independent stage model selection, vision deciphering, intermediate processing,
and text attribute reasoning. Scope/coordination is recorded in issue #1; this
continues prototype implementation, with team review still pending.

Default flow: sample → observe (vision) → validate → process (text attributes)
→ rank (text reasoning). Only observe receives images. Process extracts concise
attributes with person/evidence references and uncertainty; rank consumes these
alongside original validated observations and attendee context. Invalid references
halt execution. Context edits reuse both observation and attribute results.
Each model stage selects an independent local tag, with suggestions for the four
user-reported installed Qwen models. Existing v1 configurations remain valid;
attribute output is an additive contract definition and rank accepts it optionally.

Browser inspection shows output and optional returned reasoning, concise status
and failures, and compact output history. Raw transport envelopes, requests,
manifest data, timings, hashes and duplicate parsed results stay out of browser
snapshots. Exact original attempts remain in memory for correction provenance.
Sampling uses the frame preview; validation uses a concise success message.
Verification: runner/contract/adapter tests plus browser smoke cover independent
selection, suffix invalidation, text-only processing, filtered success/failure
output and preserved originals. Real-model checks are separate from fixtures.

Extension verification on 2026-10-25 (working changes based on `42c29f1`, branch
`codex/pipeline-model-stages`):

- `.venv/bin/python -m unittest discover -s tests -v`: 24 passed. Includes
  three model routing, attribute evidence integrity, compact snapshots, reasoning
  extraction on parse failures, corrections, staleness and old v1 configuration.
- `PLAYWRIGHT_BROWSERS_PATH=/tmp/avocadoeyes-browsers PYTHONPATH=.:tests .venv/bin/python tests/browser_smoke.py`:
  passed with fixture models, including independent stage selection, filtered
  output/reasoning, upload, correction, context reuse and mobile layout; zero
  external browser requests.
- `PYTHONPATH=.:tests .venv/bin/python tests/local_model_smoke.py --text-stages`:
  real local `qwen3.5:9b` attribute extraction 8.2454 s and ranking 3.8407 s,
  one frozen synthetic observation fixture. Both contracts passed.
- `PYTHONPATH=.:tests .venv/bin/python tests/local_model_smoke.py`: local text
  probe passed (0.539 s); `qwen3-vl:8b-instruct` processed two synthetic color-test
  frames in 13.7004 s. Empty scene passed validation and correctly skipped model
  extraction/ranking with insufficient evidence. This does not test room quality.
- Local Ollama 0.32.1; NVIDIA GB10, driver 580.178.04. `/api/tags` confirmed all
  four user-reported models. Vision digest prefix `70e58e37beb1`, text digest
  prefix `56671c2ab938`. The two larger models were offered and fixture-tested
  for selection, not benchmarked with real inference in this extension.
- `git diff --check`: passed. Updated server started with
  `.venv/bin/python -m avocadoeyes --port 7861`; HTTP 200 and all five stages
  verified. The existing port 7860 session contains footage/history and was
  preserved. Neither session's footage/history was exported.

Real-room accuracy, outcome quality, managed routing, reviewer acceptance and
full demo readiness remain unverified. The default model sizes are configurable
starting points, not a benchmark-selected optimum.

## Replacement requested: video JSON → text reasoning (2026-10-25)

Status: Implementing at the user's explicit direction in the current conversation;
team review remains pending. Coordination: issue #1. Work on main, with no new
branches or worktrees unless explicitly requested by the user.

The default workbench now targets exactly two model calls. Upload a video file,
edit the video instruction and JSON Schema, inspect its JSON, then send that JSON
as text to a separately prompted reasoning model. Both prompts, video schema,
model selections and generation settings are editable. The reasoning answer is
free text. No mandatory ranking rubric, person contract or intermediate model
pass applies. Invalid JSON/schema output remains visible but cannot feed reasoning.
Changing video settings invalidates both results; changing reasoning settings
invalidates only reasoning. Rerunning reasoning reuses current video JSON.

User clarification: “i want to input video to the qwen model without sampling
frames.” Implementing under issue #1 at this explicit direction; team review
remains pending. Verification: count every decoded frame, check native processor
metadata and temporal grid for even/odd clips, reject over-limit clips without
sampling, then run unit/browser checks and synthetic GB10 inference.

Video uses the native Qwen3-VL Transformers processor's video-file modality,
with temporal frame sampling disabled. Every decoded frame remains in order;
native spatial resizing and temporal patch grouping/padding still apply. The app does not sample
JPEGs or silently substitute multi-image inference. Native local weights and a
CUDA-capable PyTorch/Transformers runtime must be prepared; Ollama GGUF weights
are not interchangeable. Text uses installed local Ollama models with thinking
enabled by default. Runtime model downloads and cloud fallback remain disabled.

The existing consent/loopback/access-token/in-memory retention boundary remains.
Uploaded bytes are written to a temporary video file only during native inference
and removed afterward, including failures. Native processing has a maximum-frame
rejection limit and spatial pixel budget. Clips exceeding the frame limit fail
explicitly rather than being sampled or truncated. The editable `max_frames`
setting defaults to 256 (allowed 2–4096), replacing `num_frames`. Memory/context
errors must not trigger a sampled retry. Existing sessions require fresh settings.
Legacy runner/configuration code is retained for compatibility with existing work;
it is not exposed as steps in the new default UI. No existing session is reset.

Verification required: two-call JSON handoff; editable schema enforcement and
malformed-output visibility; rerun invalidation; video-file modality at processor
boundary; HTTP controls and browser workflow; actual local GB10 video and reasoning
inference. Mock tests are not proof of native runtime or observation quality.

### Two-stage replacement verification (2026-10-25)

Implemented in the current main checkout; changes remain uncommitted and review
remains pending. Prior working edits and the existing 7861 session were preserved.
The new default service is running on 127.0.0.1:7860 with HTTP 200 and exactly
video/reason configuration sections. No branch or worktree was created for this
replacement. The user explicitly directed work on main.

- `.venv/bin/python -m unittest discover -s tests -v`: **30 passed**. New tests
  cover exact two-call JSON handoff, arbitrary user schema, invalid JSON/schema
  visibility and blocked handoff, prompt/schema invalidation, reasoning-only
  reuse, upload/reset, native video-message modality and missing-weight failure.
  The initial sandboxed invocation failed only on three socket-based tests;
  the same suite passed with local networking available.
- `PLAYWRIGHT_BROWSERS_PATH=/tmp/avocadoeyes-browsers PYTHONPATH=.:tests .venv/bin/python tests/two_stage_browser_smoke.py`:
  **passed**, fixture models. Covers consent/upload, both calls, visible outputs,
  reasoning-only reuse, schema/error display, reset, mobile layout, and zero
  external browser requests. An initial asynchronous test assertion was corrected
  to wait for the completed action before inspecting call counts.
- `PYTHONPATH=.:tests .venv/bin/python tests/native_video_smoke.py`: **passed**
  with the final native processor settings on NVIDIA GB10. A generated two-second
  320×240/10fps FFmpeg test-pattern MP4 was passed as a video-file content item to
  the Qwen3-VL processor. The adapter requires `pixel_values_videos`; image-mode
  fallback is refused. Configured native budget: 64 frames, 262144 pixels per
  frame, 256 output tokens. The original video remains input to the native
  processor; it owns temporal sampling and metadata.
- Final real video call: **154.639 s** including cold model load, returned valid
  custom-schema JSON describing the test pattern with `people_visible: false`.
  Local Ollama `qwen3.5:9b` reasoning with thinking enabled and 2048-token budget:
  **36.474 s**, correctly explained that the supplied observations provide no
  evidence about people. These timings are one integration run, not an isolated
  latency benchmark. Actual room accuracy, gesture/gaze reliability and useful
  demo latency remain unmeasured. An earlier pre-adjustment run also passed;
  the recorded final run uses explicit Transformers 5 processor kwargs and the
  corrected per-frame pixel budget.
- Native checkpoint: reused the already prepared ignored
  `models/Qwen3-VL-8B-Instruct` files; its existing download metadata identifies
  revision `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b`. No weights were downloaded
  by this change. Native runtime installed in `.venv`: PyTorch **2.9.1+cu130**,
  torchvision **0.24.1**, Transformers **5.20.2**, accelerate **1.15.0**,
  PyAV **16.1.0**. Direct requirements are pinned in `requirements-video.txt`.
  PyTorch warns that its reported architecture range ends at 12.0 while GB10 is
  12.1; both actual CUDA inference checks passed. This Transformers release uses
  torchvision/PyAV decoding when TorchCodec is absent and emits a deprecation
  warning; the pinned torchvision release retains that API. These are runtime
  compatibility limits to revisit when upgrading, not fallback to image input.
- `.venv/bin/python -m pip check`: **no broken requirements**.
  `git diff --check`: **passed**. HTTP 200 confirmed the running default UI.

No private footage was exported or used in automated checks. The previous
fixed observation/attribute/ranking contract is not imposed on this new workflow.
JSON/schema validity checks structure, not the truth of model observations.
