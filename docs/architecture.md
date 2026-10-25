# Architecture

Audience: implementers and reviewer. Owner: accountable code owner (assign with
the first implementation issue). Lifecycle: update whenever boundaries,
ownership, topology, or material data flow change.

## Current state

This repository contains SDD and collaboration documents only. There is no
application, supported API, persisted format, selected framework, model, or
verified deployment. The only shared infrastructure configured is the Git remote
`https://github.com/vrindaat/AVocadoEyes.git`.

## Intended constraints and open boundaries

Per [project context](project-context.md), application inference and the final
demo run locally on the GB10. NemoClaw/OpenClaw/OpenShell and Ollama are the stack
being prepared in prior chats; their exact integration and versions remain open.
Codex assists development; its account settings and chats are not app runtime
dependencies or the authoritative shared requirements.

Candidate data flow, **unaccepted** until the first spec is agreed:

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
