# AVocadoEyes

**See the room. Choose who to approach.**

AVocadoEyes is a local AI prototype for the Dell × NVIDIA AI Hackathon that helps
an attendee decide **who to approach** at a networking event. It combines visible
behavioral cues from a room video with the attendee's goals, preferences, and
energy budget to suggest people to consider—with supporting evidence and uncertainty.

## Why AVocadoEyes

A room full of people offers more possible conversations than anyone has time
or energy for. After several conversations that go nowhere, choosing the next
person can feel exhausting.

AVocadoEyes explores whether visible interaction patterns can help make that
choice more intentional. The aim is more worthwhile interactions within the
attendee's limited time and energy budget. That benefit remains a product
hypothesis to evaluate.

## How it works

```text
Room video → Timestamped frames → Visual observations → Evidence validation
                                                               ↓
Attendee goals + preferences + energy budget → Personalized ranking
                                                               ↓
                                     Scene-linked suggestions + uncertainty
```

The visual observation and attribute-processing passes run independently of
attendee preferences. Ranking then uses their outputs and the attendee's context
to weigh potential connection/enjoyment and effort/fatigue separately. Suggestions link back to
person IDs, locations in sampled frames, and the cues behind the recommendation.

Visible cues are observations; interpretations of vibe or fit are uncertain
model estimates. Preference scores are experimental indices, not probabilities
of success. The prototype does not establish personality, compatibility, or
networking value from appearance. Insufficient evidence can produce no suggestion.

## What is built

- A browser workbench for uploading authorized clips and viewing sampled frames.
- Editable pipeline steps, models, prompts, settings, and input mappings.
- Scene-linked rankings with supporting cues, alternative explanations, and uncertainty.
- Step-by-step execution, reusable observations when preferences change, and human
  corrections that preserve originals and mark dependent results stale.
- Local inference through Ollama, with `qwen3-vl:8b-instruct` configured for vision
  and `qwen3.5:9b` for processing and ranking, bundled browser assets, and no
  automatic cloud fallback.

**Current state:** an experimental workbench. Local GB10 text inference and a
two-frame synthetic observation check have passed, with GPU use observed.
Real-room recommendation quality, useful end-to-end latency, and managed
NemoClaw/OpenShell routing remain unverified. See the
[verification evidence](docs/specs/editable-pipeline-workbench.md#local-verification-evidence-2026-10-25)
for exact versions, timings, and limits.

## Run locally

The commands below target the Linux GB10 host. Prepare Python 3.12, local Ollama,
and the models before offline use. The running pipeline uses only local services
and bundled assets; it does not download models.

Clone the repository, then install dependencies:

```sh
git clone https://github.com/vrindaat/AVocadoEyes.git
cd AVocadoEyes
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
# Preparation only, if not already installed:
ollama pull qwen3-vl:8b-instruct
ollama pull qwen3.5:9b
```

Set `OLLAMA_NO_CLOUD=1` in the Ollama **server** environment and start/restart it.
For a manually launched server, use `OLLAMA_NO_CLOUD=1 ollama serve` (do not start
a second server). Then in another terminal from this repository:

```sh
.venv/bin/python -m avocadoeyes
```

Open **http://127.0.0.1:7860**. The default inference endpoint is
`http://127.0.0.1:11434`. The workbench accepts clips up to 64 MiB and supports
sampling up to 16 frames from the first 60 seconds. Defaults sample eight frames
from the first 12 seconds.

Use authorized footage. Clips, frames, context, and history stay in the local
session; **Clear session** removes them from application memory. OS swapping and
Ollama retention remain operator concerns.

### Inference configuration

The adapter verifies `/api/show` local model metadata before inference, refusing
cloud-backed or uninstalled models. For a managed NemoClaw/OpenShell endpoint,
set `AVOCADO_INFERENCE_URL` explicitly to its native Ollama origin (no `/v1`). It
must expose `/api/show` and `/api/chat` with image forwarding, using localhost or a literal
private IP. The workbench never automatically changes routes. `AVOCADO_API_KEY`
optionally authenticates a local proxy. `.env.example` is a template; `.env` is
not auto-loaded. Verify managed routing and GPU placement on the actual target.

The adapter uses Ollama's native JSON/schema output and defaults `think` to false.
Model settings are editable per step; observation and ranking outputs are checked
against their contracts. See [architecture](docs/architecture.md) for runtime
boundaries and [pipeline configuration](config/pipeline.example.json) for defaults.

## Verification

```sh
.venv/bin/python -m unittest discover -s tests -v
# Real image + text check with an authorized local clip:
# This check uses qwen3.5:9b for every model pass.
.venv/bin/python -m avocadoeyes.check_route --video data/local/room.mp4 \
  --goals 'Find a small group for a low-energy conversation' --consent
```

The check prints versions, timings and failures without saving private inputs.
Fixture tests do not prove GB10 integration. A successful route check establishes
execution, not personality accuracy or improved networking outcomes.

## Contributing

Read [AGENTS.md](AGENTS.md), [project context](docs/project-context.md), and the
[contribution workflow](docs/contributing.md) before changing the project. Work
in one branch per change and coordinate through GitHub issues.

The [workbench spec](docs/specs/editable-pipeline-workbench.md) and
[issue #1](https://github.com/vrindaat/AVocadoEyes/issues/1) describe the prototype.
The broader [event-room spec](docs/specs/event-room-assistant.md) remains a draft.
Follow the [local SDD rules](docs/spec-system.md) and
[SDD guide](docs/sdd-guide.md); [architecture](docs/architecture.md) records
boundaries, and [contracts](docs/contracts/) define configuration and outputs.

To extend processing, register a function with
`@avocadoeyes.runner.register("my_kind")`. It receives
`(run, step, inputs, attempt)` and returns JSON-compatible output. Import your
trusted module with `--plugin my_module`, add the step and map downstream inputs.
The included `passthrough` kind accepts `{"value":"$validate"}` and illustrates
insertion before ranking.
