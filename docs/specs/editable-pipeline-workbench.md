# Editable pipeline workbench

Status: Implementing prototype at the user's explicit request. Team acceptance
and designated reviewer assignment remain pending; this is not a shipped demo.
Requesting contributor: satyagalla. Implementer: Codex.
Related issue: https://github.com/vrindaat/AVocadoEyes/issues/1
Related decision: [workbench proposal](../decisions/editable-pipeline-workbench.md).

## Outcome and scope

Upload an authorized clip, sample timestamped frames, observe visible cues,
validate evidence and rank scene-linked candidates against explicit user context.
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
| Exact step inputs, outputs, prompts, raw responses, errors, timings and revisions. | Inspection history and tests. |
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
serve both passes. A single native Ollama chat adapter sends explicitly
configured image/text requests. The user subsequently selected local Ollama
`qwen3.5:9b` for both passes and no Internet use by the running pipeline. Default
route: `http://127.0.0.1:11434`. Require a local `/api/show` manifest with model
metadata and without remote model/host fields before every inference request.
Reject cloud model names, public addresses, redirects and external DNS names;
ignore HTTP proxy environment variables. Browser assets are bundled locally.
No runtime model downloads or Internet requests. Package/model installation is
an explicit preparation step before offline use. Set `OLLAMA_NO_CLOUD=1` on the
Ollama server too. Operators must still verify host placement and GB10 GPU use.
A managed proxy is optional and must expose `/api/show` and `/api/chat`; the
workbench does not configure or claim verification of NemoClaw/OpenShell.
Use native Ollama `think:false` by default and constrain observation/ranking
outputs with their JSON schemas, with those effective settings/prompts captured
for inspection. The initial compatibility-endpoint ranking probe returned no
final JSON, motivating this native-route choice. A second JSON-only probe had an
invalid field type; schema-constrained output addresses the interface error.
Contract and evidence checks still reject malformed or invented results.

## Rollout, rollback and open verification

Start with synthetic/authorized footage. Stop the process to discard session
state; revert the feature to roll back (no migration). Inspection provides errors
and elapsed times. Before delivery, the other contributor reviews privacy and
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
