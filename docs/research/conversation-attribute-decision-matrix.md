**Below is the candidate attribute inventory from our research—not a finalized feature set or scoring formula.** It separates what the model can observe, what it might infer, and which outcome each attribute could inform.

The main limitation when choosing weights: **the papers do not establish how much each attribute contributes to AVocadoEyes’ final prediction.** They provide associations in specific settings. Where we do not have a defensible numerical effect, I say **“not quantified.”** That means unknown, not zero.

A few reading rules:

- **r** = correlation; **β** = standardized regression coefficient; **b/B** = coefficient in the study’s measurement units. They are not interchangeable or percentages of success.
- **Presence, observed absence, and unobservable are three different states.**
- For personality, use **continuous higher/lower scores**, not “trait present/absent.”
- Most findings below are associations; “influence” should not automatically mean a causal effect.

**1. The different tasks and outcomes**

| Task | What we want to estimate | Main candidate inputs |
|---|---|---|
| Practical approach opportunity | Can the user reasonably initiate contact now? | Current activity, acknowledgment, group arrangement, entry access |
| Initial appeal | Does the person initially seem appealing to the user? | Visible expression, movement, presentation, explicit style preferences |
| Conversation enjoyment and connection | Will this particular user enjoy talking with this person? | User personality/preferences, uncertain partner traits, interaction behavior |
| Energy cost | How demanding might the encounter be, immediately and later? | User energy, recent social exposure, desired pace, effort, contextual factors |
| Goal relevance | Could the encounter serve today’s purpose? | Explicit interests/goals and genuinely available candidate information |

These outcomes need separate estimates. A person can be appealing, temporarily unavailable, relevant to a professional goal, and potentially demanding—all at once.

**2. Known user personality and possible partner-trait estimates**

Collect the **user’s** traits through their existing questionnaire information. Estimating a stranger’s traits from video is a separate, less certain task.

For a concrete accuracy reference, the following correlations come from **human judgments of spontaneous full-body photographs**, against a self/informant personality criterion—not from a VLM. Single-observer results were weaker than aggregated judgments. [Naumann et al., 2009](https://ww.simine.com/docs/Naumann_et_al_PSPB_2009.pdf)

| Trait | Higher versus lower score means broadly | Human photo judgment r: single / six-observer aggregate | Proposed role |
|---|---|---:|---|
| **Extraversion, E** | More versus less sociable, assertive and outwardly energetic | .34 / .42 | Highest-priority personality pairing hypothesis |
| **Agreeableness, A** | More versus less cooperative and considerate | .13 / .20 | Important outcome hypothesis; visual estimation is weak |
| **Conscientiousness, C** | More versus less organized and dependable | .08 / .12 | Exploratory; no reliable appearance shortcut established |
| **Neuroticism / negative emotionality, N** | Greater versus lower tendency toward negative emotional experiences | Emotional stability, the opposite direction: .10 / .18 | Known user input may be explored; avoid confident video labels |
| **Openness, O** | Greater versus lower receptiveness to novelty and experience | .20 / .35 | Exploratory, especially for presentation preferences |

The C and emotional-stability aggregate results were not significant at the conventional .05 threshold. These numbers **cannot become the model’s confidence percentages**.

Results also vary across contexts: in a study of 177 short-video creators, observer/self-report agreement was significant only for E, **r=.16**; A=.03, C=.07, N=−.06 and O=−.03. Therefore, promising photo results do not establish dependable event-video inference. [Dong & Xie, 2023](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2023.1072344/full)

**The personality combinations worth distinguishing**

Here, *actor* means the user and *partner* means the candidate.

| Attribute or combination | Measured outcome and effect | What higher/lower values mean for our hypothesis |
|---|---|---|
| **User E × partner E** | Enjoyment **β=.36**; rapport **.38**; desire to interact again **.32** | Relatively high/high and low/low pairs evaluated encounters more positively than mismatched pairs |
| **Partner A** | User enjoyment **β=.25** | Higher partner A associated with better enjoyment |
| **User A × partner A** | Enjoyment **β=−.26** | Two low-A people had poorer interactions; this does **not** support universally matching similar A scores |

These findings came from **87 stranger dyads**, using independently measured personality during six-minute interactions. The study tested many effects; it does not supply production weights or establish that exact trait matching is optimal. [Cuperman & Ickes, 2009](https://doi.org/10.1037/a0015741)

A separate everyday-life study used the user’s **perception** of the partner:

| Attribute or combination | Reported effect on interaction evaluation | Interpretation |
|---|---:|---|
| Perceived partner A | **B=.164**, CI [.136, .191] | Higher perceived A associated with better evaluations |
| Perceived partner E | **B=.103**, CI [.079, .127] | Higher perceived E associated with better evaluations |
| Perceived partner N | **B=−.060**, CI [−.084, −.036] | Higher perceived N associated with poorer evaluations |
| User E × perceived partner E | **B=.002**, CI [.001, .004] | More extraverted users particularly valued perceived extraverted partners |
| User A × perceived partner N | **B=.004**, CI [.002, .006] | The N association depended on user A; not a rule to recommend high-N partners |

This was **130 participants and 3,108 reports**. The same user rated partner personality and the interaction, allowing halo effects. The E interaction was at the authors’ rounded adjusted significance boundary. A generic VLM impression is an additional transfer beyond these findings. [Weiß et al., 2023](https://online.ucpress.edu/collabra/article/9/1/91094/198724/Who-Is-Interacting-With-Whom-Assessing-the)

**Selection implication:** prioritize testing E and A. Do not give all five partner-trait estimates equal precision or equal importance.

**3. Observable visual attributes**

These are the underlying observations. They should remain available even if you decide against predicting partner personality.

| Attribute | Outcome/effect available | Presence or higher value | Absence or lower value | Proposed treatment |
|---|---|---|---|---|
| **Visible smiling**: occurrence, duration, recipient | Smile–E **r=.28**; smile–A **.21** | A visible expression that may contribute to an impression | Does not establish unfriendliness | Keep as behavior; distinguish directed versus general smiling |
| **Facial-expression composite** | Initial popularity **r=.67** | Higher study-defined facial friendliness | Lower composite, not necessarily dislike | Strong first-impression lead; not a smile-only effect |
| **Gesture/body-movement amount** | Initial popularity **r=.39** | More visible movement | Less visible movement, not necessarily introversion | Keep as a continuous behavioral feature |
| **Movement speed/energy composite** | Initial popularity **r=.38** | Faster/more energetic movement as coded | Slower movement, not necessarily low motivation | Test separately from user pace preference |
| **Movement smoothness** | Original “self-assuredness” composite: popularity **r=.51** | More smooth movement | More stop-start movement | Reoperationalize; original composite also included gender norms |
| **Stance changes / fidget-like movements** | Original nervousness composite: popularity **r=−.20**, marginal | More observed repositioning | Fewer changes, not proof of confidence | Describe actions; avoid anxiety labels |
| **Space use / expansiveness** | Initial popularity **r=.27** | More space occupied during an introduction | Less space occupied | Contextual feature; not a universal positive |
| **Nods** | No isolated future-enjoyment weight established | Observable response behavior | No nodding does not establish poor listening | Keep direction and sequence; avoid a fixed reward |
| **Head/body orientation** | No isolated enjoyment weight established | Person turns toward someone or an entry position | No turn may reflect activity or visibility | Useful for interaction context |
| **Response following another person’s action** | No transferable individual weight | A timestamped response sequence | No response may be ambiguous | Candidate responsiveness feature |
| **Clothing/presentation descriptors** | Original body/dress composite: popularity **r=.29** | A particular visible presentation | Different presentation, not poorer character | Use neutral descriptors and explicit user taste |
| **Hairstyle/grooming descriptors** | Original face/hairstyle composite: **r=.21**, marginal | Visible presentation details | Different or unobservable details | Do not import facial attractiveness judgments |
| **Distinctive/unusual clothing** | Initial popularity **r=.10**, no clear association | Distinctive presentation | Conventional presentation | Personalize; no generic unusualness penalty |
| **Neatness** | Observer C impression **r=.53**; actual-C criterion **r=.18**, nonsignificant | Stronger conscientiousness impression | Does not establish low conscientiousness | Good example of impression versus validity |
| **Crossed arms** | Criterion likability **r=.01**, nonsignificant | A posture | Uncrossed arms do not establish openness | No automatic rejection penalty |
| **Facial action-unit measurements** | Feature-family evidence, not individual cue weights | Measured facial movements | Low activation is not absence of emotion | Optional detector-based features |
| **Head/hand/facial coordination between people** | No universal positive coefficient | Some temporal coordination | Less measured coordination | Experimental; do not assume more synchrony is always better |

The Back results above concern **initial popularity among 73 students**, not subsequent conversation enjoyment. Its original composites mix several observations; replacing them with a neutral detector creates a new feature requiring validation. [Back et al., 2011](https://doi.org/10.1002/per.790)

The smiling, neatness and crossed-arm results come from photograph-based analyses. [Naumann et al., 2009](https://ww.simine.com/docs/Naumann_et_al_PSPB_2009.pdf)

For computational context, facial-feature models reached **AP=.70 versus a .25 random baseline** for low received rapport during group discussions. This is performance of a feature family and trained model—not a weight for a smile or an individual success probability. [Müller et al., 2018](https://www.collaborative-ai.org/publications/mueller18_iui.pdf)

**Important implementation distinction:** a VLM can describe visible behavior. Precise AU intensity, movement speed, duration or response timing needs suitable measurement and verification; sparse frame descriptions should not produce invented measurements.

**4. Practical availability and the seven earlier rubric dimensions**

These are **proposed operational features**. The research does not provide validated numerical enjoyment contributions or validated 0–4 thresholds for them.

| Dimension | Underlying attributes | What positive evidence means | What absence/negative evidence means |
|---|---|---|---|
| **R1: Current availability** | Current activity, phone/call use, eating/handling objects, departure, pauses | A visible opportunity without an obvious interruption | A clear competing activity suggests waiting; no visible activity does not guarantee availability |
| **R2: Acknowledgment toward this user** | Directed wave, greeting, reciprocal acknowledgment, response to a bid | The user has been acknowledged | No acknowledgment is not rejection; a clear decline means give space |
| **R3: Spatial access** | Relative positions, orientation, entry space, participants making room | A usable position or active accommodation of a newcomer | Inaccessibility is a practical constraint; a gap alone is not an invitation |
| **R4: Tempo fit** | Observed movement pattern × stated pace preference | Observed behavior matches today’s preference | A mismatch is a hypothesis about fit; it does not prove exhaustion |
| **R5: Aesthetic affinity** | Clothing/accessory descriptors × explicit user taste | Visible presentation matches stated taste | A mismatch concerns taste; missing taste information means unknown |
| **R6: Visible topic relevance** | Legible item, project sign or activity × stated interest/goal | There is a grounded potential topic | No visible topic does not establish no shared interests |
| **R7: Demonstrated inclusion** | Response to an actual newcomer, making space, facilitating participation | Inclusion was observed in that sequence | Without an entry opportunity, inclusion is unobserved—not absent |

The historical anchors are preserved in the [prototype rubric](<D:/My Stuff/Nvidia x Dell Hackathon '26/AVocadoEyes/AVocadoEyes/docs/research/prototype-observation-rubric.md>). Spatial research supports detecting group arrangements, but does not make a spatial opening a validated invitation. [Setti et al., 2015](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0123783)

**Avoid double-counting:** one turn-and-wave might contribute to acknowledgment, orientation and inclusion. Those are not three independent pieces of evidence.

**5. Explicit user preferences and personalized associations**

| Attribute | Task and numerical support | Presence / match | Absence / mismatch |
|---|---|---|---|
| **Preferred interaction pace today** | Enjoyment/effort; not quantified for this application | Provides a direct comparison with observed tempo | Missing preference means no tempo-fit conclusion |
| **Preferred participation role**: lead/listen/shared | Enjoyment/effort; no transferable weight | Can inform a role-fit hypothesis | Do not infer role preference solely from E |
| **Preferred group size** | Group-fit hypothesis; not quantified | Observed size matches stated preference | Mismatch is contextual, not proof of poor conversation |
| **Explicit style preferences** | Appearance–preference fit and unique initial liking **r=.12** | A supported personalized first-impression hypothesis | No preference means unknown, not low fit |
| **Clothing-preference similarity** | Unique initial liking **r=.12** | Small association in the original setting | No universal mismatch penalty established |
| **Subcultural-scene preference similarity** | Unique initial liking **r=.10** | Small association between reported preferences | Clothing alone does not establish the candidate’s identity or preferences |
| **Stated interests and expertise** | Goal/topic relevance; no reviewed visual-to-enjoyment weight | Known relevant information supports a topic or goal match | No visible evidence does not mean no common ground |
| **Today’s goal and its priority** | Defines what “good outcome” means; no universal coefficient | Allows goal-specific ranking | Missing goal requires a declared default |
| **Time available / desired duration** | Practical feasibility; not quantified | Encounter can fit the user’s time budget | Limited time is a constraint, not incompatibility |
| **User’s anticipated enjoyment** | Later enjoyment **r=.41** in one getting-acquainted study | Useful subjective baseline to compare with the model | Low expectations can be mistaken |
| **User’s anticipated liking** | Later enjoyment **r=.20** in that study | Another subjective baseline | Not a definitive forecast |
| **Prior familiarity** | Interaction evaluation **B=.226** in the everyday-life study | Known relationship context matters | Being strangers does not imply poor compatibility |

Preference-fit results: [Back et al., 2011](https://doi.org/10.1002/per.790). Expectations: [Sprecher](https://link.springer.com/article/10.1007/s12144-021-01466-4). Familiarity: [Weiß et al., 2023](https://online.ucpress.edu/collabra/article/9/1/91094/198724/Who-Is-Interacting-With-Whom-Assessing-the).

**Additional personality × appearance hypotheses**

These concern **initial liking of photographs**, not actual conversation outcomes:

| Combination | Reported interaction | Candidate interpretation |
|---|---:|---|
| User O × conventional appearance | **b=−.05, p=.001** | Higher-O observers reacted relatively more favorably to unconventional presentation |
| User O × ordinary appearance | **b=−.04, p=.005** | Higher-O observers reacted relatively more favorably to distinctive presentation |
| User E × traditional appearance | **b=.03, p=.032** | Small study-specific preference association |
| User A × traditional appearance | **b=−.03, p=.021** | Small study-specific preference association |
| User C × energetic appearance | **b=.03, p=.029** | Small study-specific preference association |

These came from 385 observers rating 146 targets. They are exploratory feature ideas, not a reason to override the user’s explicit taste. Lower trait scores do not guarantee the reverse preference. [Lönnqvist et al., 2021](https://helda.helsinki.fi/server/api/core/bitstreams/84952839-37a7-4614-ac34-0c61c15875b5/content)

**6. Energy and fatigue attributes**

This is the area where **user state and history deserve more attention than the candidate’s appearance**.

| Attribute | Reported effect or evidence status | Higher/present means | Lower/absent means |
|---|---|---|---|
| **Current self-reported fatigue/energy** | Proposed baseline measurement; no imported weight | Establishes the starting state | Low current fatigue does not guarantee low later fatigue |
| **User’s recent sociable/talkative behavior** | Later fatigue **b=.08**, SE=.03 | Greater earlier sociable behavior associated with more fatigue about three hours later | Less exposure does not prove no later fatigue |
| **Number of people recently encountered** | Later fatigue **b=.12**, SE=.04 | Higher social exposure associated with later fatigue | Fewer encounters do not necessarily mean less effort |
| **User’s recent conscientious/goal-directed behavior** | Later fatigue **b=.12**, SE=.02 | Another possible source of later fatigue | Low exposure does not identify the candidate as the cause of fatigue |
| **Recent conversation duration** | Proposed exposure measure; duration-specific weight not established | Records exposure time | Short conversations can still be demanding |
| **User E × sustained acting-extraverted demands** | Momentary tiredness interaction **b=−1.42**, SE=.50 | More introverted participants experienced greater costs under weeklong instructions | Does not establish no cost for extraverts |
| **Desired effort/pace today** | Explicit preference; not quantified | Provides a current constraint | Missing preference should stay unknown |
| **Candidate visible tempo × desired pace** | Not quantified for fatigue | A testable fit or mismatch | Calm appearance does not guarantee low effort |
| **Event duration, rest/breaks and intervening activity** | Proposed context variables | Help interpret accumulated fatigue | No validated weights in our review |
| **Noise/crowding** | Proposed context variables | Could change encounter demands; needs testing | No verified coefficient or automatic penalty |

The observational fatigue results involved **48 participants and 2,328 observations**. Trait E did not explain the behavior–fatigue relationship in that study. [Leikas & Ilmarinen, 2017](https://helda.helsinki.fi/server/api/core/bitstreams/e6ff30bd-64bb-47fe-b87a-0be781d2a268/content)

The acting-extraverted experiment found **no overall tiredness main effect**; its personality interaction concerned sustained instructions across a week. It does not establish that an animated partner drains an introverted user. [Jacques-Hamilton et al., 2019](https://jessiesun.me/publication/jacques-hamilton-2019/jacques-hamilton-2019.pdf)

**7. Attributes requiring audio or conversation content**

These are optional extensions. Silent video cannot supply them reliably. Evidence from the user’s own conversation also cannot be used retrospectively as an input to a supposedly pre-approach prediction.

| Attribute | Outcome/effect | Presence / higher value | Absence / lower value |
|---|---|---|---|
| **Voice-strength composite** | Initial popularity **r=.42** | Stronger delivery in the original introduction setting | Quiet voice is not low confidence or incompatibility |
| **Voice-pleasantness composite** | Initial popularity **r=.52**; simultaneous **β=.20, p=.06** | Positive initial-impression association | Subjective and context-dependent; original composite included gender norms |
| **Introduction originality/content composite** | Initial popularity **r=.36** | More original/friendly/casual content | Ordinary content is not proof of poor conversation |
| **Content length/cumbersomeness** | Initial popularity **r=.03**, no clear association | Longer content | No evidence here for rewarding brevity or penalizing length |
| **Question-asking** | High-question condition liked more: **d=.35** | Potential responsiveness-related behavior | Few questions do not automatically mean poor listening |
| **Follow-up questions** | Context-dependent; no universal weight | Content can show engagement with a prior contribution | Counts alone miss quality and context |
| **Validation/listening behaviors** | Connection associations; no transferable production weight | Content-based evidence of responsive behavior | Absence in a brief segment is inconclusive |
| **Speaking turns, duration and overlap** | No universal ideal ratio established | Describes participation patterns | More balanced time is not automatically optimal |
| **Turn-response latency** | Enjoyment **b=−.27**, SE=.05 | Longer partner delays associated with lower enjoyment in one study | Faster is not always better; do not impose a universal threshold |
| **Reciprocal self-disclosure** | Improved enjoyment/liking in an experiment; effect size not verified in our review | Alternating contribution can matter | Lack of disclosure in short small talk is not a failure |
| **Pitch/intensity synchrony** | Experimental modeling feature; no universal positive rule | Measured coordination | More synchrony does not necessarily mean better rapport |

Voice/content composites: [Back et al., 2011](https://doi.org/10.1002/per.790). Questions: [Huang et al., 2017](https://www.hbs.edu/ris/Publication%20Files/Huang%20et%20al%202017_6945bc5e-3b3e-4c0a-addd-254c9e603c60.pdf). Response latency: [Templeton et al., 2022](https://doi.org/10.1073/pnas.2116915119). Listening: [West et al., 2025](https://www.nature.com/articles/s44271-025-00342-2). Disclosure: [Sprecher et al., 2013](https://doi.org/10.1016/j.jesp.2013.03.017).

A useful counterexample: a 2026 rapport study included personality, synchrony and their interactions, but **none of its tested dyadic models beat the held-out baseline RMSE of .994**. Plausible attributes do not necessarily improve prediction. [Reverdy et al., 2026](https://camps.aptaracorp.com/ACM_PMS/PMS/ACM/ICMI26/60/6f94f100-86a3-11f1-b513-16ffd757ba29/OUT/icmi26-60.html)

**8. Attributes discussed that should not become automatic scoring rules**

| Attribute or proposed shortcut | What the research supports | Recommended decision |
|---|---|---|
| **Body weight / BMI** | Back popularity **r=−.05** | Exclude |
| **Babyfaceness / facial structure** | Back popularity **r=.12**, no meaningful rule established | Exclude |
| **Gender-typical movement or voice** | Embedded in some historical composites | Exclude those normative judgments; test neutral measurements separately |
| **Appearance-based intelligence, trustworthiness, wealth or character** | No validated basis for this project | Exclude |
| **“Smile means happy/sincere”** | Facial movement does not uniquely identify internal emotion | Keep observable movement; exclude certainty about the hidden state |
| **Alcohol-looking glass → intoxication or intelligence** | Drink appearance can bias judgments; contents may be unknown | Exclude inference; retain only observable activity/context |
| **Food/drink similarity → compatibility** | Assigned similar food affected trust/cooperation in specific experiments | No passive visual compatibility weight |
| **Standing alone → introverted/unapproachable** | No defensible rule established | Exclude shortcut |
| **Phone use → permanently uninterested** | Current activity may constrain timing | Use temporary context only |
| **No smile / crossed arms → reject candidate** | Unsupported as a standalone rule | Exclude shortcut |
| **Unusual dress → low fit** | No generic negative established | Use explicit user preference only |
| **Whole-profile Big Five similarity → enjoyment** | Back unique initial liking **r=.02**; other settings show similarity nulls | Do not use a universal similarity score |
| **Self-concept / vocational-interest similarity from appearance** | Back unique liking **r=.01 / .00** | Do not invent these attributes from video |
| **Perceived attractiveness** | Associated with evaluations in some studies, but distinct from personalized satisfaction | Prefer explicit user taste over a universal attractiveness rating |

Relevant sources: [Back et al.](https://doi.org/10.1002/per.790), [emotion-expression review](https://doi.org/10.1177/1529100619832930), [alcohol-cue bias](https://faculty.wharton.upenn.edu/wp-content/uploads/2014/06/Imbibing-Idiot-Bias_1.pdf), [shared-food experiments](https://kaitlinwoolley.com/wp-content/uploads/2017/08/woolleyfishbachjcp.pdf), and [friendship satisfaction/similarity findings](https://www.sciencedirect.com/science/article/pii/S0092656623000983).

**9. Information every observation needs**

These fields affect whether an attribute can be trusted, rather than whether the person is a good match:

| Field | Why it matters |
|---|---|
| Temporary person ID and timestamp | Connect evidence to the correct person and moment |
| Visible duration and occlusion | Distinguish observed absence from missing evidence |
| Recipient/direction | Separate acknowledgment of the user from behavior toward someone else |
| Available modality | Prevent invented speech or audio-based conclusions |
| Count/duration/intensity and measurement method | Distinguish an impression from a measured quantity |
| Repetition across separate episodes | Identify consistency without counting adjacent frames as independent evidence |
| Alternative explanations | Preserve ambiguity such as crowding, camera motion or another ongoing task |
| Evidence provenance | Record whether information came from the user, video, questionnaire or inference |
| Detector/model version and validation status | Make results reproducible and confidence assessable |

Keep **observation confidence**, **trait-estimate confidence**, and **outcome-prediction confidence** separate. A clearly detected smile can still provide weak evidence about future enjoyment.

**10. My recommended starting selection**

This is an engineering recommendation based on the evidence above, not a published optimum.

| Status | Attributes |
|---|---|
| **Core explicit inputs** | User E/A, today’s goal, preferred pace/role/group size, interests, time budget, current energy and recent social exposure |
| **Core observations to test** | Directed acknowledgment, current activity, spatial access, demonstrated inclusion, smiles, gesture amount/tempo, head/body orientation |
| **Optional personalization** | Explicit style affinity and genuinely legible topic relevance |
| **Experimental interpretation layer** | Partner E/A estimates, E×E and A-related interactions—with uncertainty retained |
| **Later extensions** | Other trait interactions, AUs, synchrony and audio/content features |
| **Exclude from scoring** | Facial/body morphology, demographic or gender-norm judgments, hidden-character claims and the unsupported shortcuts above |

For learning the eventual weights, collect **enjoyment, connection, effort, desire to talk again, immediate fatigue change, delayed fatigue and goal usefulness separately**. Compare whether adding each feature family improves held-out predictions and the ranking of candidates **for the same user**.

Until that evaluation exists, a feature’s published correlation is a reason to test it—not its percentage contribution to the final score.
