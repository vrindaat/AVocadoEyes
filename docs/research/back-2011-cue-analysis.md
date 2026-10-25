# Back 2011: first-impression cues and personalized liking

Primary source: Back, Schmukle & Egloff (2011), [DOI 10.1002/per.790](https://doi.org/10.1002/per.790). Read from the user-supplied PDF; all pages extracted and key results visually checked. The original copyrighted paper is not redistributed. This analysis supersedes the earlier abstract-only account.

## What Back actually measured

Seventy-three psychology freshmen in Germany (52 women, 21 men; mean age 22.32) gave short introductions in an introductory session. Mean introduction duration was 7.49 seconds (range 4.00-21.30). There were 2,628 unordered dyads, not 2,628 independent participants. Ten pairs reported prior acquaintance; excluding them did not materially change the results.

Peers rated initial liking and desire to become acquainted, and predicted whether the other person would like them. Seven groups of four trained judges coded separate information channels. Sixty-three cues were condensed into fifteen factors. Findings are observational; appearances and behavior were not experimentally assigned.

The paper separates general liking tendencies, target popularity, and unique liking for a particular person. It did not measure whether a subsequent conversation was enjoyable, professionally useful, or futile.

## Exact cue results from Figure 2

The correlation column is association with aggregate general liking/popularity, controlling target age and sex. These are sample-level associations, not weights for an individual or percentages of success. Definitions appear on printed pp.229-230; Figure 2 is printed p.233.

| Cue factor | r with general liking | Interpretation for feature design |
|---|---:|---|
| Fashionable body and dress | 0.29 | Composite includes fashion/chic ratings and body/fit judgments; not a pure clothing effect. Suggested treatment: descriptive plus user preference. |
| Weight | -0.05 | No meaningful general-liking association here. Suggested treatment: exclude from recommendation. |
| Fashionable face and hairstyle | 0.21 | Weak/marginal; composite mixes grooming with facial judgments. Suggested treatment: hairstyle descriptors only. |
| Babyfaceness | 0.12 | No meaningful general-liking association; not evidence of character. Suggested treatment: exclude from recommendation. |
| Outlandishness of dress | 0.10 | No clear general-liking association; personalized style fit is a different result. Suggested treatment: personalize do not penalize. |
| Amount of body movement | 0.39 | More body and expressive hand movement. Suggested treatment: candidate feature. |
| Speed and energy of body movement | 0.38 | Fast gait, fast movement and observer-rated body tension. Suggested treatment: candidate feature. |
| Extensiveness of behavior | 0.27 | Taking up space and proximity to the audience during an introduction. Suggested treatment: candidate contextual feature. |
| Self-assuredness of movement | 0.51 | Original factor blends smooth motion with gender-typical behavior; not pure confidence. Suggested treatment: reoperationalize smoothness. |
| Nervousness of behavior | -0.20 | Weak/marginal; includes facial/hand nervousness, stance changes and reduced eye-contact seeking. Suggested treatment: record components not emotion. |
| Friendliness of facial expression | 0.67 | Original composite: more smiling, more alert-looking expression and less grumpy-looking expression. Suggested treatment: record components not emotion. |
| Strength of voice | 0.42 | Composite strong versus nervous-sounding voice. Suggested treatment: audio only candidate. |
| Pleasantness of voice | 0.52 | Composite includes friendly voice and gender-typical voice; subjective/contextual. Suggested treatment: audio only reoperationalize. |
| Cumbersomeness of content | 0.03 | No meaningful general-liking association; do not penalize length from this finding. Suggested treatment: unsupported as negative rule. |
| Originality of content | 0.36 | Original, friendly and casual introduction content. Suggested treatment: audio only candidate. |

Facial friendliness and pleasantness of voice were the most important predictors in the simultaneous regression. Facial friendliness had standardized beta .41 (p<.01) for liking. Pleasantness of voice had beta .20 (p=.06) for liking: its independent contribution was marginal at the conventional .05 threshold despite its larger bivariate correlation.

The weaker face/hairstyle (.21) and behavioral nervousness (-.20) correlations should not be presented as equally established as the stronger associations. The null or weak factors remain useful negative findings: unusual dress is not a generic negative; lengthy content did not predict dislike; weight and babyfaceness are not useful liking rules.

Original factor labels are subjective composites. In particular, 'self-assuredness' combines smooth movement with gender-typical behavior, 'pleasantness of voice' combines friendliness with gender-typical voice, and fashionable appearance combines clothing/grooming with judgments of bodily/facial proportions. A new detector of smoothness, vocal warmth or clothing style is therefore a new operationalization, not an exact replication. Avoid importing gender norms, body-shape judgments or facial structure into compatibility scoring.

## The personalized result: preference and appearance fit

Table 3 (printed p.233):
- Overall preference similarity -> unique liking: r=.14.
- Clothing-preference similarity -> unique liking: r=.12.
- Subcultural-scene preference similarity -> unique liking: r=.10.
- Big Five similarity: r=.02; self-concept similarity: r=.01; vocational-interest similarity: r=.00. These did not predict unique liking here.

Figure 3 and accompanying text (printed p.234):
- Fit between observer preferences and the other person's appearance, aggregated across appearance factors, predicted unique liking: r=.12.
- Appearance-fit association with expected unique liking by the other person: r=.13. This is an expectation, not confirmed reciprocity.
- Individual appearance-fit factors had small associations: body/dress .06, face/hairstyle .08, unusual dress .09 with unique liking.
- Similarity partly operated through preference-to-appearance fit. The mediation was observational, so it does not establish causality.

This directly supports testing personalized visual affinity. Collect the user's own style preferences rather than assuming the target's dress has the same meaning for everyone. Do not infer subcultural identity from clothing; ask about style or interests when appropriate.

The .12 personalized association and .67 popularity association refer to different statistical levels and different outcomes; they cannot be compared as competing accuracy scores.

## What not to claim

Table 1 attributes .49 of the variation in liking to relationship effects, .13 to perceiver effects, .13 to target effects and .25 to error. This does not mean the study predicted 49% of compatibility.

The regression with age, sex and 15 cue factors explained R-squared .67 of aggregate popularity within the same sample (adjusted R-squared .57). There was no held-out prediction test. This is not 67% success accuracy, not performance of an LLM, and not variance explained in personalized enjoyment.

Extraversion and self-centered values were associated with greater popularity. The latter also predicted liking others less. Therefore appearing likable does not establish that a person will reciprocate liking or be considerate. Do not infer these hidden traits from the footage.

The cohort is small and culturally/age restricted. Zero-acquaintance interest null results do not show interests are irrelevant once people speak. No food/drink feature was tested in this paper.

## Compact comparison with Naumann et al. (2009)

[Source](https://ww.simine.com/docs/Naumann_et_al_PSPB_2009.pdf), printed p.1668, Tables 3-4. Photograph-based criterion-likability correlations: smile .26; energetic stance .27; tense stance -.23; distinctive appearance -.22; stylish appearance .14 (not significant); folded arms .01 (not significant). Neatness strongly affected conscientiousness impressions (.53), but its full-sample criterion association was .18 and not significant. These are trait/impression associations, not observed conversation outcomes. Keep perception and validity separate.

## Model-ready observation variables

These definitions are proposed operationalizations, not published validated scales.

| Variable | How to record | Required qualification |
|---|---|---|
| visible_smiling | Proportion of visible time with a smile; count occurrences; recipient if clear | Expression only; no happiness or sincerity inference |
| facial_orientation_and_change | Turns toward people, changes following another person's action | Camera direction is not eye contact; no private intention inferred |
| gesture_amount | Motion amount and gesture frequency relative to visible time | Normalize for occlusion, framing and camera movement |
| movement_speed | Observed hand/body movement speed | Not energy, confidence or personality by itself |
| movement_smoothness | Smooth versus stop-start motion, with timestamps | Do not label gender-typicality or stable confidence |
| stance_changes | Repositioning/fidget events | No diagnosis of anxiety; environmental alternatives retained |
| space_and_orientation | Relative space use, orientation, entry positions | Audience proximity in the source differs from event access |
| clothing_description | Garment type, colors, patterns, fit, styling and visible accessories | Avoid wealth, intelligence, identity or character inference |
| user_style_affinity | Match descriptors with the user's explicitly stated tastes | Missing preference -> unknown, not low compatibility |
| food_drink_objects | Exact visible item and hand/activity context | No contents inference; timing/hook use is an untested extension |
| voice_characteristics | Audible delivery descriptors, relative loudness if feasible | Audio required; no claim to infer personality |
| introduction_content | Specificity, novelty and relevant content | Transcript/audio required; novelty judged relative to context |

Preserve timestamps, observation confidence, missingness and alternative explanations. No single cue determines the recommendation. Separate directed acknowledgment of the user from general expressive behavior toward someone else.

## How the model can learn

A knowledge base can retrieve evidence and limits, but retrieval alone does not train or validate a new predictor. Build example records with:
- pre-encounter video and observable cues;
- explicit user preferences and event context;
- a frozen initial prediction;
- afterward: each participant's enjoyment, ease, interest and desire to talk again;
- follow-up usefulness separately from immediate enjoyment.

Learn separate outputs for first-impression appeal, personal appearance affinity, current opening and actual enjoyment. Fit and evaluate the final target from outcome-labeled data. Do not label data using 'a psychologist says this person looks extraverted' when the target is enjoyable conversation.

Evaluate across held-out people and events. Compare equal-information human predictions and an availability baseline. Include some exploratory encounters to observe outcomes beyond top recommendations, with participant agreement. Avoid treating repeated clips or dyads as independent people. Recommendation display can affect the encounter itself; measure this separately.

## Consolidated cues and conclusions across the papers

The entries distinguish support for an observed outcome from proposed product use. Exact thresholds remain unvalidated.

| Cue family | Evidence and measured outcome | Recommended conclusion/use |
|---|---|---|
| Smile and facial expression | Back: facial-expression composite correlates with initial liking (.67). | Candidate first-impression feature; record observable components. |
| Movement amount, speed, smoothness | Back: .39, .38, .51 with popularity; subjective composite definitions. | Candidate visual features; personal tempo fit needs outcome validation. |
| Space use and posture | Back: extensiveness .27; [Vacharkulksemsuk et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4839399/) manipulated posture in romantic selection. | Contextual candidate; not a universal compatibility rule. |
| Style matched to user taste | Back: aggregate preference-to-appearance fit .12 with unique liking; [Hester & Hehman](https://doi.org/10.1177/10888683231157961) review context and observer preferences. | Most direct personalized hypothesis; collect actual user tastes. |
| Broad traits and interests | Back: Big Five/self-concept/vocational-interest similarity did not predict unique liking at first sight. | Do not invent hidden similarity from video; this null is specific to the setting. |
| Directed gaze plus smiling | [Walsh & Hewitt](https://doi.org/10.2466/pms.1985.61.3.873): more approaches in a bar. | Acknowledgment cue; approach is not enjoyment. |
| Affiliative behavior | [Montoya et al.](https://doi.org/10.1037/bul0000148): meta-analysis associates behavior with attraction. | Consider sequences and combinations; pre-approach generalization needs testing. |
| Shared food | [Woolley & Fishbach](https://doi.org/10.1016/j.jcps.2016.06.003): assigned similarity affected trust/cooperation. | Possible shared context; not a personality inference. |
| Drink category | [Rick & Schweitzer](https://doi.org/10.1016/j.jcps.2012.06.001): alcohol cues biased intelligence judgments. | Counterexample; exclude that inference from the model. |
| Emotion labels | [Barrett et al.](https://doi.org/10.1177/1529100619832930): facial movement varies with context. | Output observation rather than hidden emotion. |
| Food/phone occupancy and opening topics | Practical extension beyond these tested findings. | Mark as design hypotheses and validate separately. |

Overall conclusion: there is empirical support for predicting initial appeal and small personalized appearance-affinity effects from visible information. Predicting enjoyable conversations from live event footage remains the project's new validation target. The model should learn cue-outcome relationships and individual taste fit, while preserving uncertainty and avoiding unsupported hidden-trait rules.



---

[Research index](README.md) | [Source library and access status](sources-and-access-status.md)
