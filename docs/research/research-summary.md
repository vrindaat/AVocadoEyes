# Research rationale for AVocadoEyes

AVocadoEyes has an evidence-based reason to test personalized candidate selection. Some visible behavior helps people estimate personality; some combinations of user and partner traits relate to conversation evaluations; and social effort has energy costs that can emerge later. The strongest research contribution is a set of testable features and relationships for the agent. Its eventual value is whether those features improve the user's choices among people in the room.

## Evidence supporting the project

| Project question | Quantitative anchor | What it supports | Transfer still to establish |
|---|---|---|---|
| Can visible behavior contain personality information? | Naumann et al. (2009): six-observer photograph judgments correlated .42 with criterion extraversion; a single observer averaged .34. Borkenau et al. (2004): extraversion judgment/self-report correlations .21 for one task and .30 across 15 tasks. | Testing behavioral indicators, especially extraversion, with repeated observations. | A local VLM's accuracy on silent, crowded event footage and an individual candidate. |
| Does the user's personality change which partner is enjoyable? | Cuperman & Ickes (2009): actor × partner extraversion β=.36 for enjoyment, .38 for rapport, .32 for wanting to interact again. | Testing a specific personalized interaction term, rather than relying only on general popularity. | Replacing the partner questionnaire with an uncertain video estimate. |
| Is the combination more specific than general similarity? | In the same study, partner agreeableness β=.25 for enjoyment; agreeableness interaction β=−.26. Two low-agreeableness people did worse. | Distinguishing favorable partner characteristics from matching. | An accurate visual estimate of agreeableness and replication in event settings. |
| Do similar effects appear in everyday life? | Weiß et al. (2023): 3,108 reports; own E × perceived partner E B=.002, CI [.001,.004]. | Testing user-specific impressions and personality in natural interactions. | The perceiver was the user, not a VLM; the same user also evaluated the outcome. |
| Can personality help multimodal rapport estimation? | Hayashi et al. preprint: facial model r=.31; facial plus both questionnaires .38. User questionnaire alone .32. | Comparing multimodal models with and without personality. | Small user-only gain; data came from the actual conversation, not a pre-approach view. |
| Can behavior support a machine outcome model? | Müller et al. (2018): face features AP=.70 for bottom-quartile received rapport; random-ranking baseline .25. | A technical precedent for studying interaction features and outcome labels. | Group-level received rapport differs from this user's future satisfaction. |
| Is energy cost a separate target? | Leikas & Ilmarinen (2017): own sociable behavior related to fatigue about three hours later, b=.08, SE=.03. | Including recent social exposure, current energy, and delayed follow-up. | Predicting energy cost from the prospective partner's behavior. |

Sources and exact study scope: [visual-cue evidence](visual-cues-and-personality.md), [personality/outcome evidence](personality-and-conversation-outcomes.md), and [fatigue evidence](social-fatigue-and-energy.md). Each contains direct author/publisher links and numerical interpretation.

## The strongest honest project claim

> AVocadoEyes uses observable social behavior and the user's personality and preferences to investigate personalized recommendations about who to approach. Published research identifies candidate signals and personality interactions relevant to enjoyment and rapport. We evaluate enjoyment and energy cost separately and show the evidence behind a suggestion.

Before validation, describe recommendations as experimental rankings. After outcome collection and held-out calibration, a model could estimate a defined event such as an enjoyment rating meeting a prespecified threshold. The literature does not provide a ready-made 0-100 compatibility equation.

## Findings that improve the design

- Extraversion currently has more promising visual criterion evidence than most other traits. Dong & Xie (2023) nevertheless found only r=.16 for aggregated extraversion judgments from multiple posted videos, with the other traits nonsignificant. The input domain matters.
- Agreement among observers or VLMs can reflect shared impressions without establishing actual personality accuracy. MM-OCEAN evaluates cue grounding using apparent-personality labels; it is not an outcome-validation study.
- Specific pair interactions deserve testing. Universal Big Five similarity does not have consistent support, including null results in established friendships.
- VLM grounding, cue detection, trait validity, personalized ranking, and improvements in users' actual experiences need separate measurements.
- Reverdy et al. (2026) found that tested personality/synchrony models did not beat the baseline for held-out dyadic rapport. This makes simple baselines and leakage prevention essential.
- A user can enjoy an animated conversation and feel tired later. Fatigue requires its own timeline and user-state inputs.

## Confidence map

These labels are qualitative assessments of applicability, not computed posterior probabilities or formal meta-analytic grades.

| Proposition | Assessment from this review |
|---|---|
| Some behavior contains information about extraversion under studied conditions | Supported, with modest and variable accuracy. |
| Specific measured personality combinations relate to initial conversation evaluations | Direct supporting evidence; restricted samples and multiple-testing/context limits. |
| User preferences can personalize initial appearance liking | Direct but small, outcome-specific associations. |
| Visual cues can replace the partner questionnaire without material loss | Unestablished for this project. |
| The proposed VLM can predict this user's enjoyment from a pre-approach clip | Unvalidated. |
| The proposed score predicts fatigue from partner personality alone | Unsupported by the reviewed studies. |
| Showing recommendations increases satisfaction or beats equal-information human judgment | Requires a direct comparison. |

## Highest-value experiment

Freeze pre-approach observations and predictions, then compare candidate rankings from (1) practical availability, (2) visual cues plus explicit user preferences/state, and (3) those inputs plus user personality. Obtain post-conversation enjoyment and energy ratings, including delayed fatigue where feasible. Hold out people and events. The decisive result is whether adding personality improves **within-user candidate ranking** and whether recommendations improve actual outcomes. An actor main effect that raises all of one user's predicted ratings cannot reorder that user's candidates.

See [agent design and validation](agent-design-and-validation.md) for the proposed modeling and evaluation plan.

---

[Research index](README.md) | [Source library and access status](sources-and-access-status.md)
