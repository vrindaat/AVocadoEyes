# Architecture

Audience: implementers and reviewer. Owner: accountable code owner (assign with
the first implementation issue). Lifecycle: update whenever boundaries,
ownership, topology, or material data flow change.

## Current state

The local workbench prototype implements the
[workbench spec](specs/editable-pipeline-workbench.md) under user direction in
[issue #1](https://github.com/vrindaat/AVocadoEyes/issues/1). Team review and
GB10 inference verification remain pending.

```text
Bundled browser UI -> loopback HTTP server -> ordered Python runner
video -> timestamped JPEGs -> observe -> validate -> rank
model steps -> local Ollama manifest check -> local Ollama chat -> GB10 GPU
correction -> separate human revision -> stale downstream -> explicit rerun
```

`runner.py` owns execution, attempt history, lineage and staleness. `video.py`
bounds decoding and deletes temporary files. `contracts.py` validates versioned
configuration/output JSON schemas and scene references. `inference.py` forwards
image/text requests to one local route. `server.py` checks Host, Origin and an
ephemeral request token and binds only to loopback. All browser assets are local.
The browser and CLI route check share execution functions.

The user selected local Ollama `qwen3.5:9b` for both passes at
`http://127.0.0.1:11434`. The pipeline performs no model downloads or Internet
requests. It ignores HTTP proxies and refuses public IPs, external DNS names,
redirects, cloud model names and remote model manifests. `/api/show` must confirm
local model metadata before every chat. Set `OLLAMA_NO_CLOUD=1` on the Ollama
server too; the workbench cannot prove target placement or GPU use.

NemoClaw/OpenClaw/OpenShell may surround the local service, but do not schedule
Python steps. An explicit managed endpoint must forward `/api/show` and
`/api/chat` including images. There is no automatic route bypass. Native Ollama
JSON/schema output and `think:false` avoid an empty final answer from an exhausted
thinking budget. Returned thinking fields are preserved when present.

Configuration selects order, model aliases, prompts, settings, extra inputs and
`$step.field` references. Trusted Python modules register extension kinds via
`--plugin`; there is no graph engine, automatic discovery or cross-run cache.
Attempts preserve exact inputs/prompts/settings, original raw responses (including
returned explanation fields), parsed results, errors, timings and revision IDs.
Human revisions retain original attempts and propagate a human-assisted marker.
Upstream edits/failures stale the suffix; context can reuse frozen observations.
Inspection JSON hashes images to avoid repetition; exact images remain in memory.

Consent is required before upload. A new video discards the previous scene's
history. Reset/exit clears in-memory footage, frames and context. No database,
automatic export or request logging. OS swapping and model-server retention are
operator concerns. Actual GB10 inference, managed routing, exact runtime versions,
quality and useful demo latency remain unverified. Direct GB10/Ollama text and
two-frame synthetic observation checks passed, with GPU process use observed;
see the workbench spec for exact versions and timings. Fixture execution does
not prove outcomes or managed routing.

## Intended constraints and open boundaries

Per [project context](project-context.md), application inference and the final
demo run locally on the GB10. NemoClaw/OpenClaw/OpenShell and Ollama are the stack
being prepared in prior chats; their exact integration and versions remain open.
Codex assists development; its account settings and chats are not app runtime
dependencies or the authoritative shared requirements.

Broader product flow, still pending product acceptance:

```text
room image/video -> local visual observation -> candidate selection
                 -> attendee-facing view with evidence and uncertainty
```

Before implementation, decide capture/input handling, observation representation,
selection criteria, presentation, retention, and the runtime/tool boundary. Assign
one owner per boundary in the issue, with the other contributor reviewing any
shared interface. Define supported interfaces in machine-readable contracts
before parallel producer/consumer implementation. This does not assign either
person to a fabricated module or imply that the pipeline already exists.

Record durable choices in ADRs only when decided. For retained video/images,
security/privacy decisions, or supported external APIs, expand the spec according
to the full-spec triggers in the guide.
