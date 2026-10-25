# Agent design and validation proposals

This document translates the research into testable design options for choosing **who to approach**. It does not accept a product specification or select an implementation stack. The repository's local GB10 inference requirement remains in force; these research papers do not determine the model/runtime choice.

## Proposed reasoning layers

| Layer | Input and output | Evaluation |
|---|---|---|
| Observation | Video → timestamped visible actions, visibility, recipient, scene context | Human-annotated cue detection and measurement agreement. |
| Interpretation | Observations → uncertain apparent traits, possible user-specific preference fit | Separate validation for questionnaire traits, observer impressions, and user impressions. |
| Personalized outcome | User traits/preferences/state + candidate evidence → enjoyment/connection ranking | Held-out participant-reported outcomes and within-user ranking. |
| Energy cost | User state/history + proposed candidate/context features → effort and fatigue estimates | Immediate change and delayed follow-up, accounting for intervening activities. |

Each recommendation should reference the actual observations it used. Research citations explain why a feature was tested; they do not certify the individual prediction.

## Proposed user inputs and visible measurements


## Collect explicitly from the user

- Voluntary questionnaire-based personality: preferably full **60-item BFI-2** when feasible; preserve continuous domain scores, version, language, and scoring method. Verify the chosen instrument's official instructions.
- Today's goal and its priority: enjoyable small talk, teammate, topic learning, professional connection, etc.
- Today's preferred conversation energy: calm, moderate, animated, or no preference.
- Preferred role: lead, listen, shared lead, or no preference.
- Preferred group size and time available.
- Stated interests and expertise relevant to the goal.
- Explicit aesthetic preferences, preferably concrete examples, rather than assumptions based on the user's looks.
- Optional immediate expectation: anticipated liking/enjoyment before approaching.

## Record from video, with timestamps and visibility

- Smile occurrence/duration and recipient when resolvable; no assumed happiness/sincerity.
- Head/body orientation and changes; head direction is not exact eye contact.
- Gesture amount, motion speed/smoothness, and stance changes; no assumed enduring trait or anxiety label.
- Spatial arrangement, entry positions, acknowledgment of actual newcomer bids, and changes that make room.
- Current visible actions: eating, phone use, leaving, handling objects; practical timing hypotheses.
- Neutral garment/accessory descriptions and actual matches to stated user tastes.
- Legible topic hooks such as a visible project sign or item; do not invent text, brands, expertise, or affiliation.
- With audio explicitly available: speaking turns, turn-transition timing, actual acknowledgments, relevant questions, validation, and content. Silent video cannot establish these reliably.

Food/drink may provide an observed action or opening topic. A glass shape does not establish its contents. Objects do not establish intelligence, wealth, intoxication, trustworthiness, religion, diet, or personality.

## Modeling and uncertainty proposals

Everything in this section is a design proposal, not a tested result from the cited studies.

1. Keep timestamped observations separate from inferred traits. Each observation records person ID, time interval, channel, description, visibility and source frames. Use missing/unknown for occluded evidence.
2. Candidate visual features: smile occurrence/proportion; visible head nods; body/head orientation; gesture frequency/amplitude; motion tempo; responses following another person's visible contribution; changes in group arrangement. Exact AU intensity, motion speeds, durations, speaking turns and gaze require suitable detectors and verification. Sparse frame descriptions cannot establish precise timing or speech content.
3. Maintain separate representations for observed behavior, machine-rated apparent personality, partner questionnaire estimates, and the specific user's impression. They have different ground truths. Initially prioritize testing E and A; retain uncertainty on every trait.
4. Compare a direct model enjoyment=f(user traits, visual features, current state) against a latent-trait model that propagates uncertainty in partner traits. Do not assume that inferring an intermediate trait improves prediction.
5. Test E_actor x E_partner, A_partner and A_actor x A_partner with all constituent main effects. If testing perceived-trait findings, separately test A_actor x perceived_N_partner. Preserve direction and centering. Include quadratic terms/response-surface analysis when making claims about exact matching; a product term alone does not establish that exact similarity is optimal.
6. Use separate outcomes for enjoyment, connection, fatigue immediately afterward, and delayed fatigue. Ask current energy and recent social exposure. A conversation can score positively on enjoyment and negatively on energy cost.
7. Fit actor, target and dyad components with repeated-participant dependence accounted for. Check that a gain in a user's general rating tendency actually improves ranking of that user's candidates. User main effects alone cannot change candidate order for a fixed user.
8. Literature estimates can motivate features, interactions and weak, scale-aware priors. They cannot be combined by multiplying cross-paper r and beta or by directly adding differently scaled B values. A VLM's verbal confidence is not an empirical confidence interval.
9. Before outcome data, expose an experimental ranking score with traceable reasons and evidence quality. A 0-100 display would be a display scale, not a probability. After collecting labels, define a favorable outcome threshold before fitting, calibrate a probabilistic model, and test on held-out people/events. Consider actor-target latent uncertainty by averaging predicted outcomes across plausible partner profiles.
10. Compare availability-only, user-preferences-plus-video, and personality-plus-video models. Freeze all footage before approach. Separate model skill from whether displaying its recommendation improves satisfaction. Collect exploratory encounters to reduce approached-only selection bias. Assess within-user ranking, average error, calibration, uncertainty and abstention coverage.

## Candidate statistical models

These equations describe research models, not fitted systems. All coefficients must be estimated and evaluated; the literature does not supply production values.

```text
Direct outcome model:
  expected_enjoyment(user, candidate)
    = f(user_traits, stated_preferences, current_state,
        candidate_visual_features, event_context)

Trait-mediated model:
  expected_enjoyment
    = average over plausible partner traits T of
      g(user_traits, T, stated_preferences, current_state, context)
      weighted by the validated video-to-trait uncertainty model

Separate energy model:
  expected_fatigue_change
    = h(starting_energy, recent_social_exposure, user_traits,
        candidate_features, context)
```

Keep all lower-order terms when testing an interaction. Do not multiply a cross-paper visual correlation by a β coefficient or paste differently scaled B values into a score. Treat paper effects as hypothesis guidance or carefully specified weak priors only after checking measurement compatibility.

## From ranking score to probability

Before outcome data, a ranking can carry evidence quality and an experimental label. A 0-100 display is a display scale unless there is an externally validated probability model. It must not imply that the literature gives an 80% chance of success.

For a probability, define the event before fitting, such as an enjoyment rating at or above a chosen threshold. The threshold is a project decision, not a published optimum. Train on outcome-labeled encounters; calibrate using separate data; report held-out Brier score/log loss, reliability by probability band, sample counts, coverage, and uncertainty. Evaluate ordinal/continuous ratings too, so the threshold does not hide useful information.

Report separate estimates for enjoyment and energy cost. If the UI needs one ordering, any tradeoff between those outcomes should reflect an explicit user preference and be tested; it is not established by summing the prototype rubric.

## Proposed comparison and data collection

1. **Define the decision.** Which candidate does this user approach, from the available candidates, for the stated goal?
2. **Freeze inputs.** Save the allowed pre-approach window, feature/model version, prediction, candidate set, and decision time. Exclude later interaction cues from initial predictions.
3. **Compare baselines.** Availability alone; cues plus explicit preferences and current state; those inputs plus measured user personality. Compare direct-feature and trait-mediated models. Include equal-information human predictions where feasible.
4. **Collect distinct outcomes.** User enjoyment, ease/effort, connection, desire to talk again, immediate fatigue change, delayed fatigue, and goal-specific usefulness. Obtain both participants' independent ratings when possible. Proposed ad hoc ratings require a documented measurement plan.
5. **Measure the intermediary claims.** If claiming actual personality-pairing effects, obtain independently volunteered partner questionnaire measures. User-specific impressions and crowd apparent personality need their own labels.
6. **Prevent leakage and dependence errors.** Hold out people and events; keep repeated clips and dyads together; account for repeated raters/targets. Training-seed variation is not a population confidence interval.
7. **Measure candidate ranking.** Report within-user ranking, top-choice outcomes, average prediction error, abstention/coverage, calibration when relevant, and uncertainty. Separate actor/target general tendencies from dyad-specific gains.
8. **Address missing outcomes.** Never-approached candidates have unobserved conversation outcomes. With participant agreement, include exploratory encounters rather than training only on top-ranked choices.
9. **Test real benefit separately.** Randomize or counterbalance showing recommendations when studying whether the agent improves experience. A recommendation can change expectations and behavior.

This is an evaluation proposal, not an executed experiment. Sample-size planning, rating instruments, decision thresholds, consent/input handling, and acceptance criteria belong in the actual experiment/spec before data collection. Record real model/version, split, environment, seeds, commands, input provenance, and results when an experiment is run.

## Historical rubric and present scope

The [prototype observation rubric](prototype-observation-rubric.md) preserves earlier anchors and decision rules. Its 15-30-second window, 0-4 scales, and cutoffs are engineering hypotheses. Practical access can filter temporarily unavailable candidates, but solving who to approach remains the product goal. Historical opener generation is outside the current draft scope.

---

[Research index](README.md) | [Source library and access status](sources-and-access-status.md)
