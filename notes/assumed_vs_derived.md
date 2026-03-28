# What Is Assumed vs. What Is Derived

## ASSUMPTIONS (things we assert without proof)

A1. A task of effort E can be decomposed into ~E atomic decisions, each requiring 
    O(1) bits of intent to specify.

A2. Each decision is either "routine" (agent's prior covers it) or "novel" 
    (human must provide specification). The fraction that is novel is ν.

A3. The agent's error rate on routine decisions is bounded by some constant 
    (not zero), and errors accumulate without self-correction unless checkpointed.

A4. Verification of agent output requires inspecting a fraction of the output 
    proportional to its size, unless automated verification exists.

A5. The agent's prior is approximately fixed during a single task execution 
    (no meaningful within-task learning).

## DERIVED CONSEQUENCES (things that follow from assumptions but are non-obvious)

D1. H ~ (ν + c_v + c_c + c_d) · E  [linear scaling]
    - This follows directly from A1-A4. Semi-tautological.
    - But the NON-OBVIOUS part: there is no smooth sublinear regime. 
      H jumps from O(E) to O(1) with nothing in between. This surprised us 
      and is not assumed.

D2. Better agents improve coefficients, not exponents.
    - Higher accuracy → lower c_c. Better prior → lower ν. Self-verification → lower c_v.
    - But all of these are multiplicative constants on E, not changes to the power.
    - NON-OBVIOUS: you might expect that sufficiently good agents could change the 
      scaling class. They can't, within the model.

D3. For any nonzero ν, the linear term dominates at large E.
    - Even ν = 0.01 makes H/E converge to a positive constant.
    - NON-OBVIOUS: the routine sublinear savings become negligible at scale. 
      This means agents help LESS (in relative terms) on bigger tasks.

D4. Agent trajectory divergence requires O(E) checkpoints.
    - From A3: errors accumulate as random walk, deviation ~ √t.
    - Bounded deviation requires checkpoints every O(1) steps → O(E) total.
    - This is INDEPENDENT of specification — even with perfect spec, 
      correction effort is linear.

D5. March of nines: end-to-end reliability decays exponentially with E.
    - p^E → 0 for any p < 1. Checkpoints to maintain target reliability: O(E).
    - This gives a SECOND independent mechanism for linear H, 
      distinct from specification.

D6. [ORG SCALING] Optimal team size n* = √(cE/(β+γτ)).
    - Derived from minimizing wall-clock time T(n).
    - n* DECREASES as agent throughput τ increases.
    - NON-OBVIOUS: better agents make large teams LESS efficient, not more.

D7. [ORG SCALING] Wall-clock time T* ~ O(√E) but total effort H_total ~ O(E).
    - You can buy calendar speed but not cognitive savings.
    - NON-OBVIOUS: wall-clock and total-effort have different scaling classes.

D8. [RISK] The exploitation/exploration asymmetry.
    - Exploiting existing knowledge is routine (ν ≈ 0) → agents are unbottlenecked.
    - Generating new knowledge is novel (ν ≈ 1) → agents are bottlenecked.
    - NON-OBVIOUS: the risk profile is "effective at weaponizing, 
      mediocre at innovating" — a worse profile than "generally superhuman."

D9. [RECURSIVE IMPROVEMENT] Self-improvement is bounded by serial insight generation.
    - Novel architectural innovation has ν ≈ 1.
    - Clock speed helps but parallelism doesn't.
    - NON-OBVIOUS: fast takeoff in human-time possible, but only through 
      clock speed, not through parallel copies.

## WHAT COULD BREAK THE ASSUMPTIONS

- A1 breaks: tasks have hierarchical/compositional structure → effective decisions < E
- A2 breaks: the novel/routine boundary is fuzzy, not binary
- A3 breaks: agents achieve zero error rate on routine work
- A4 breaks: formal/automated verification eliminates human inspection
- A5 breaks: agents learn during task execution → ν shrinks dynamically

The most consequential: A5. If within-task learning works, 
ν(t) ~ 1/t → H_spec ~ O(log E). This is the continual learning escape route.
