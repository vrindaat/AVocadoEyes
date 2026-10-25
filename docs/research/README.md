# AVocadoEyes research

Research consolidated: **25 October 2026**. Audience: founders, implementers, reviewers, and hackathon readers.

AVocadoEyes investigates whether a user's measured personality and preferences, combined with observed behavior of people at an event, can help the user choose **who to approach** for an enjoyable conversation with manageable energy costs. The research gives specific reasons to test this idea: visible behavior contains some personality information, particular personality combinations relate to interaction evaluations, and recent social behavior relates to later fatigue. The complete live-video recommendation pipeline still needs outcome-based validation.

## Reading guide

| Document | What you will find |
|---|---|
| [Research summary](research-summary.md) | The strongest project rationale, claim-to-evidence map, numerical highlights, and limits on confidence. Start here. |
| [Visual cues and personality](visual-cues-and-personality.md) | Human judgment accuracy, cue validity, video benchmarks, VLM grounding, and specific observable features. |
| [Personality and conversation outcomes](personality-and-conversation-outcomes.md) | Actor/partner effects, extraversion and agreeableness interactions, rapport modeling, and similarity null results. |
| [Social fatigue and energy](social-fatigue-and-energy.md) | Delayed tiredness, acting-extraverted experiments, and implications for a separate energy-cost estimate. |
| [First impressions and supporting studies](first-impressions-and-supporting-studies.md) | Appearance preferences, friendship/romantic selection, conversation behaviors, reviews, books, datasets, and earlier research leads. |
| [Back 2011 cue analysis](back-2011-cue-analysis.md) | All 15 cue factors, exact reported associations, personalized liking, cue definitions, null findings, and combined cue synthesis. |
| [Agent design and validation](agent-design-and-validation.md) | Proposed inputs, evidence records, candidate modeling approaches, uncertainty, ranking evaluation, and probability calibration. |
| [Prototype observation rubric](prototype-observation-rubric.md) | Preserved seven-dimension research prototype, anchors, provisional rules, and historical model instructions. |
| [Sources and access status](sources-and-access-status.md) | Primary links, verification/version flags, papers needing access, and an exhaustive external-link inventory from the research notes. |

Two machine-readable supplements preserve earlier research details:

- [Historical source notes](historical-source-notes.json): 19 original source records, including S01-S15 and B01-B04 used by the prototype. Historical review flags are preserved; newer verified summaries in the documents take precedence.
- [Back 2011 cue evidence](back-2011-cue-evidence.json): structured extraction from the user-supplied paper and companion evidence. Research data, not scoring weights.

## How to interpret the evidence

Each detailed study entry identifies the design, measured outcome, reported estimate, access limits, and possible use by a vision-language model (VLM). Published findings and proposed engineering choices are labeled separately. We preserve null results because they help select useful features and avoid spending effort on unsupported rules.

Actual questionnaire traits, observer impressions, the user's own impressions, and visible behavior have different ground truths. Initial liking, actual enjoyment, rapport, fatigue, and professional usefulness are separate outcomes. A correlation or regression coefficient is not a person's probability of a satisfying encounter.

## Relationship to the repository

These files are a research reference, not an accepted product specification, architecture decision, implemented predictor, or new work queue. The existing [event-room proposal](../specs/event-room-assistant.md), [architecture](../architecture.md), and [project context](../project-context.md) retain their status. Current product intent is candidate selection; historical opener examples and timing rules remain background material. No model, framework, hardware performance, or end-to-end accuracy is established by these documents.

Use descriptive lowercase kebab-case names for subject documents; `README.md` is the directory entry point. Relative links make the collection navigable on GitHub. The collection paraphrases research and links to publisher/author copies; it does not redistribute full papers, private footage, personal chats, credentials, or model weights.

## Provenance and coverage

This collection consolidates the prior conversation's context handoff, the subsequent visual-personality/conversation evidence review, the detailed analysis of the supplied Back PDF, the original source/cue inventories, and the prototype rubric. Earlier transcript-only research links are retained in the source library as historical leads, with their limitations. The private transcript itself is not copied. This is a targeted review, not a systematic literature search; access labels describe the research session, not a fresh re-download of every source on document creation.
