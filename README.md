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


## Run the two-stage local workbench

The default interface has exactly two model stages:

1. **Video → JSON:** upload a video file, edit the video prompt and JSON Schema,
   and inspect the model's output.
2. **JSON → reasoning:** send that JSON as text to a local reasoning model with
   your own prompt. Edit the reasoning prompt and rerun without reprocessing video.

Run `.venv/bin/python -m avocadoeyes` and open **http://127.0.0.1:7860**.
Confirm permission before uploading a clip up to 60 seconds / 64 MiB. Use **Run both models**, or run either model
separately. Invalid JSON/schema output stays visible but cannot feed reasoning.
Edits mark affected results stale. **Clear session** removes footage and outputs.
No prescribed person fields, ranking rubric or extra processing steps are required.

Video inference uses native Qwen3-VL through Transformers. The model processor
receives a local video file with temporal frame sampling disabled: every decoded
frame is included in order. Native spatial resizing and temporal patch grouping
still apply. The app does not turn the clip into an image-list request.
`max_frames` (default 256) rejects larger clips rather than sampling or truncating
them; raise it explicitly or use a shorter clip. `max_pixels` controls spatial
detail. Longer clips can exceed GPU memory or model context; no sampled retry occurs.

Prepare a CUDA-capable PyTorch/torchvision build and `requirements-video.txt` in
`.venv`, plus local Transformers weights for `Qwen/Qwen3-VL-8B-Instruct` under
`models/Qwen3-VL-8B-Instruct`. Set `AVOCADO_VIDEO_MODEL` or edit the model directory
in the UI to use a different compatible local model. **Installed Ollama GGUF tags
cannot be used as native video weights.** The app never downloads weights at runtime.
Native setup and integration evidence are recorded in the workbench spec.

For a fresh GB10 environment, preparation is explicit:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu130
.venv/bin/python -m pip install -r requirements-video.txt
# Only if the native checkpoint has not already been prepared:
.venv/bin/hf download Qwen/Qwen3-VL-8B-Instruct --revision 0c351dd01ed87e9c1b53cbc748cba10e6187ff3b --local-dir models/Qwen3-VL-8B-Instruct
```

The text stage uses local Ollama at `http://127.0.0.1:11434`, defaulting to
`qwen3.5:9b` with thinking enabled. You can select another installed local tag,
including `qwen3.5:35b`. The text answer is unrestricted text; the video
output is checked against your JSON Schema. An optional Model reasoning section
shows reasoning returned by the text backend. Set `OLLAMA_NO_CLOUD=1` in the
Ollama server environment. `AVOCADO_INFERENCE_URL` optionally selects an explicit
private native Ollama origin; no automatic route bypass or cloud fallback exists.
`.env.example` is a template, not automatically loaded.

Footage and outputs remain in session memory. Native inference temporarily writes
the uploaded video to a private temporary directory and removes it afterward.
OS swapping and model-server retention remain operator concerns. Only use
footage you are authorized to process. Models can make observational errors;
valid JSON does not prove accurate observations or networking value.

Checks:

```sh
.venv/bin/python -m unittest discover -s tests -v
PLAYWRIGHT_BROWSERS_PATH=/tmp/avocadoeyes-browsers PYTHONPATH=.:tests .venv/bin/python tests/two_stage_browser_smoke.py
# Real local native-video + text check using a generated synthetic clip:
PYTHONPATH=.:tests .venv/bin/python tests/native_video_smoke.py
```

The earlier ordered runner and v1 configuration remain in the repository for
compatibility with existing work. They are not steps in the default interface.
See the [workbench spec](docs/specs/editable-pipeline-workbench.md),
[architecture](docs/architecture.md) and [issue #1](https://github.com/vrindaat/AVocadoEyes/issues/1).
