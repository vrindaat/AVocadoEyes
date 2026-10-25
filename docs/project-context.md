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
deployment or selected model here. Check actual GB10 OS/architecture, package and
image compatibility, sandbox health, GPU access, and end-to-end local inference
before claiming the stack works. Keep weights and runtime bundles outside Git.
