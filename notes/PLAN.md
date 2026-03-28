# Paper Plan: The Linear Bottleneck of Human Effort in AI-Assisted Work

## Hypothesis
For a task of total effort E, the human effort H required when using AI agents scales as H ~ O(E), not sublinearly. The linear coefficient is reduced by shared prior (mutual information between agent and human intent), but the scaling class remains linear for novel work.

## Key Claims to Test
1. H ~ O(E) empirically for current AI agent workflows
2. The bottleneck is specification, verification, and error correction — all O(E)
3. Sublinear H requires sufficient mutual information (shared prior) between agent and human
4. For genuinely novel work, shared prior is thin, forcing H back to O(E)
5. This constrains recursive self-improvement and "fast takeoff" scenarios

## Plan

### Phase 1: Formal Model
- Define E, H, A formally
- Model the information-theoretic relationship between specification complexity and task novelty
- Derive conditions under which H can be sublinear
- Show that novelty breaks these conditions

### Phase 2: Simulations
- Simulate agent-human collaboration under varying:
  - Task novelty (fraction of decisions not covered by prior)
  - Agent capability (prior coverage, error rate, self-correction ability)
  - Task size E
- Measure H as function of E under these conditions
- Test whether H/E converges to a constant or shrinks

### Phase 3: Thought Experiments & Mathematical Analysis
- Random walk model of agent trajectory divergence
- Information-theoretic lower bound on H
- Brooks's Law analogy — formal version
- Conditions for escaping linear scaling

### Phase 4: Literature Review
- Brooks (1975) - Mythical Man-Month
- Amdahl's Law and its analogs
- Recent AI scaling papers
- "Situational Awareness" (Leopold Aschenbrenner)
- Dwarkesh Patel interviews/blog posts on AI progress
- Dario Amodei "Machines of Loving Grace"
- Sam Altman on AGI timelines
- AI agent benchmarks (SWE-bench, etc.)
- Human-AI collaboration empirical studies

### Phase 5: Write Paper
- LaTeX, clean style
- Sections: Introduction, Model, Analysis, Simulations, Implications, Related Work, Discussion
