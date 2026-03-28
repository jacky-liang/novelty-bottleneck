# The Novelty Bottleneck

**A Framework for Understanding Human Effort Scaling in AI-Assisted Work**

Paper arguing that human effort scales linearly with task complexity when working with AI agents, and that this bottleneck is structural (driven by task novelty) rather than a capability limitation that scaling alone can overcome.

## Key Claims

1. There is no smooth sublinear regime for human effort — it transitions sharply from O(E) to O(1)
2. Better agents improve the coefficient on human effort but not the scaling exponent
3. Optimal team size *decreases* as AI agents improve (AI-era Brooks's Law)
4. Wall-clock time achieves O(√E) through team parallelism but total effort remains O(E)
5. AI is bottlenecked on frontier research but unbottlenecked on exploiting existing knowledge

## Repository Structure

```
├── paper.tex          # LaTeX source
├── paper.pdf          # Compiled paper (19 pages)
├── code/
│   ├── simulation.py       # Core scaling simulations (Fig 1-2, Tables 1-2)
│   ├── org_scaling.py       # Organizational scaling simulations (Fig 4, Table 4)
│   └── additional_sims.py   # March of nines & verifiability (Fig 3, 5)
├── figures/
│   ├── scaling_results.pdf/.png
│   ├── scaling_exponents.pdf/.png
│   ├── org_scaling.pdf/.png
│   ├── march_of_nines.pdf/.png
│   └── verifiability.pdf/.png
└── notes/
    ├── PLAN.md                  # Original project plan
    ├── formal_model.md          # Mathematical development notes
    ├── literature_review.md     # Literature review notes
    ├── revision_plan.md         # Peer review synthesis & revision plan
    ├── assumed_vs_derived.md    # What is assumed vs. derived (key document)
    ├── simulation_results.json  # Numerical results
    └── org_scaling_results.json # Org scaling numerical results
```

## Reproducing Results

Requirements: Python 3.10+, NumPy, Matplotlib

```bash
# Run all simulations and generate figures
python code/simulation.py
python code/org_scaling.py
python code/additional_sims.py

# Compile paper (requires LaTeX)
pdflatex paper.tex && pdflatex paper.tex
```

All simulations use fixed random seeds for exact reproducibility. See §4.1 of the paper for full specification of all parameters.

## Citation

```
@article{noveltybottleneck2026,
  title={The Novelty Bottleneck: A Framework for Understanding Human Effort Scaling in AI-Assisted Work},
  author={Liang, Jacky},
  year={2026},
  month={March}
}
```
