# Hackathon and product context

Audience: both contributors and coding agents. Owner: product accountable owner
(assign in the first feature issue). Lifecycle: update as team decisions replace
open assumptions; accepted behavior belongs in a spec or contract.

## Evidence used for this bootstrap

The setup reviewed local Codex chat records on October 25, 2026:

- “Explain Dell x Nvidia hackathon,” October 24:
  `01a16d27-1162-7f40-9492-b7e37efff20c`.
- “Explain Dell x Nvidia hackathon,” October 24–25:
  `01a17157-83aa-7053-8669-b41fa1ed19c9`.
- “Load stack onto USB,” October 25:
  `01a171eb-e0f2-7403-9b9b-960f5963999e`.

These are provenance references, not files a teammate must possess. The following
summarizes the relevant user statements; raw chats and personal logs are not
copied into this repository. Suggestions in a prior chat are not team acceptance.

## Product intent

The user calls this an **event room assistant**: observe a room at a networking
event and help choose people likely to offer a worthwhile interaction, using
visible behavioral cues and perceived vibe. The motivation is fatigue after
multiple conversations that go nowhere. The user explicitly emphasized solving
**who**, rather than when/how to approach or what conversation opener to use.
Profile-based matching alone would miss that intent.

Whether visible cues predict a worthwhile interaction is an untested product
hypothesis. Define observable inputs, uncertainty, and user-evaluated success in
the spec. The exact ranking method, UI, capture mode, data policy, and models have
not been accepted. Do not treat appearance-based interpretations as verified
personality or a person's intrinsic value.

## Supplied organizer checklist

The user pasted a checklist for October 25, 2026, Frontier Tower, 995 Market
Street, San Francisco. It says all inference is local and the demo runs on the
GB10 on site; prepare the NemoClaw + OpenClaw + OpenShell stack and models on an
external drive. Teams are 2–5 people with one GB10 per team; this repository's
collaboration workflow is for two contributors.

Submission is stated as 6:00 PM PT sharp: repository, demo video at most three
minutes, short write-up, and NVIDIA feedback form. The pasted text conflicts on
doors opening (8:30 AM versus 9:00 AM); confirm logistics with the organizer.
[Event link supplied in the chat](https://builderbase.com/event/dell-x-nvidia-ai-hackathon-san-francisco).
This bootstrap preserves the supplied checklist; it does not independently
verify current organizer rules.

## Runtime preparation and known gaps

The chats discuss a Dell GB10 target and local Ollama with the NemoClaw,
OpenClaw, and OpenShell stack. On the Windows/WSL development laptop, Ollama
responded but the sandbox inference route returned HTTP 503 and the sandbox later
entered Error. Host model listing did not prove successful inference through the
sandbox. Do not carry that state into this project as a working deployment.

The user separately authorized stack/Ollama preparation on an external drive,
later excluding models from that transfer scope. This setup has not inspected
the resulting bundle or installed runtime software. There is no verified target
deployment here. The working model shortlist below comes from the subsequent
session discussion; compatibility and runtime behavior remain unverified. Check actual GB10 OS/architecture, package and
image compatibility, sandbox health, GPU access, and end-to-end local inference
before claiming the stack works. Keep weights and runtime bundles outside Git.


## Clarifications from the model and pipeline discussion

Updated October 25, 2026 at the user's request. This preserves conversation
context, not spec acceptance or proof of a working deployment. No models were
downloaded, application code written, or GB10 benchmarks run by this session.

### What the user wants to build

Rank people in a room relative to the attendee's goals and preferences, using
behavioral evidence from video. The intended benefit is more worthwhile
interactions within a limited time and energy budget. The user explicitly
rejected reducing this to conversation openings, immediate approachability, or
technical/profile matching. Personality fit and perceived vibe matter to the
product hypothesis, but cannot be treated as established facts from footage.

The user explicitly chose **inference only, with no training**. Earlier discussion
of self-labeling clips and reinforcement learning was exploration, not the plan.
Domain research should steer observation and interpretation through prompts and
rubrics. Prompting cannot recover cues that are invisible or missed by sampling.

### Proposed pipeline to evaluate

1. Sample ordered, timestamped frames from a short room video; associate evidence
   with stable person IDs where possible.
2. Ask a vision model for structured observations, with timestamps, interaction
   context, ambiguity, and alternative explanations. Keep the initial observation
   pass independent of the attendee's preferences.
3. Pass observations, explicit attendee preferences/goals, and a research-based
   interpretation rubric to a text reasoning pass.
4. Produce a personalized ranking with evidence and uncertainty. A score is an
   uncalibrated preference index until validated, not a measured probability of
   compatibility or of providing value.

Two passes can reuse one multimodal model. A separate text-only model is not
required. The proposed starting point is the same model for both passes, with a
second vision model used for comparison. Preserve frames for targeted inspection
when the structured observations omit something needed by the reasoning pass.

Separate visible observations from interpretations and from measured outcomes.
For example, posture or orientation is evidence; generosity, confidence,
professional value, and personality compatibility are hypotheses. Similarity to
an attendee does not necessarily imply compatibility. Silent footage does not
establish conversation content or reliably establish who is speaking.

### Working Ollama download shortlist

Subsequent implementation direction (2026-10-25): the user selected local
`qwen3.5:9b` for both workbench passes and no Internet use by the running pipeline.
The native local Ollama adapter is implemented; current verification and remaining
managed-stack/product gaps are in the [workbench spec](specs/editable-pipeline-workbench.md)
and [issue #1](https://github.com/vrindaat/AVocadoEyes/issues/1). The original
shortlist below remains historical context, not an instruction to download models.

These are the selected candidates from the conversation, not accepted production
models. Approximate package sizes were discussed; verify the exact current tag,
quantization, capabilities, and size before downloading.

| Ollama tag | Intended use | Approximate download |
| --- | --- | --- |
| `qwen3.5:35b` | Main visual observation and text reasoning candidate; discussed as the 35B-A3B mixture-of-experts variant | 22 GB |
| `qwen3-vl:32b` | Vision comparison candidate | 21 GB |
| `qwen3.5:9b` | Optional smaller fallback | 6-8 GB |

**122B is excluded from the selected list.** It was an optional candidate
introduced during advice and caused confusion. Do not add an 81 GB / 122B model
to the preparation scope without a new user decision.

The GB10's 128 GB is coherent unified memory shared by CPU and GPU, not a
separate 128 GB dedicated VRAM pool. Weights, visual inputs, context/KV cache,
runtime, operating system, and concurrent services all consume memory. Total
parameters and active parameters differ for mixture-of-experts models; active
parameter count does not mean only that fraction of weights needs storage.

### GB10 preparation commands discussed

Run on the native GB10 host, outside the sandbox. These commands were advice;
this session has not executed or verified them on the target.

```sh
ollama --version
curl -sS http://localhost:11434/api/version
ollama pull qwen3.5:35b
ollama pull qwen3-vl:32b
# Optional fallback:
ollama pull qwen3.5:9b
ollama list
ollama show qwen3.5:35b
ollama run qwen3.5:35b "Reply with one sentence confirming you are ready."
ollama ps
```

If Ollama is missing, the official Linux installer discussed was
`curl -fsSL https://ollama.com/install.sh | sh`. Check the actual ARM64 host and
installed version first. Start `ollama serve` only if no server is running.
Downloading a model does not update an existing sandbox's selected model.
NemoClaw onboarding was intended to select Local Ollama and `qwen3.5:35b`.
Verify an actual image request and the managed route before calling setup done.

### Runtime and latency considerations

The intended request path is application/OpenClaw -> OpenShell inference route
-> host Ollama -> GB10 GPU. Host inference can use the GPU without requiring the
agent sandbox itself to have direct CUDA access. NemoClaw is orchestration and
sandboxing, not a faster inference engine.

A model's video capability does not guarantee that Ollama or the managed
OpenAI-compatible route accepts an MP4 or `video_url`. Start with ordered sampled
images and confirm that the actual route forwards image content. Native Ollama
options, thinking controls, keep-alive settings, and context configuration may
not pass through a compatibility route unchanged. Tool calling also needs an
actual execution test; plausible JSON output alone does not prove a tool ran.

Initial sampling suggestions were approximately 8-16 frames per scan or around
2 FPS for short clips, to be tuned rather than treated as fixed requirements.
Sampling can miss brief gestures. Keep the model warm, bound output length and
context, and avoid separate agent turns for every person in every frame. A change
to attendee preferences should normally rerun reasoning over cached observations.

There is **no measured end-to-end latency on this GB10**. The earlier 15-45 second
estimate for a bounded warm analysis was a planning assumption. Text generation
benchmarks are not video-analysis benchmarks: decoding, image encoding, input
processing, reasoning tokens, tool calls, cold loads, and routing add latency.
Measure direct Ollama and routed requests with the same input before estimating
the demo's refresh cadence or choosing timeouts.

### Clip sources and evaluation ideas

- [SALSA](https://tev.fbk.eu/resources/salsa): the first suggested practical
  source, especially cocktail-party footage and group/body-pose annotations.
  Overhead views and small faces limit detailed expression analysis. The
  discussed license is CC BY-NC-SA 3.0; check the source terms for intended use.
- [ConfLab](https://research.tudelft.nl/en/datasets/conflab-a-rich-multimodal-multisensor-dataset-of-free-standing-so/):
  real conference mingling, multiple sensors and views; full raw-data access can
  require a request. Do not depend on approval arriving during the hackathon.
- [MatchNMingle](https://matchmakers.ewi.tudelft.nl/matchnmingle/pmwiki/pmwiki.php?n=Main.MatchNMingle):
  mingling and speed-dating interactions with access conditions. Dating outcomes
  do not establish professional networking value.

No dataset clips were downloaded or annotated in this session. Check access,
license, and public-demo permissions before choosing footage.

Suggested diagnostic evaluation: compare visual observations separately from
personalized rankings on a small set of clips; preserve annotator disagreement,
and keep clips from the same person/source or alternate camera view in the same
split. Compare prompts with and without domain research to see whether it helps.
Human labels of perceived vibe are judgments, not ground truth about eventual
value. A ranking-quality claim needs attendee feedback or actual interaction
outcomes. None of these evaluations has been run.

### Laptop failure context worth retaining

The earlier Windows/WSL installation reported NemoClaw `0.0.137` and OpenShell
`0.0.116`. Windows Ollama was reachable from an ordinary Docker container at
`http://host.docker.internal:11434/api/tags`; this proved model-list connectivity
only. The `avocado` sandbox passed direct CUDA checks but later entered Error.
Its managed route returned `cluster inference is not configured`, and supervisor
logs reported an empty route bundle (`route_count:0`).

The managed local sentinel provider could not be used as a cluster inference
provider. An `openai` provider named `ollama-windows` was then created against
`http://host.openshell.internal:11434/v1`; endpoint verification failed. Saving
that route with `--no-verify` did not fix connectivity or make the sandbox ready.
`nemoclaw onboard --resume` found no resumable session. Do not treat this laptop
installation as working or transplant its unverified routing configuration to
the native GB10. The exact cause of every failure was not resolved.

### Reference documentation discussed

Model tags and runtime behavior change; these are sources for rechecking, not
pinned versions or evidence that the target works.

- [Qwen3.5 Ollama catalog](https://ollama.com/library/qwen3.5)
- [Qwen3-VL Ollama catalog](https://ollama.com/library/qwen3-vl)
- [Ollama Linux setup](https://docs.ollama.com/linux)
- [Ollama vision inputs](https://docs.ollama.com/capabilities/vision)
- [Ollama OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility)
- [NemoClaw local inference](https://docs.nvidia.com/nemoclaw/latest/inference/use-local-inference.html)
- [Qwen3.5-35B-A3B model card](https://huggingface.co/Qwen/Qwen3.5-35B-A3B)
- [Qwen3-VL-32B-Instruct model card](https://huggingface.co/Qwen/Qwen3-VL-32B-Instruct)
