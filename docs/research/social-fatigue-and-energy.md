# Social fatigue and conversation energy

The intended user benefit includes avoiding conversations that leave the user drained. The reviewed evidence supports tracking energy separately from enjoyment and distinguishing current feelings from later costs. It mostly concerns the user's **own behavior and recent exposure**, not an exhausting-person detector based on another person's face or animation.


## Quantitative studies

### C1. Leikas & Ilmarinen (2017)

*Happy Now, Tired Later? Extraverted and Conscientious Behavior Are Related to Immediate Mood Gains, but to Later Fatigue*. DOI: 10.1111/jopy.12264.

[Full author manuscript](https://helda.helsinki.fi/server/api/core/bitstreams/e6ff30bd-64bb-47fe-b87a-0be781d2a268/content). Full text accessed; fatigue results and Table 4 discussion.

48 participants, 41 women; 2,328 observations over 12 days. Earlier own sociable/talkative behavior predicted fatigue about three hours later, reported coefficient .08, SE=.03, p<.001. Number of people encountered was associated with later fatigue, b=.12, SE=.04, p<.01, and statistically mediated part of the behavior-fatigue association. Counter-trait tests did not find trait extraversion explaining the effect; the study was small for moderation.

VLM/system proposal: collect recent interaction count, duration and user-reported current energy. These are the user's history, not prospective partner traits. Observational mediation does not establish a causal mechanism. No coefficient maps a partner's visible animation to the user's future exhaustion.

### C2. Jacques-Hamilton, Sun & Smillie (2019; online 2018)

*Costs and Benefits of Acting Extraverted: A Randomized Controlled Trial*. DOI: 10.1037/xge0000516.

[Full paper](https://jessiesun.me/publication/jacques-hamilton-2019/jacques-hamilton-2019.pdf). Full text accessed, Tables 4 and 6 and Results.

147 participants randomized to a week of act-extraverted or sham instructions; 135 retained in the two randomized ESM groups. Condition x trait extraversion coefficient for momentary tiredness b=-1.42, SE=.50, p<.01; retrospective tiredness b=-.44, SE=.20, p<.05. More introverted participants experienced greater costs under sustained act-extraverted instructions; the momentary increase was significant only toward the low end of extraversion. There was no overall intervention main effect on tiredness. Concurrent own extraverted behavior/tiredness b=-.20, SE=.03, p<.001.

VLM/system proposal: distinguish current enjoyment/activation from later costs; ask about preferred pace and effort. This manipulated the user's own weeklong behavior, not a partner's trait or brief energetic conversation. It does not justify automatically assigning animated partners to a high-fatigue category for introverts.

### C3. Leikas (2020): supporting replication, limited access

*Sociable behavior is related to later fatigue: moment-to-moment patterns of behavior and tiredness*. DOI: 10.1016/j.heliyon.2020.e04033.

[Published/PMC record](https://pmc.ncbi.nlm.nih.gov/articles/PMC7260435/). Indexed abstract/full-text excerpts were accessible; direct PMC page and publisher full text were blocked. N=74, 1,046 observations; sociable behavior related to tiredness 2-3 hours later. Do not present this as a directly inspected complete paper or add unverified table coefficients. Full PDF would improve verification.

## What the agent can use

| Input | Why collect it? | Evidence status |
|---|---|---|
| Current self-reported energy/fatigue | Establish starting state and predict change, rather than confusing an already tired user with an exhausting encounter | Proposed measurement choice. |
| Recent conversation count and duration | Social exposure may explain some later tiredness | Motivated by Leikas & Ilmarinen; duration-specific weights require new data. |
| Desired pace and participation role today | Enduring extraversion does not fully specify current preference or effort | Proposed explicit preference input. |
| User trait extraversion | Test whether effort costs depend on personality in this setting | RCT motivates moderation; effect is not universal across fatigue studies. |
| Immediate enjoyment and effort | A conversation can be enjoyable and demanding at once | Keep distinct outcome labels. |
| Immediate and delayed fatigue | Delayed costs may be missed by a single post-conversation question | Time-lagged evidence motivates follow-up; select practical intervals prospectively. |
| Candidate visible tempo | A feature for testing preferred pace fit | No reviewed coefficient directly establishes its effect on this user's fatigue. |

## Proposed energy outcome

Estimate fatigue change relative to the user's pre-conversation state and collect perceived effort separately. Record subsequent conversations and other activities before a delayed rating, since they can affect tiredness. Event length, rest, noise, and current state can be recorded as proposed contextual variables; these documents do not assign published coefficients to them.

An initial energy display should express available evidence and uncertainty. It should not automatically label an energetic partner as draining for an introverted user. A single blended compatibility number would obscure the possibility of high enjoyment and high energy cost.

---

[Research index](README.md) | [Source library and access status](sources-and-access-status.md)
