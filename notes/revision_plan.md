# Peer Review Synthesis and Revision Plan

## Review Summary by Reviewer

### Reviewer 1: Daron Acemoglu (Economist)
**Strengths**: Framework aligns with his task-based model; Amdahl's Law analogy is sound.
**Weaknesses**: 
- Asserts H ~ O(E) as functional form without empirical measurement
- Missing institutional/directional dimension — AI development priorities make bottleneck worse
- "Novelty" is underspecified — his "hard-to-learn" vs "easy-to-learn" distinction is more precise
- Need empirical grounding: his estimate is only 4.6% of tasks currently automatable
**Questions**: What is the actual measured H/E ratio across real workflows? How does it change over time?

### Reviewer 2: Andrej Karpathy (ML Practitioner)
**Strengths**: Matches his lived experience perfectly — demos vs production gap, nanochat experience.
**Weaknesses**:
- Missing "march of nines" mechanism: each nine of reliability = equal effort, compounding in multi-step workflows
- Missing "verifiability frontier": the novel/routine boundary is better captured as verifiable/non-verifiable
- Should distinguish capability improvement (accuracy) from reliability engineering (consistency)
- Vibe coding MenuGen example: 80% demo was really 20% done — could formalize this
**Suggestions**: Add verifiability as a dimension alongside novelty. Cite the reliability compounding math.

### Reviewer 3: Ilya Sutskever (AI Researcher)
**Strengths**: Agrees bottleneck is real for current architectures.
**Core challenge**: The bottleneck is architectural, not structural. Solve generalization (emotions as value functions, continual learning) and the scaling class changes.
**Specific objections**:
- Paper treats "novelty" as fixed property of tasks; but agent's ability to handle novelty improves
- Models generalize "dramatically worse than people" — but this is a solvable research problem
- The insight-is-serial claim may be wrong: insight could emerge from enough compute + right architecture
**What would change**: If continual learning + better generalization → ν shrinks dynamically during task execution → H could become sublinear

### Reviewer 4: Dwarkesh Patel (Techno-optimist)
**Strengths**: Napoleon argument directly supports organizational section. Appreciates intellectual honesty.
**Weaknesses**:
- Paper conflates "can't be done today" with "can't be done ever" — need clearer temporal scoping
- Missing the continual learning crux: the bottleneck is that models don't learn on the job
- The "country of geniuses" critique is too strong — should acknowledge that even constant GDP growth of 2% is transformative over decades
- Combinatorial attention argument (Scott Alexander) should be cited
**Suggestions**: Add explicit "conditions for falsification" — what would need to be true for H to become sublinear?

### Reviewer 5: Michael Nielsen (Epistemologist of Discovery)
**Strengths**: Discovery fiction framework strongly supports serial insight chain. Empirical evidence on scientific productivity is powerful.
**Weaknesses**:
- Missing the cognitive primitive creation possibility: AI might not just speed up existing cognition but create new cognitive operations
- The paper is too binary (linear vs sublinear) — should discuss phase transitions in what counts as "novel"
- Nobel Prize discovery rate per dollar being constant is the strongest empirical evidence — should be cited
- "Thought as a Technology" framework suggests bottleneck is real but the boundary of what's thinkable is expandable
**Core insight**: The bottleneck is real AND the boundary is dynamic — these aren't contradictory.

## Consolidated Revision Plan

### 1. EXPLICIT ASSUMPTIONS SECTION (new)
Add Section 2.5 "Assumptions and Boundary Conditions" stating:
- A1: Decisions are approximately independent (breaks for hierarchical tasks)
- A2: Novelty fraction ν is roughly constant during task execution (breaks if agent learns on-the-fly)
- A3: Verification requires inspecting output (breaks if formal verification exists)
- A4: Human intent exists prior to execution (breaks for exploratory/creative work — actually strengthens our argument)
For each, state what happens if it breaks.

### 2. ADD VERIFIABILITY DIMENSION (revise model)
Augment novelty ν with verifiability v ∈ [0,1]:
- High verifiability + low novelty → agents excel, H ~ O(1)
- High verifiability + high novelty → agents can self-correct, H ~ O(E) but low coefficient
- Low verifiability + any novelty → human judgment required, H ~ O(E) with high coefficient
This captures Karpathy's framework and explains the "jagged intelligence" of LLMs.

### 3. ADD MARCH OF NINES ANALYSIS (new subsection in simulations)
Simulate multi-step workflows where per-step reliability compounds:
- Show that end-to-end reliability drops exponentially with steps
- Show that achieving target reliability requires O(E) human checkpoints regardless

### 4. ADD EMPIRICAL EVIDENCE SUBSECTION
Cite Nielsen/Collison finding on Nobel discoveries per dollar.
Cite Karpathy's 80/20 demo/production gap.
Cite SWE-EVO (19-21% vs 65%) as novelty-dependent performance drop.

### 5. STRENGTHEN "CONDITIONS FOR FALSIFICATION" (new subsection in Discussion)
State explicitly what would make H sublinear:
- Continual learning during task execution (Sutskever/Patel)
- Formal/automated verification of open-ended outputs
- Agent develops own intent and doesn't need human specification
- New cognitive primitives that compress specification (Nielsen)

### 6. TEMPORAL SCOPING
Add clear language: our claim is about the current and near-term regime where agents execute human intent. Explicitly acknowledge this could change with architectural breakthroughs.

### 7. MORE NUANCED DISCUSSION
- Acknowledge constant-factor improvements are genuinely transformative
- Don't overstate: 10x productivity gain at same scaling class is enormous
- The boundary between novel and routine is dynamic and shifts in our favor over time
- "Phase transitions" possible if new cognitive tools restructure what counts as novel
