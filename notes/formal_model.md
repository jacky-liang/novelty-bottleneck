# Formal Model: Human Effort Scaling in AI-Assisted Work

## Definitions

Let a task T be characterized by:
- E: total effort (a measure combining time and complexity, e.g., number of atomic decisions)
- H: human effort required (specification + verification + correction)
- A: AI agent effort (tokens, compute)

We decompose E into atomic decision units d_1, ..., d_E. Each decision d_i requires:
1. A specification bit s_i (what the human wants)
2. An execution step (the agent acts)
3. A verification step (checking correctness)

## Information-Theoretic Framework

### Specification Complexity
The task contains I(T) bits of intent — the information needed to fully specify the desired outcome.

Key claim: I(T) ~ O(E). Each decision unit contributes some bits of intent.

### Shared Prior
Let P_agent be the agent's prior distribution over "what the human wants" for each decision.
Let P_human be the human's actual intent distribution.

Define mutual information: M = I(P_agent; P_human)

When M is high, the agent can infer many specification bits without explicit human input.
When M is low, human must provide bits explicitly.

### Human Effort Decomposition

H = H_spec + H_verify + H_correct + H_decompose

H_spec: bits of intent that must be explicitly communicated
H_verify: effort to check agent outputs
H_correct: effort to fix agent errors
H_decompose: effort to break task into agent-digestible chunks

### Key Theorem (informal)

H_spec = I(T) - M = O(E) - M

For H to be sublinear, we need M to be "almost all" of I(T), i.e., M >= I(T) - o(E).

This happens when the agent's prior is very well-aligned with human intent — 
i.e., the task is "routine" from the perspective of their shared knowledge.

### Novelty Parameter

Define novelty ν ∈ [0,1] as the fraction of decisions where the agent's prior has 
low confidence (high entropy). Then:

H_spec ~ ν * E  (novel decisions require explicit specification)
H_verify ~ E * (1 - trust(agent))  (verification scales with output size)
H_correct ~ E * error_rate * correction_cost

For novel work (ν → 1): H ~ O(E)
For routine work (ν → 0): H ~ O(f(E)) where f could be sublinear

### The Verification Lower Bound

Even with perfect specification, verification is bounded below:
H_verify >= Ω(E^α) for some α > 0

Because the output is O(E) in size, and any meaningful verification requires 
reading/understanding at least a sample of it. 

If the agent is trusted (self-verifying), α could be small. 
But trust calibration itself requires O(E) experience.

### Random Walk Divergence Model

Model agent trajectory as: x_t = x*_t + Σ_{i=1}^{t} ε_i
where x*_t is the intended trajectory and ε_i are errors.

Expected deviation after t steps without correction: E[|x_t - x*_t|] ~ O(√t)

To keep deviation bounded by δ, need checkpoints every O(δ²) steps.
Number of checkpoints for task of length E: O(E / δ²)
This is linear in E for any fixed δ.

### When Can H Be Sublinear?

H can be sublinear if:
1. ν is small (task is routine) — but this bounds absolute E that's "novel"
2. Agent can self-verify reliably — reduces H_verify
3. Agent can self-correct — reduces H_correct
4. Specification is compressible against shared prior — reduces H_spec

All four require high mutual information M, which is exactly what "novelty" destroys.

### The Amortization Argument

Over many tasks T_1, ..., T_n from a similar distribution:
- Total novel bits across all tasks may grow sublinearly if tasks share structure
- H per task can decrease as shared prior grows
- But for each individual truly novel task, H ~ O(E) still holds

This is the "things get reclassified as routine over time" effect.
It improves aggregate H across tasks but not H for any single novel task.

## Implications for Recursive Self-Improvement

If an AI system is improving itself:
- The "task" is its own architecture modification
- E scales with the complexity of the improvement
- Novelty ν is high (by definition — if it were routine, it would already be done)
- Even if the AI is both "human" and "agent," the insight generation is serial
- No parallelism advantage for the genuinely novel part

Rate of self-improvement bounded by serial insight generation, not parallel compute.
