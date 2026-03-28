# Literature Review Notes

## Key References and How They Relate

### Brooks (1975) - The Mythical Man-Month
- "Adding manpower to a late software project makes it later"
- Communication overhead: n people → n(n-1)/2 communication channels
- Essential vs accidental complexity (No Silver Bullet)
- DIRECTLY supports our thesis: even among humans, coordination doesn't scale sublinearly
- Brooks' distinction between essential and accidental complexity maps onto our novel/routine distinction

### Amdahl's Law (1967)
- Speedup = 1 / ((1-p) + p/N) where p is parallelizable fraction
- Serial fraction creates hard ceiling on parallelism benefits
- OUR ANALOGY: "novelty" is the serial fraction. It's the part that can't be delegated.
- Gustafson's counter: if problem size grows with processors, near-linear speedup possible
  - This maps to: if you use agents to do MORE routine work (not faster novel work), you get value

### Aschenbrenner (2024) - Situational Awareness  
- Predicts AGI by 2027, intelligence explosion shortly after
- Key claim: "Hundreds of millions of AGIs could automate AI research, compressing a decade of algorithmic progress into ≤1 year"
- OUR CRITIQUE: This assumes research parallelizes well. Our model says the novel/insight-generation part is serial. You can parallelize the routine execution downstream of insights, but not the insights themselves.
- His "OOMs" argument is about compute scaling, not about the serial bottleneck of insight generation

### Amodei (2024) - Machines of Loving Grace
- "Country of geniuses in a data center"
- Predicts 100 years of biology progress compressed into 5-10 years
- Key nuance: He acknowledges "human factors" as a bottleneck but treats it as a constant overhead
- OUR CRITIQUE: The "human factors" bottleneck IS the serial bottleneck, and it scales with task novelty
- His biology example actually supports our model: biology has many ROUTINE experiments that can be parallelized, with a serial chain of novel insights connecting them
- The 10x speedup claim is plausible for the routine parts; the insight chain is what limits overall compression

### Amodei (2025) - The Adolescence of Technology
- "AI is already substantially accelerating the rate of our progress in building the next generation of AI systems"
- Feedback loop: current AI builds next AI
- OUR FRAMEWORK: This works to the extent that AI research has become routine (better hyperparameter search, faster experiment iteration). The genuinely novel architectural insights remain serial.

### Dwarkesh Patel - "Will Scaling Work?" (2023)
- Key insight: "Self play doesn't require models to be perfect at judging their own reasoning. They just have to be better at evaluating reasoning than at doing it de novo"
- This relates to our verification point: verification is easier than generation, which is why H_verify might have a lower coefficient than H_spec
- But both are still O(E)

### SWE-bench / SWE-bench Pro / SWE-EVO
- SWE-bench: most tasks take <1 hour for experienced engineer — these are ROUTINE
- SWE-bench Pro: tasks requiring hours to days — more novel, multi-file
- SWE-EVO: GPT-5 resolves only 19-21% vs 65% on SWE-bench Verified
- KEY OBSERVATION: As task complexity/novelty increases, agent performance drops dramatically
- This is exactly what our model predicts: routine tasks → high agent success; novel tasks → low success
- The scaling of agent success rate with task complexity is our core empirical prediction

### No Silver Bullet (Brooks, 1986)
- Essential complexity: inherent in the problem
- Accidental complexity: introduced by tools/methods
- "There is no single development that promises even one order of magnitude improvement"
- Maps directly: AI agents remove accidental complexity but not essential complexity
- Essential complexity IS the novel part; accidental complexity IS the routine part
