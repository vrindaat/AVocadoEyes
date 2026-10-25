# Visual cues and personality inference

This document addresses the first research question: what can be inferred from visual behavior, how accurate are those inferences, and what can a VLM use? The studies below distinguish **cue validity** (a cue relates to a measured trait), **judgment accuracy** (an observer's estimate relates to that criterion), and **machine performance** on a particular dataset. None is automatically a calibrated probability for a stranger at an event.

Abbreviations: E = extraversion; A = agreeableness; C = conscientiousness; N = neuroticism/negative emotionality; O = openness. Emotional stability is the opposite direction of neuroticism, but instruments and scales still need alignment. Reported r values are correlations, not percentages correct.


## Quantitative studies

### A1. Naumann, Vazire, Rentfrow & Gosling (2009)

*Personality Judgments Based on Physical Appearance*. DOI: 10.1177/0146167209346309.

[Author-hosted full paper](https://ww.simine.com/docs/Naumann_et_al_PSPB_2009.pdf). Full text accessed; Tables 1 and 3, printed pp. 1667-1668.

113 targets; full-body standardized and spontaneous photographs; criterion combines self- and informant-reported personality. Table 1 spontaneous-condition accuracy:

| Trait | Aggregated six observers r | Average single observer r |
|---|---:|---:|
| Extraversion | .42** | .34** |
| Agreeableness | .20* | .13 |
| Conscientiousness | .12 | .08 |
| Emotional stability | .18, p<.10 | .10 |
| Openness | .35** | .20* |

*p<.05; **p<.01. Nonsignificant entries are retained.

Table 3 cue-validity correlations: energetic stance with extraversion .39; smiling with extraversion .28 and agreeableness .21. Neatness correlates .53 with observers' conscientiousness judgments but only .18, nonsignificantly, with the personality criterion.

VLM proposal: timestamp smiles, posture and movement descriptions; test an extraversion estimate. These are human/photo results; study-defined energetic stance is an observer judgment, not a validated motion-speed threshold. Agreement among observers is not criterion accuracy. Do not interpret the paper's BESD-derived proportion index as observed classification accuracy.

### A2. Borkenau, Mauer, Riemann, Spinath & Angleitner (2004)

*Thin Slices of Behavior as Cues of Personality and Intelligence*. DOI: 10.1037/0022-3514.86.4.599.

[Author-uploaded full text](https://www.researchgate.net/publication/8646931_Thin_Slices_of_Behavior_as_Cues_of_Personality_and_Intelligence). Full article text accessed, particularly Table 5, printed p. 606.

600 participants; 15 recorded tasks. Uncorrected video-judgment correlations with self-reports, one task versus all 15: extraversion .21/.30; agreeableness .13/.22; conscientiousness .05/.08; neuroticism .11/.18; openness .17/.31. Against acquaintance reports, extraversion .21/.31 and agreeableness .12/.20.

One-task judgments aggregate four judges; the 15-task composite aggregates 60 judgments. Tasks include spoken and performed activities; this is not a silent-event-video benchmark. The reported .43 cross-situational consistency is not trait-prediction accuracy.

VLM proposal: compare evidence across different behavioral situations and retain variation. Repeated neighboring frames are not independent episodes. Additional-task gains in this design cannot prescribe a universal clip duration.

### A3. Dong & Xie (2023)

*How to know who you are through your short video selfies?—Capturing personality via short video selfies*. DOI: 10.3389/fpsyg.2023.1072344.

[Full paper](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2023.1072344/full). Full text accessed, Tables 1-2 and Methods.

177 Chinese Douyin users; mean age 26.78; observers reviewed multiple posted videos, not a single short clip. Aggregated observer/self-report correlations: extraversion .16 (p<.05), agreeableness .03, conscientiousness .07, neuroticism -.06, openness -.03; only extraversion significant. Smile frequency/proportion and self-reported agreeableness: age/gender-controlled r=.18. Conscientiousness questionnaire reliability was low, alpha=.34.

VLM use: smiles can be a candidate feature, with weak trait evidence. Platform editing, selfie posting, acting and background music are contextual social-media features; do not transfer them to event attendees. This study shows why observer consensus and trait validity need separate evaluation.

### A4. Palmero and colleagues (WACVW 2021): UDIVA

*Context-Aware Personality Inference in Dyadic Scenarios: Introducing the UDIVA Dataset*.

[Full author version](https://arxiv.org/html/2012.14259); [conference PDF](https://openaccess.thecvf.com/content/WACV2021W/HBU/papers/Palmero_Context-Aware_Personality_Inference_in_Dyadic_Scenarios_Introducing_the_UDIVA_Dataset_WACVW_2021_paper.pdf). Author version accessed; conference PDF fetch blocked. See Sections 4.2-4.3, Table 4.

Dataset: 147 participants, 188 sessions, 90.5 hours; this is the original collection, not every later release. Personality experiments used participant-independent splits with 15 test participants and BFI-2-based z-score labels. In the Talk task, average MSE across five traits: mean baseline .896; local visual model .875; both-person visual context .852; context plus metadata .821; context, metadata and audio .817.

VLM use: a relevant independently measured personality benchmark and evidence for retaining interaction context. The model is a trained transformer, not an off-the-shelf VLM. The .817 includes audio/metadata and is not an accuracy percentage. Fifteen held-out people constrain certainty. Metadata is not visual evidence; inspect its contents before adopting features.

### A5. Kang and colleagues (2026 preprint): MM-OCEAN

*Perception or Prejudice: Can MLLMs Go Beyond First Impressions of Personality?*

[Full preprint](https://arxiv.org/html/2605.22109). Full text accessed; peer-reviewed final publication not verified. See Sections 3-5 and dataset documentation.

1,104 videos, 5,320 cue-grounding multiple-choice questions, 27 multimodal models. Mean reported Prejudice Rate: 51.3%, defined through the benchmark's task thresholds; over half of correct trait ratings failed its grounding criterion. Mean Holistic-Grounding Rate: 10.4%; best 33.5%.

Personality labels inherit crowd-sourced First Impressions V2 ratings, discretized into five levels; they are not independently measured target personality. Annotation includes AI-generated material with human verification and AI-assisted evaluation.

VLM use: borrow the separation of observations, trait judgments and evidence links. Assess timestamp/body-region grounding separately from score agreement. The benchmark does not validate particular cue-to-trait causal explanations or conversation predictions. Grounding is necessary for reviewability, not sufficient for personality validity.

## Apparent personality benchmark labels

The [official ChaLearn First Impressions V2 description](https://chalearnlap.cvc.uab.cat/dataset/24/description/) describes 10,000 approximately 15-second clips from more than 3,000 YouTube videos with crowd-sourced apparent-personality annotations. These support agreement-with-impressions tasks. They do not establish independently measured personality or conversation satisfaction. A benchmark score expressed as 1 − MAE is not a literal percentage of correctly identified personalities.

## Proposed feature-to-evidence map

Everything in this table is an implementation proposal. The research motivates testing it; it does not validate a VLM detector or establish a universal threshold.

| Feature family | What to extract | Research connection | What the agent can conclude |
|---|---|---|---|
| Visible smiles | Occurrence, duration/proportion when measurable, direction/recipient | Naumann; Dong & Xie; [Back analysis](back-2011-cue-analysis.md) | A smile was visible; trait or liking implications remain uncertain. |
| Gestures and motion | Amount, tempo, smoothness, changes, visible interval | Naumann stance ratings; Back movement composites | The visible behavior pattern; motion alone is not enduring extraversion. |
| Head/body orientation | Turns, mutual orientation, shifts following another action | UDIVA context; [supporting spatial literature](first-impressions-and-supporting-studies.md) | Interaction context; head direction does not establish exact eye contact. |
| Nods and visible response sequences | Timestamped nods and responses after a visible contribution | [Cuperman & Ickes](personality-and-conversation-outcomes.md) | Candidate responsive behavior; silent video cannot prove listening, verbal acknowledgment, or speech turns. |
| Facial action units | AU occurrence/intensity with a suitable verified detector | Rapport models in [outcome evidence](personality-and-conversation-outcomes.md) | Measured facial movement; no one-to-one emotion or personality label. |
| Multiple episodes | Separate contexts with visibility and temporal provenance | Borkenau; UDIVA | More contextual evidence, without counting adjacent frames as independent samples. |
| Presentation/style | Neutral clothing/accessory descriptors and explicit user preference fit | Lönnqvist; Back; Hester & Hehman | Possible personal initial appeal, not intelligence, character, or conversation quality. |

## Evaluating confidence

1. Evaluate observation accuracy against independent human annotations. Record visibility and missingness.
2. Evaluate trait estimates against the intended criterion: partner questionnaires for actual-trait claims; independent observers for apparent-trait claims; the user for user-specific impressions.
3. Evaluate confidence empirically on held-out people. Repeated model agreement and verbal confidence are not substitutes for calibration.
4. Evaluate the final recommendation against participant-reported conversation outcomes. An accurately detected smile can still be weak evidence about future enjoyment.

No reviewed paper supplies a defensible fixed confidence value for a current VLM's video-to-trait inference at this event. Start by testing E and A as research priorities; do not silently give all five traits equal precision.

---

[Research index](README.md) | [Source library and access status](sources-and-access-status.md)
