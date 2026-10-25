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


There are no app dependencies, install scripts, or runnable services yet. Add
reproducible setup and verification commands when the first implementation lands.
