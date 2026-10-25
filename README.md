# AVocadoEyes

An event-room assistant for the Dell × NVIDIA AI Hackathon. The product idea is
to help an attendee choose **who to approach** from visible behavioral cues,
reducing the fatigue of conversations that lead nowhere.

## Start here

1. Read [shared Codex instructions](AGENTS.md) and
   [project context](docs/project-context.md).
2. Follow the [two-person Git workflow](docs/contributing.md).
3. Use the [SDD rules](docs/spec-system.md), which supplement the
   [repository copy of the supplied guide](docs/sdd-guide.md).
4. Refine the [draft event-room spec](docs/specs/event-room-assistant.md) in a
   GitHub issue and record acceptance before implementing the capability.

[Architecture](docs/architecture.md) records current boundaries and open design
choices. Specs live in `docs/specs/`; create ADRs in `docs/decisions/` and
machine-readable contracts in `docs/contracts/` only when their triggers apply.

## Both contributors use the same setup

```sh
git clone https://github.com/vrindaat/AVocadoEyes.git
cd AVocadoEyes
git switch -c <name>/<short-change>
```

Open this repository root in Codex. `AGENTS.md` is the shared instruction entry
point; Git carries its linked documents to both machines. Each contributor uses
their own Codex login and Git identity. Personal/global instructions can differ,
so avoid local overrides that conflict with the agreed repository workflow.
See [official AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).


## Run the local pipeline workbench

Prepare Python 3.12, local Ollama and `qwen3.5:9b` on the GB10 before offline use.
The running pipeline uses only local services and bundled assets; no downloads.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
# Preparation only, if not already installed:
ollama pull qwen3.5:9b
```

Set `OLLAMA_NO_CLOUD=1` in the Ollama **server** environment and start/restart it.
For a manually launched server, use `OLLAMA_NO_CLOUD=1 ollama serve` (do not start
a second server). Then in another terminal from this repository:

```sh
.venv/bin/python -m avocadoeyes
```

Open **http://127.0.0.1:7860**. Both model aliases use local `qwen3.5:9b` at
`http://127.0.0.1:11434`. Confirm permission, upload a clip, add goals and
preferences, and click **Run all**. To inspect frames first, **Run step** on
`sample`. Each step exposes prompts, settings, additional inputs and mappings;
the JSON editor also exposes model aliases and sequence. Save edits, then run
a step or **Run from here**. Context changes reuse observations. Original
responses/timings remain inspectable; human corrections create revisions and
stale downstream results. **Clear session** removes in-memory footage and history.
Use authorized footage; OS swapping and Ollama retention are operator concerns.

The adapter verifies `/api/show` local model metadata before inference, refusing
cloud-backed or uninstalled models. For a managed NemoClaw/OpenShell endpoint,
set `AVOCADO_INFERENCE_URL` explicitly to its native Ollama origin (no `/v1`). It
must expose `/api/show` and `/api/chat` with image forwarding, using localhost or a literal
private IP. The workbench never automatically changes routes. `AVOCADO_API_KEY`
optionally authenticates a local proxy. `.env.example` is a template; `.env` is
not auto-loaded. Managed integration and GB10 GPU use still require verification.

The adapter uses Ollama's native JSON/schema output and defaults `think` to false
so thinking does not consume the final answer budget. Edit `think`, `num_predict`,
`temperature`, `num_ctx`, `top_p`, `seed`, `format` or `keep_alive` in step settings
when comparing configurations. Any returned thinking/explanation stays in the
original response. The observation/ranking contract is always checked.

```sh
.venv/bin/python -m unittest discover -s tests -v
# Real image + text check with an authorized local clip:
.venv/bin/python -m avocadoeyes.check_route --video data/local/room.mp4 \
  --goals 'Find a small group for a low-energy conversation' --consent
```

The check prints versions, timings and failures without saving private inputs.
Execution does not validate personality or networking outcomes. See the
[workbench spec](docs/specs/editable-pipeline-workbench.md),
[architecture](docs/architecture.md) and [issue #1](https://github.com/vrindaat/AVocadoEyes/issues/1).

To extend processing, register a function with
`@avocadoeyes.runner.register("my_kind")`. It receives
`(run, step, inputs, attempt)` and returns JSON-compatible output. Import your
trusted module with `--plugin my_module`, add the step and map downstream inputs.
The included `passthrough` kind accepts `{"value":"$validate"}` and demonstrates
insertion before ranking.
