# Personality and conversation outcomes

This document addresses the second research question: how do the known personality traits of the user combine with a partner's traits or perceived traits to relate to enjoyment, rapport, and satisfaction? The closest evidence is actor × partner modeling of actual interaction evaluations.

## Terms needed to interpret the results

| Term | Meaning | Implication for AVocadoEyes |
|---|---|---|
| Actor effect | The user's trait relates to the user's general evaluation tendency | Can change predicted rating levels; alone cannot rank candidates for a fixed user. |
| Partner effect | A partner trait relates to evaluations received | A general candidate characteristic, not necessarily a unique compatibility effect. |
| Actor × partner interaction | The effect depends on both people's traits | Candidate personalized relationship to test. |
| Actual partner personality | Independently measured questionnaire trait | The criterion in some pairing studies; video estimates introduce additional error. |
| Perceived partner personality | The evaluator's own impression | Distinct from a generic VLM impression and subject to halo effects. |
| Relationship-specific effect | Evaluation unique to this dyad after broader tendencies | Especially relevant to personalized candidate ranking. |

β denotes a standardized regression coefficient; b/B usually denotes an unstandardized coefficient. Preserve each paper's scaling and design. An interaction is directional when actor and partner traits differ.


## Quantitative studies

### B1. Cuperman & Ickes (2009)

*Big Five Predictors of Behavior and Perceptions in Initial Dyadic Interactions: Personality Similarity Helps Extraverts and Introverts, but Hurts "Disagreeables."* DOI: 10.1037/a0015741.

[Full paper](https://www.researchgate.net/profile/William-Ickes/publication/26852443_Big_Five_predictors_of_behavior_and_perceptions_in_initial_dyadic_interactions_Personality_similarity_helps_extraverts_and_introverts_but_hurts_disagreeables/links/00b7d5201204a3465c000000/Big-Five-predictors-of-behavior-and-perceptions-in-initial-dyadic-interactions-Personality-similarity-helps-extraverts-and-introverts-but-hurts-disagreeables.pdf). Full text accessed, Tables 3-5. Correction to handoff locator: Table 5 is printed p. 680, not 679.

87 stranger dyads, six-minute spontaneous laboratory interactions; independently completed BFI-44 measures. Actor x partner extraversion: enjoyment beta=.36; rapport .38; desire to interact again .32. Relatively higher/higher and lower/lower extraversion pairs evaluated interactions more positively than mismatched pairs. Agreeableness interaction for enjoyment beta=-.26; two low-agreeableness people had poorer interactions. Partner agreeableness/enjoyment beta=.25. Own agreeableness predicted nod count beta=.22 and smile/laugh count .23.

600 effects tested; student sample and observational trait associations. There is no complete five-trait compatibility rule. VLM proposal: uncertain partner extraversion and agreeableness as candidate interaction terms; do not equate smiles/nods with a questionnaire score or import coefficients as deployed weights.

### B2. Weiss, Grundahl, Jachnik & Hein (2023)

*Who Is Interacting With Whom? Assessing the Relationship Between Personality Traits and Preferences for Interaction Partners in Real Life*. DOI: 10.1525/collabra.91094.

[Full registered report](https://online.ucpress.edu/collabra/article/9/1/91094/198724/Who-Is-Interacting-With-Whom-Assessing-the). Full text accessed, Table 1 and confirmatory results.

130 participants, 107 women; 3,108 valid reports over seven days. User traits: IPIP-NEO-120. Partner traits: respondent's perceived personality, not partner self-reports. Outcome: single retrospective 1-7 interaction evaluation.

Own E x perceived partner E: B=.002, 95% CI [.001,.004], reported p=.013. The authors describe this as significant; it sits at their reported multiplicity-adjusted alpha of .013 (rounded from .05/4), so avoid describing it as a strong replication on p-value alone. Own A x perceived partner N: B=.004, CI [.002,.006], p<.001. Perceived partner main effects: A .164, E .103, N -.060.

More extraverted users particularly valued perceived extraverted partners. The A x N finding does not prove that agreeable users prefer neurotic over stable partners, or that neurotic users prefer agreeable partners. Actor and partner scales differ, so B magnitudes are not directly comparable. The evaluator rated both partner traits and outcomes, allowing halo/common-method effects.

VLM proposal: evaluate the user's own partner impression separately from generic machine-rated apparent personality. The latter is an additional transfer step.

### B3. Hayashi, Kimura, Ishii & Okada: preprint 2024, conference record 2025

*Investigating Role of Big Five Personality Traits in Audio-Visual Rapport Estimation*. Final DOI: 10.1109/FG61629.2025.11099120.

[Full preprint](https://arxiv.org/html/2410.11861v1). Exact numbers below are from the preprint; final IEEE tables were not verified.

32 Japanese friends in eight groups of four; 48 dyadic conversations, 96 directed ratings; first 20-minute conversation per pair analyzed. Eight-fold group-held-out cross-validation. Questionnaire input uses 60 item responses. Table 2 rapport prediction:

| Inputs | Pearson r | Concordance correlation |
|---|---:|---:|
| Facial features | .31 | .18 |
| Facial + perceiver questionnaire | .32 | .18 |
| Facial + target questionnaire | .35 | .20 |
| Facial + both questionnaires | .38 | .21 |

The user-only facial-model gain is small and not marked significant in Table 2. Reported plus/minus values are variation across training seeds, not participant-based confidence intervals. Their visual features come from the perceiver during the actual conversation, using OpenFace AUs summarized over utterances. This differs from observing a prospective partner before approach. Both questionnaire profiles cannot be replaced with video estimates without further testing.

### B4. Muller, Huang & Bulling (2018)

*Detecting Low Rapport During Natural Interactions in Small Groups from Non-Verbal Behaviour*. DOI: 10.1145/3172944.3172969.

[Full paper](https://www.collaborative-ai.org/publications/mueller18_iui.pdf). Full text accessed, Methods, Figure 5, temporal-segment results.

78 participants in 22 groups; approximately 20-minute discussions among strangers. Target outcome averaged rapport received from other group members. Lowest quartile defined low rapport. Leave-one-interaction-out evaluation: facial features AP=.70, random-ranking baseline .25. First-third facial features AP=.60; adding measured target personality allowed first-third results to reach approximately full-interaction performance.

Features include AU intensities/activations, face orientation, hand motion, coordination, and audio-dependent speaking/prosody features. AP=.70 is not 70% correctness or a success probability. Outcome is general received rapport, not this user's unique liking. This supports investigating current interaction dynamics and personality context; it does not establish pre-approach personalized prediction. The first third is several minutes, not a few seconds.

### B5. Reverdy, Silem & Cassell (ICMI 2026)

*Validation of a Multi-level Self-Report Rapport Scale and its Impact on Multimodal Modeling of Small Group Interaction*. DOI: 10.1145/3776574.3831156.

[Full conference article](https://camps.aptaracorp.com/ACM_PMS/PMS/ACM/ICMI26/60/6f94f100-86a3-11f1-b513-16ffd757ba29/OUT/icmi26-60.html). Full text accessed, Tables 8-9.

30 four-person groups overall; multimodal subset 16 groups/64 people. Reported 192 dyadic observations correspond to directed partner ratings, not 192 independent pairs. Personality x pitch-synchrony association: rater openness interaction beta=-.126, SE=.063, p=.046. Pitch requires audio.

Held-out-group dyadic RMSE: random-effects baseline .994; personality 1.026; synchrony .999; full 1.044; moderation 1.033. None beat baseline on this outcome. Small task sample and preliminary interaction; do not turn the openness finding into a universal scoring rule. Useful features include AU12, head motion, audio intensity/pitch, and video/audio representations, assessed as time series.

### B6. Friendship similarity null results

Korner & Altmann (2023), 190 friendship dyads: own agreeableness, extraversion and emotional stability associated with own satisfaction; agreeableness associated with friend's satisfaction; actual similarity unrelated to satisfaction. [Published abstract](https://www.sciencedirect.com/science/article/pii/S0092656623000983). Final full tables not accessed; prior handoff documents a manuscript discrepancy.

Yang and colleagues (2026), 1,476 participants/369 friend groups: response-surface analyses found no similarity effect on friendship satisfaction. [Published abstract](https://journals.sagepub.com/doi/10.1177/19485506261450240). Final full text not accessed. These existing-friendship outcomes constrain broad similarity claims, rather than directly refuting first-conversation associations.

## Interaction roles: additional direct satisfaction evidence

### 5.5 Dryer & Horowitz (1997): complementarity in interaction roles

**Title:** *When Do Opposites Attract? Interpersonal Complementarity Versus Similarity.* Journal of Personality and Social Psychology, 72(3), 592–603.

[Full PDF](https://www.communicationcache.com/uploads/1/0/8/8/10887248/when_do_opposites_attract-_interpersonal_complementarity_versus_similarity.pdf)

**Design:** Study 1: 42 female undergraduates interacting with a confederate. Study 2: 44 women in 22 pairs doing collaborative tasks. Studied dominance/submission and interpersonal goals, **not Big Five profiles**. Full text was inspected.

**Finding:** Satisfaction was greater when directing/yielding behavior complemented the participant's interpersonal style or goals. Study 1's second-interaction effect: **F(1,38)=8.26, p<.01**. Study 2's planned complementarity comparison: **t(40)=2.75, p<.01**.

**Limit:** Small, women-only task samples. Supports investigating preferred interaction roles, not a universal “opposites attract” rule or inferring dominance from posture. See Study 1 Results and Study 2 “Impact of Complementarity on Satisfaction.”

## Which associations should be tested first?

| Candidate relationship | Evidence | Proposed treatment |
|---|---|---|
| User E × partner E | Cuperman & Ickes; perceived-partner version in Weiß et al. | Test with all main effects and uncertainty in partner estimates. |
| Partner A | Favorable partner associations in the initial-interaction and everyday studies | Test as a partner main effect, separate from similarity. |
| User A × partner A | Initial-interaction result: low/low combination was unfavorable | Test the published form, rather than a universal similarity bonus. |
| User A × perceived partner N | Registered-report everyday result | Preserve the measured direction; collect or validate user-specific perceptions. |
| User traits × observed behaviors directly | Conceptually relevant; multimodal models provide partial precedents | Compare against a trait-mediated pipeline rather than assuming traits must be inferred first. |
| Full five-trait similarity | Friendship and other null findings constrain broad claims | Include a simple similarity baseline if useful; do not treat it as established. |

These are candidate hypotheses, not deployed weights. Include quadratic terms and response-surface analysis when claiming that exact similarity is optimal. A positive product term alone can describe patterns that are more complicated than exact matching.

## Where confidence is lost in the proposed transfer

The initial-interaction study measures both people's traits, then their actual conversation evaluations. AVocadoEyes would observe the candidate in another situation, estimate traits with error, and predict a new encounter with the user. Each step needs validation. Machine-rated apparent personality is not interchangeable with the specific user's impression in the everyday study. Do not multiply a visual-accuracy correlation by an interaction coefficient to create a pair success probability.

The most useful operational result would be a reproducible improvement in the ordering of this user's candidates over a visual-features/preferences baseline. Improvements in predicting generally positive raters or generally popular targets are useful to report separately.

---

[Research index](README.md) | [Source library and access status](sources-and-access-status.md)
