# Research scope and evidence decisions

Recorded: 2026-10-25.

Research direction: Vrinda. Prepared from the available research conversation, context handoff, and repository research documents.

Status: Record of explicit user research direction and the resulting evidence review. Final feature selection, weights, model choice, and product acceptance remain open. Recording an assistant suggestion here does not make it an accepted decision.

Audience: AVocadoEyes contributors and anyone reviewing the basis for the project. Purpose: explain what was investigated, why particular evidence was retained, what Vrinda explicitly chose, and what has not yet been chosen. This is a research decision record, not an implementation specification or a task queue.

Related issue: No originating research issue was supplied in this conversation; no tracker reference is invented. Related specification: [event-room assistant, currently Draft](../specs/event-room-assistant.md). This document does not change its acceptance status.

## Context

AVocadoEyes investigates whether live observations of people at an event, combined with information about a particular user, can help that user choose **who to approach** for a satisfying, worthwhile conversation with manageable energy costs. The initial research explored how people make approach judgments. Vrinda then narrowed the central question to how the user's personality and another person's traits or perceived traits jointly relate to actual conversation enjoyment, satisfaction, and connection.

Vrinda explicitly acknowledged that a direct, validated link for the whole proposed system is not established, while choosing to continue investigating whether useful associations exist. Better-than-human precision and an individual probability or score are intended capabilities to investigate, not measured achievements.

The research record includes both user decisions and assistant-generated proposals. The distinction matters most now: Vrinda requested a complete attribute inventory specifically so that she could make the final cue, trait, and attribute selections herself.

## Explicit decisions and requirements from Vrinda

The entries below paraphrase explicit user requests. They record research direction, not approval of every implementation suggested in response.

| User decision or requirement | Basis in the available conversation | Consequence for the research |
|---|---|---|
| Focus on choosing **who to approach** at an event. | Requests for judging which person might be enjoyable or useful to talk with; reinforced in repository project context. | General approach timing, opener generation, and profile matching alone do not answer the central question. |
| Use **live video of the people at the event** as the intended observation input. | The user explicitly identified live video footage as input. | Examine visible actions, presentation, objects, and interaction context; do not silently replace the setting with text-only profiles. |
| Include **known information about the user**, especially personality. | Requests explicitly referred to the user's Big Five traits and later stated that user personality is available. | Separate known user information from uncertain candidate observations and inferred traits. No specific questionnaire was finally selected. |
| Investigate a broad set of potentially useful visual cues. | Stance, appearance, expression, clothing, food/drink, and other details were explicitly raised; the user allowed retrieving as many cues as needed. | Research broadly before selecting a smaller feature set. Mentioning a cue does not commit the product to using it. |
| Personalize to the particular user's likely experience. | Requests concerned matching the user's vibe and personality combinations, rather than generic appeal. | Distinguish broadly liked candidates from pairings that might work particularly well for this user. |
| Study **actual satisfaction, enjoyment, and connection**, not just approach choices. | The user corrected responses toward papers associating the personalities of both people with how satisfying the interaction is. | Prioritize actual interaction evaluations; keep attraction, selection, and established friendship findings in their proper supporting roles. |
| Include **not becoming drained or exhausted** in the desired benefit. | The continued research request explicitly added conversation-related exhaustion. | Include social-fatigue evidence and user state/history; do not reduce success to initial appeal. |
| Work toward a **probability or score** that could help the user choose better conversations. | The user explicitly requested this kind of agent output. | Investigate prediction and uncertainty. No probability definition, scoring equation, numerical weights, or validated accuracy was selected. |
| Investigate two links separately: **visual cues to traits/impressions**, and **user information plus perceived partner attributes to outcomes**. | The user explicitly enumerated these two research categories and requested confidence in each. | Do not treat evidence for one link as validation of the entire pipeline. |
| Require **quantifiable, credible studies** with participant and methodological context. | Repeated requests asked who participated, what was measured, what each cue predicted, and the basis for the findings. | Record sample, setting, criterion, numerical estimate, and limits wherever verified. |
| Cite sources, avoid assumptions or hallucination, and disclose inaccessible papers. | Repeated explicit instructions; the user offered help obtaining papers. | Preserve links and access/version labels; do not fill missing methods or results from guesses. |
| Explain **presence, absence, meaning, influence, and confidence** for candidate attributes. | The user asked what nervousness or its absence means, then extended the request to all cues and the final inventory. | Distinguish higher/lower values, observed absence, and unobservable evidence; explain which outcome an association actually concerns. |
| Inspect the supplied **Back 2011 paper** and combine its findings with the other evidence. | The user supplied a local PDF and explicitly requested its analysis and a combined cue synthesis. | Retain the detailed full-text extraction, all 15 cue factors, personalized results, and limits. The paper itself is not redistributed in the repository. |
| Develop a research-backed rubric and knowledge-base foundation. | The user requested rubrics plus papers, books, and resources for grounding the model. | Preserve the prototype rubric and source inventories as proposals; a request for a rubric is not acceptance of its exact thresholds. |
| Preserve the research in readable, linked documents using descriptive repository naming. | Requests asked for a handoff, a consolidated research library, and the complete attribute response with every table and link. | Use Markdown, descriptive kebab-case subject filenames, and links to the detailed research. |
| Leave **final cues, traits, attributes, and their use** for the user to decide. | The latest attribute-inventory request explicitly states that the user is going to decide these. | Keep the inventory as a candidate catalog. Do not present the assistant's recommended shortlist as an approved model specification. |
| Make the current documentation addition **without any Git commands**. | The request creating this decision record explicitly prohibits them. | Add this document directly; do not inspect status, fetch, create/switch branches, stage, commit, or push for this task. |

## What was searched and why

This is a reconstruction of the research questions and coverage from the recorded requests and saved evidence. The earlier discussion export does not contain tool logs, so this is **not** a verbatim search-query log, a complete database search history, or a systematic-review protocol. Exact query strings, total hits, screening counts, and search dates for individual papers are not reconstructed.

| Research area | Questions that guided the search | Why it was included |
|---|---|---|
| Event approach judgments and nonverbal behavior | What do people notice before approaching someone? What can stance, expression, movement, clothing, and objects tell an observer? | Establish the original cue vocabulary and distinguish current opportunity from anticipated enjoyment. |
| First impressions and personal appeal | Which visible behaviors relate to initial liking? Do observer preferences change which appearances they like? | Identify measurable visual candidates and genuinely personalized first-impression hypotheses. |
| Meaning and absence of cues | What did researchers actually code? Does an apparently nervous behavior imply a poor partner? Does absence imply the reverse? | Avoid treating composite labels, ambiguous behavior, or missing evidence as definitive character judgments. |
| Visual personality inference | How well do photo/video judgments agree with independently measured personality? Does observer agreement equal accuracy? | Test the first link between visual information and candidate traits; distinguish real-trait criteria from apparent-personality labels. |
| User personality and choice | Which traits relate to approach, friendship nominations, dating choices, or collaboration preferences? | Explore personalized selection evidence while recognizing that selection is not satisfaction. |
| Personality combinations and actual interaction outcomes | How do actor traits, partner traits, and their interactions relate to enjoyment, rapport, comfort, satisfaction, or willingness to meet again? | Address the user's explicitly narrowed central question. |
| Conversation behavior and connection | What do questions, listening, turn timing, and reciprocal disclosure predict? | Define possible during-interaction features and outcome measures without substituting conversation advice for personality-pairing evidence. |
| Social fatigue and energy | Does sociable behavior predict later tiredness? Does personality change the cost of acting extraverted? | Address the user's exhaustion objective and separate user exposure from a candidate's visible animation. |
| Computational personality and rapport modeling | What inputs, labels, splits, metrics, and grounding checks have models used? Does adding personality improve held-out performance? | Assess technical feasibility and prevent benchmark metrics from being mistaken for individual conversation probabilities. |
| Books, measurement, and datasets | What supports cue coding, personality measurement, social-scene annotation, and reproducible evaluation? | Build the requested knowledge-base and methods foundation. |

The investigation therefore progressed from broad approach cues to a more specific personalized-outcome question. Earlier appearance and selection evidence was retained as context rather than discarded or relabeled as direct evidence of enjoyable conversations.

## What the research collection includes

The inclusion descriptions below record **what the assistant retained in the research corpus and why**. They do not claim that Vrinda independently selected every paper or accepted each associated feature for the model. Full source links, alternate copies, access labels, and historical leads remain in the [source library](../research/sources-and-access-status.md).

| Evidence group | Papers and resources retained | Role and limitation |
|---|---|---|
| Visual-to-personality evidence | Naumann et al. (2009); Borkenau et al. (2004); Dong & Xie (2023). | Human judgments compared with personality criteria. Useful for evaluating the first inference link; not a VLM accuracy guarantee. See [visual cues and personality](../research/visual-cues-and-personality.md). |
| Computational trait inference and grounding | Palmero et al./UDIVA; MM-OCEAN preprint; ChaLearn First Impressions documentation. | Examine context, labels, evaluation, and evidence grounding. Actual questionnaire traits and crowd impressions have different ground truths. See [visual evidence](../research/visual-cues-and-personality.md). |
| Direct initial-interaction personality combinations | Cuperman & Ickes (2009). | Independently measured actor/partner traits and actual stranger-interaction evaluations; especially relevant E/A findings. See [conversation outcomes](../research/personality-and-conversation-outcomes.md). |
| Everyday perceived-personality combinations | Weiß et al. (2023). | User traits, perceived partner traits, and retrospective interaction evaluations. Important direct pairing evidence, with same-rater/halo and setting limits. See [conversation outcomes](../research/personality-and-conversation-outcomes.md). |
| Rapport prediction and personality additions | Hayashi et al., 2024 preprint/2025 conference record; Müller et al. (2018); Reverdy et al. (2026). | Technical modeling evidence, including small gains, different rapport targets, and held-out failures. Not direct validation of pre-approach ranking. See [conversation outcomes](../research/personality-and-conversation-outcomes.md). |
| Complementarity and established-friendship findings | Dryer & Horowitz (1997); Körner & Altmann (2023); Yang et al. (2026). | Qualified context for roles, satisfaction, and similarity nulls. Different relationship stages, trait constructs, and access limits prevent a universal matching rule. See [conversation outcomes](../research/personality-and-conversation-outcomes.md). |
| Fatigue and behavioral costs | Leikas & Ilmarinen (2017); Jacques-Hamilton et al. (2019); Leikas (2020), access-qualified. | Primarily the user's own social behavior, exposure, and later tiredness. No established exhausting-person detector from a stranger's appearance. See [social fatigue and energy](../research/social-fatigue-and-energy.md). |
| First-impression cues and personalized appearance fit | Back et al. (2011); Naumann et al.; Lönnqvist et al. (2021). | Cue factors, general appeal, preference fit, and observer-personality interactions; initial liking is not subsequent enjoyment. See [Back analysis](../research/back-2011-cue-analysis.md) and [supporting studies](../research/first-impressions-and-supporting-studies.md). |
| Selection, attraction, and network context | Selfhout et al.; De La Mare & Lee; de Matos Fernandes et al.; Montoya and colleagues; historical mixer/proximity leads. | Broader context for choice and similarity. Romantic matching, friendship nomination, and professional preference are not interchangeable with conversation satisfaction. See [supporting studies](../research/first-impressions-and-supporting-studies.md). |
| Conversation mechanisms | Sprecher and colleagues; Templeton et al.; Huang et al.; West et al.; Kardas et al. | Questions, listening, disclosure, timing, expectations, and depth. Primarily actual-interaction evidence; silent video cannot supply speech content. See [supporting studies](../research/first-impressions-and-supporting-studies.md). |
| Cue-specific cautions and social context | Hall and colleagues; Funder; Hester & Hehman; Barrett et al.; Vacharkulksemsuk et al.; Walsh & Hewitt; Woolley & Fishbach; Rick & Schweitzer; Setti et al. | Coding vocabulary, context, narrow cue findings, and examples of misleading impressions. Not a universal scoring formula. See [supporting studies](../research/first-impressions-and-supporting-studies.md). |
| Methods, books, and data resources | Kendon; Bakeman & Quera; Hall/Schmid Mast/West; Gosling; BFI-2 materials; ConfLab; CANDOR and other qualified technical leads. | Support measurement, annotation, and experiment planning. Resource inclusion does not establish a selected questionnaire, training dataset, or model. See [supporting studies](../research/first-impressions-and-supporting-studies.md) and [source library](../research/sources-and-access-status.md). |

The collection also preserves [historical source notes](../research/historical-source-notes.json), [structured Back evidence](../research/back-2011-cue-evidence.json), the [prototype rubric](../research/prototype-observation-rubric.md), and the complete [attribute decision matrix](../research/conversation-attribute-decision-matrix.md). These are research artifacts, not learned weights or accepted application contracts.

### Access and inclusion limits retained during the review

- The user-supplied Back PDF was inspected directly. The detailed analysis preserves all 15 factors and distinguishes popularity from unique liking; the full copyrighted paper is not copied into the repository.
- Hayashi's rapport-estimation numerical results were checked in the preprint; the final IEEE tables were not verified. UDIVA's author version was available while the conference PDF fetch was blocked.
- Körner & Altmann's author manuscript and final abstract were available; final tables and a manuscript/final discrepancy remain qualified. Yang's final article was abstract-only in this review.
- Berry & Hansen (2000), the Jaques bonding papers, and full Leikas (2020) details remain access-limited research leads. Unaudited sample sizes, coefficients, or advertised accuracies were not promoted into core evidence.
- Other technical leads with uncertain label provenance, evaluation units, or transferability were retained as leads, not endorsed as validated actual-personality or conversation predictors.
- The source library preserves null findings, negative held-out results, version differences, and numerical corrections alongside favorable evidence. Inclusion means relevant to understanding the project, not proof that the project already works.

These are evidence-review judgments recorded by the assistant in response to Vrinda's quality requirements. They are not claims that the user explicitly voted on each inclusion or exclusion.

## Alternatives considered and how the direction changed

| Alternative | Recorded position | Rationale |
|---|---|---|
| A generic approachability assistant | Insufficient as the central answer. | The user repeatedly asked for personally satisfying encounters and trait combinations. Practical availability can still be a supporting observation. |
| An opener-generation or when/how-to-approach tool | Not the primary product intent; the repository draft treats these as non-goals. | The desired decision is which person to approach. Earlier opener examples remain historical material. |
| A profile-matching service using only declared traits/interests | Insufficient on its own. | Live visible behavior is central to the user's intended setup. |
| Initial appeal or romantic selection as proof of enjoyment | Retained as qualified supporting evidence, not the answer to the narrower question. | Choosing or initially liking someone does not establish that the conversation was satisfying. |
| Universal similarity across the Big Five | Not established by the reviewed evidence. | Specific E/A interactions and similarity null results do not support one all-traits matching rule. This is a research conclusion, not a finalized scoring decision. |
| Giving up because the complete pipeline is not already validated | The user chose to continue the investigation. | The goal is to identify testable associations and build a credible research basis while acknowledging uncertainty. |
| A probability versus a non-probabilistic ranking score | Both remain open output options. | The user requested a probability or score; the research did not select a calibrated event definition or fit a predictor. |

## Assistant proposals that remain unaccepted

The following were proposed to translate research into an experiment. They must not be attributed to Vrinda as completed implementation decisions merely because the user requested that the research be saved.

| Proposal | Why it was suggested | Current status |
|---|---|---|
| Prioritize E and A; treat other partner traits more cautiously. | Closest initial-interaction evidence and uneven visual inference validity. | Suggested research priority, not a final trait list. |
| Use the full 60-item BFI-2 when feasible. | A possible source of known user personality with documented scoring. | Instrument, length, language, and administration not chosen. |
| Separate enjoyment/connection from immediate effort and delayed fatigue. | The evidence concerns different outcomes and time horizons. | Proposed output and measurement design; no accepted scales or thresholds. |
| Preserve observations, apparent traits, user impressions, and outcome estimates separately. | They have different ground truths and error sources. | Proposed representation, not an accepted schema or interface. |
| Compare a direct cue-plus-user model with a trait-mediated model. | An intermediate personality inference may introduce error rather than improve prediction. | No model comparison has been executed or selected. |
| Test E-by-E and A-related interactions with main effects; use response-surface terms for exact-similarity claims. | Reflect the structure and limits of the evidence. | Statistical design proposal; no fitted coefficients. |
| Use R1-R7, ordinal 0-4/U anchors, and CLEAR/LIMITED/UNAVAILABLE evidence labels. | Earlier operational prototype for organizing observations. | Historical unvalidated rubric, not the final scoring system. |
| Observe a rolling 15-30-second window. | An initial engineering choice for prototyping. | No research-established optimum or accepted duration. |
| Use temporary availability filters, explicit pace/style preferences, topic relevance, and inclusion sequences. | Concrete observable or user-supplied candidates. | Candidate features; no accepted weights, penalties, or thresholds. |
| Avoid hidden-character conclusions and unsupported appearance penalties. | Evidence limits and repository guidance require careful interpretation. | Existing research/repository constraint; the exact permitted output contract remains to be specified. |
| Freeze pre-approach inputs and evaluate on held-out people/events against baselines. | Avoid leakage and measure actual predictive value. | Evaluation proposal, not an executed experiment or accepted numerical success criterion. |
| Calibrate probabilities on outcome-labeled data and report uncertainty/coverage. | Published correlations are not individual success probabilities. | No calibration model, training dataset, or measured calibration result exists in this record. |
| Include exploratory encounters and separately test the effect of showing recommendations. | Address missing outcomes and recommendation-induced behavior changes. | Research-method proposal; no study or data collection approved by this document. |

See [agent design and validation](../research/agent-design-and-validation.md) for the complete proposals and [attribute decision matrix](../research/conversation-attribute-decision-matrix.md) for feature-by-feature implications.

## Decisions still open

The available record does not establish any of the following as finalized:

- Final visual cues, user attributes, candidate traits, and optional audio features.
- The final cue definitions, detector requirements, temporal aggregation, and missing-evidence handling.
- The questionnaire or other method used to obtain known user personality.
- Whether the system should infer candidate personality at all, use apparent impressions, or predict outcomes directly from behavior and user information.
- Numerical feature weights, interaction coefficients, similarity functions, hard filters, score cutoffs, or success-probability thresholds.
- Whether one combined score or several outcome displays should be shown, and how the user trades enjoyment against energy cost or goal relevance.
- Capture scope, observation duration, refresh behavior, supported group sizes, UI, and candidate-identification method.
- Final model, framework, runtime integration, training dataset, and local GB10 performance. Download scripts or model metadata do not establish selection or successful inference.
- Outcome instruments, delayed-follow-up intervals, sample size, evaluation splits, baseline definitions, and acceptance criteria.
- Data collection, consent, storage, retention, access, and deletion policies. Creating this research record does not authorize collecting footage or participant outcomes.
- Demonstrated improvement over human judgment or baselines, calibrated pair probabilities, or verified improvement in user satisfaction.

The local-inference/GB10 constraint is already recorded in [project context](../project-context.md). It is not a new research-derived model selection. The [architecture](../architecture.md) and [draft specification](../specs/event-room-assistant.md) remain authoritative for their respective current status.

## Consequences and revisit conditions

The project has a documented research rationale and a broad candidate inventory. It does not yet have a validated cue-to-trait-to-enjoyment pipeline or an accepted final cue set. Research support should therefore explain why particular hypotheses deserve testing rather than claim demonstrated individual prediction accuracy.

Initial appeal, approach selection, actual enjoyment, connection, fatigue, and professional usefulness retain their distinct meanings. Paper coefficients retain their original scales and settings; they are not copied into a production score or converted into confidence percentages.

Revisit this record's open selections when Vrinda explicitly chooses the final features and intended use, when better primary-paper access materially changes the evidence, or when an actual experiment demonstrates which attributes improve personalized predictions. New durable implementation decisions should record their real acceptance and evidence through the repository's existing process; this document does not fabricate that acceptance.

## Provenance and related documents

This record was prepared from the 18 user requests preserved in the earlier discussion export, the context handoff, the continued research request in this chat, the documentation requests, and the repository's saved research. Private raw chats and local paper paths are not reproduced here. The search coverage is a reconstruction from those materials, not a newly executed literature search.

- [Research index](../research/README.md): complete reading guide and provenance.
- [Research summary](../research/research-summary.md): main claim-to-evidence map.
- [Conversation attribute decision matrix](../research/conversation-attribute-decision-matrix.md): full saved response, including tables, presence/absence interpretations, and recommended starting candidates.
- [Sources and access status](../research/sources-and-access-status.md): primary/alternate links, verification limits, missing access, corrections, and the complete earlier external-link inventory.
- [Agent design and validation](../research/agent-design-and-validation.md): proposed models, uncertainty handling, and evaluation.
- [Prototype observation rubric](../research/prototype-observation-rubric.md): historical anchors and model instructions.
- [Project context](../project-context.md), [architecture](../architecture.md), and [draft event-room specification](../specs/event-room-assistant.md): existing project intent and implementation boundaries.

Document creation adds this single decision record. It does not revise the research papers, accept the product spec, select final features, or run any Git commands.
