# Historical prototype observation rubric v0.1

> **Research archive, not accepted behavior.** This earlier prototype is preserved so its exact anchors, decision rules, and source mappings remain available. The present product focuses on who to approach. Timing, opener examples, and aesthetic-affinity rules below are historical design material, not automatically accepted requirements. Newer evidence and uncertainty guidance in [agent design](agent-design-and-validation.md) take precedence when designing an experiment. No scoring weights or thresholds here have been validated.

Full-text evidence update: see [Back analysis and combined cue conclusions](back-2011-cue-analysis.md) and [machine-readable cue evidence](back-2011-cue-evidence.json). These distinguish aggregate first-impression appeal from personalized preference fit and future conversation enjoyment.

Purpose: recommend whether a brief conversation with a visible person is worth trying for a particular user, at this moment. Inputs: recent live video, user preferences, event context, and audio only when explicitly available.

This is a proposed operational rubric informed by research, not a validated compatibility instrument. The scores, window and thresholds are engineering hypotheses. Source IDs refer to [historical-source-notes.json](historical-source-notes.json). Newer evidence in this collection supplements and sometimes supersedes those historical review flags.

## User profile

Record event goal; preferred interaction tempo (quiet/moderate/animated/no preference); preferred group size; interests; aesthetic preferences and dislikes; time available. Missing preferences remain unknown. Do not infer user preferences from the user's appearance.

## Observation protocol

Prototype setting: inspect a rolling 15-30 second window and refresh after a meaningful change. This duration is not a research-established optimum. Use more context or abstain where needed.

Use temporary labels such as person_A. Record timestamp, visible action/item, recipient/direction, repetition, visibility and alternative explanations. Do not invent speech, relationships, brands or drink contents. A wine-shaped glass does not establish alcohol consumption. Head direction alone does not establish eye contact.

## Scoring anchors

Use ordinal 0-4 scores. Anchors 0, 2 and 4 are defined below; 1 and 3 are intermediate. U means unobservable or missing required user preference. U is not zero. Scores are not probabilities and must not be summed into a success percentage.

| ID | Dimension | 0 | 2 | 4 | Unknown rule and evidence |
|---|---|---|---|---|---|
| R1 | Approach timing and practical availability | Currently on a call, clearly leaving, or actively handling/eating food so initiation would interrupt the activity | No immediate barrier observed; no clear transition | Pauses after an exchange and visibly invites a new interaction | U if activity cannot be determined. Hand-occupancy/timing anchors are practical hypotheses. Background: S01, B02. |
| R2 | Acknowledgment toward the user | Clear observable decline of an interaction bid | No acknowledgment observed despite adequate visibility; no negative intent inferred | Directed greeting/wave or clearly reciprocal acknowledgment | U if recipient or signal cannot be resolved. A smile at someone else does not count. S06, S10; broader application is provisional. |
| R3 | Spatial access and orientation | Physically inaccessible entry or sustained arrangement with no usable position for a newcomer | Accessible position exists without adjustment toward a newcomer | Participants turn and shift to create a shared position for a newcomer | U if geometry or orientation is obscured. A gap alone is not an invitation. S11, B02. |
| R4 | Observed tempo fit | Sustained visible movement/gesture pattern conflicts with a stated user preference | Pattern is mixed or moderate relative to that preference | Sustained visible pattern matches a stated user preference | U without preference, adequate behavior or visibility. Silent footage does not establish a quiet conversation. S01, S03 are background; outcome prediction is a new hypothesis. |
| R5 | Aesthetic affinity | Visible dress/accessories conflict with an explicitly supplied user taste | Visible style is neutral to stated taste | Visible style closely matches stated taste | U without taste profile or visible details. Formality, neatness and price are not universal rankings. S04; compatibility prediction remains unvalidated. |
| R6 | Visible conversation-hook relevance | No usable visible hook in the adequately observed scene | Generic event/activity hook | Specific legible item/activity connects to a stated user interest | U if details or interests are missing. A band shirt supports a question, not certainty of fandom. S04, S07; proposed use. |
| R7 | Demonstrated inclusion behavior | Following a clear newcomer bid, actions repeatedly prevent entry | Brief acknowledgment without clear extension or blocking | Visibly greets a newcomer, makes space and facilitates participation | U when no relevant entry sequence occurred. Do not infer a trait such as kindness. Audio-free footage cannot establish verbal introductions or questions. S01, B02; outcome prediction needs testing. |

R2/R7 and R1/R3 may overlap. Do not count the same observation as independent evidence twice.

Food, drinks and objects affect only a visible timing constraint (R1), a stated aesthetic preference where applicable (R5), or an actual opening topic (R6). Do not infer intelligence, wealth, intoxication, personality, religious/dietary identity or trustworthiness from these objects. S08 illustrates impressions changing without evidence for the inferred attribute.

No smile, crossed arms, standing alone or briefly using a phone is insufficient by itself to infer disinterest. Account for context, crowding, culture and individual variation. Fixed facial features and demographic appearance are not evidence of character or compatibility.

## Provisional decision rules

Apply in order. These rules are prototype heuristics, not research findings.

1. Clear decline of the user's bid: GIVE_SPACE. No lasting incompatibility implied.
2. Clear current interruption/inaccessibility: R1 or R3 <= 1 with clear evidence -> WAIT.
3. R1 >= 2; R2 or R3 >= 3; and one of R4/R5/R6 >= 3 -> PROMISING_TO_TRY.
4. Both R4 and R5 <= 1, each supported by clear observations and explicit preferences -> LOWER_OBSERVED_FIT. This means profile mismatch, not a futile conversation or judgment of worth.
5. Opening exists but personal-fit evidence is weak/unknown -> EXPLORATORY_INTRODUCTION.
6. Otherwise -> INSUFFICIENT_EVIDENCE; name what is missing.

Keep the individual scores and evidence rather than a total. A low hook score indicates no visible topic; it does not indicate no common ground.

## Evidence quality and output

For each score label evidence CLEAR, LIMITED or UNAVAILABLE. Explain with visibility, direction, repetition and ambiguity. Clear visibility is not confidence that the predicted conversation will be enjoyable. No numerical success probability without external held-out calibration.

Return: temporary target ID; window; recommendation; all dimension scores/U with timestamps and evidence quality; supporting and conflicting observations; interpretation versus observation; unknowns; plausible alternatives; an opening line grounded in a visible detail; source IDs and source applicability. Cite research only for what the source actually studied, not as validation of this rubric's thresholds.

Example: PROMISING_TO_TRY. A camera is clearly visible; photography is one of your interests. The person acknowledged you and shifted toward you. Actual enjoyment remains untested. Opener: Are you photographing the event or trying out the camera?

## Knowledge-base structure

The JSON file is a source inventory and paraphrased seed notes, not a replacement for the full texts. Keep one empirical finding per record. Store source/version/date, design, population, setting, measured outcome, finding, limitations, rubric mapping, disallowed extrapolations and evidence type. Add exact page/section locators only after inspecting them.

Distinguish findings, theory, reviews, methods, datasets and design hypotheses. Retrieve both supporting and limiting records: clothing -> S04 with S03 limits; expression -> S06 plus S10; drinks -> S08; food -> S07 with its assigned-consumption setting. An aggregate study effect does not determine an individual's score. Keep user preferences and outcome feedback separate from general research.

Use licensed book copies or permitted excerpts and preserve attribution. The supplied notes are brief paraphrases.

## Validation against people

Freeze the pre-conversation window, rubric version and prediction before the encounter. Collect enjoyment, ease and interest (each 1-5), desire to talk again, and goal-specific follow-up separately. Duration and smiling are not enjoyment labels.

Assess observer agreement on cue coding separately from predictive accuracy. Compare model recommendations with human predictions from the same footage and an availability-only baseline. Split by participant and event, not just clips. Evaluate ranking quality, top-choice success, abstention coverage and calibration only if probabilities are produced.

Distinguish widely liked people from unusually good pairings. With participant agreement, include some exploratory encounters beyond top recommendations; outcomes for never-approached people are otherwise missing. Counterbalance whether recommendations are displayed when testing their benefit, because a recommendation may itself change expectations or behavior. Observational prediction does not establish causality.

Report whether you validated cue detection, human-impression agreement, personalized ranking, or improvement in real conversation outcomes. These are different claims.

## Reading order

S01 -> S04 -> S03 -> S02 for the foundation. S05-S08 for narrow cue evidence, alongside S10 for inference limits. B03 for coding and reliability; B01 for interpersonal accuracy. S12-S13 for computational benchmarking, not satisfaction labels.



## Historical model instructions

The following preserves the proposed instructions associated with this rubric; it is not a current application contract.

```text
You assess whether a brief conversation with a visible person is worth trying for THIS user at THIS moment.

Inputs:
- Recent video with timestamps; audio_available true/false.
- Explicit user preference profile and event context.
- Rubric v0.1 and retrieved knowledge-base records.

Treat the rubric's scores, observation window and decision rules as prototype design hypotheses, not validated psychological thresholds.

1. Observe first. Use temporary target IDs. Record actions, items, orientation, direction/recipient and timestamps. Do not invent speech, precise eye contact, labels, brands, relationships or drink contents. Use U for missing evidence.
2. Apply R1-R7 anchors from the rubric. Score 0-4 or U, with CLEAR/LIMITED/UNAVAILABLE evidence quality. Personal-fit dimensions require explicit user preferences. U is not low fit.
3. Separate observation from interpretation. Do not infer emotion, character, intelligence, social worth, intoxication, protected identity, wealth or personality from facial structure, appearance, clothes or objects. A smile at another person is not an invitation toward the user. A visible item is a possible opener, not proof of an interest.
4. Inspect cue combinations and context. Do not count the same action twice. No single gesture establishes disinterest or compatibility. Keep practical availability separate from aesthetic affinity and topic relevance.
5. Apply provisional decisions in order: GIVE_SPACE for a clear decline; WAIT for clear current interruption/inaccessibility; PROMISING_TO_TRY for adequate availability plus acknowledgment/spatial opening plus a supported personal-fit/hook cue; LOWER_OBSERVED_FIT only for the rubric's multiple explicit preference mismatches; EXPLORATORY_INTRODUCTION when an opening exists but fit is unknown; otherwise INSUFFICIENT_EVIDENCE.
6. Report bounded conclusions and conflicting observations. Never report a numeric success probability unless supplied by an externally calibrated predictor. Never call a person or an unknown conversation futile.
7. Use retrieved sources only within their measured setting/outcome. Label extrapolations as hypotheses. Return concise supporting evidence, not a claim that citations validate your individual prediction.
8. Reassess after meaningful change. For pre-approach predictions exclude later conversation evidence.

Required output:
target_id:
observation_window:
recommendation:
scores: [{dimension_id, score_or_U, observations_with_timestamps, evidence_quality, interpretation, source_ids, applicability_limit}]
supporting_evidence:
conflicting_evidence:
unknowns_and_alternatives:
suggested_opener:
hypothesis_notice: "Prototype recommendation; personal outcome not established."
```

---

[Research index](README.md) | [Source library and access status](sources-and-access-status.md)
