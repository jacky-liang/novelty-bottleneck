"""
Simulation: Human Effort Scaling in AI-Assisted Work

Models a task as a sequence of E decision points. At each point:
- The agent attempts to infer the correct decision from its prior
- If the agent is wrong, human must intervene (specification or correction)
- Human must verify outputs periodically

We measure H (human effort) as a function of E under varying:
- novelty (ν): fraction of decisions where agent prior is uninformative
- agent_capability: probability of correct decision on "routine" decisions
- self_correction: whether agent can detect and fix its own errors
- checkpoint_interval: how often human verifies
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple
import json

@dataclass
class SimConfig:
    name: str
    novelty: float  # fraction of decisions that are "novel"
    agent_accuracy_routine: float  # P(correct) on routine decisions
    agent_accuracy_novel: float  # P(correct) on novel decisions
    self_correction_rate: float  # P(agent catches own error)
    verification_cost: float  # cost per verified decision
    correction_cost: float  # cost per corrected decision
    spec_cost: float  # cost per specification bit

def simulate_task(E: int, config: SimConfig, rng: np.random.Generator) -> dict:
    """Simulate a task of effort E and return human effort breakdown."""
    
    H_spec = 0.0
    H_verify = 0.0
    H_correct = 0.0
    
    errors_accumulated = 0
    total_errors = 0
    
    for i in range(E):
        is_novel = rng.random() < config.novelty
        
        if is_novel:
            # Novel decision: agent has low accuracy, human must often specify
            correct = rng.random() < config.agent_accuracy_novel
            # Human must provide specification for novel decisions
            H_spec += config.spec_cost
        else:
            # Routine decision: agent has high accuracy
            correct = rng.random() < config.agent_accuracy_routine
        
        if not correct:
            # Can agent self-correct?
            if rng.random() < config.self_correction_rate:
                pass  # Agent catches and fixes its own error
            else:
                errors_accumulated += 1
                total_errors += 1
    
    # Verification: human checks output
    # Cost proportional to output size (all E decisions)
    # But can be sampled — check sqrt(E) items for low-stakes, all for high-stakes
    H_verify = E * config.verification_cost
    
    # Correction: human must fix accumulated errors
    H_correct = errors_accumulated * config.correction_cost
    
    H_total = H_spec + H_verify + H_correct
    
    return {
        'E': E,
        'H_total': H_total,
        'H_spec': H_spec,
        'H_verify': H_verify,
        'H_correct': H_correct,
        'total_errors': total_errors,
        'novelty': config.novelty,
    }


def run_scaling_experiment(configs: List[SimConfig], 
                           E_values: List[int],
                           n_trials: int = 50) -> dict:
    """Run experiments across task sizes and configurations."""
    
    rng = np.random.default_rng(42)
    results = {}
    
    for config in configs:
        config_results = []
        for E in E_values:
            trial_results = []
            for _ in range(n_trials):
                r = simulate_task(E, config, rng)
                trial_results.append(r)
            
            # Average across trials
            avg = {
                'E': E,
                'H_total_mean': np.mean([r['H_total'] for r in trial_results]),
                'H_total_std': np.std([r['H_total'] for r in trial_results]),
                'H_spec_mean': np.mean([r['H_spec'] for r in trial_results]),
                'H_verify_mean': np.mean([r['H_verify'] for r in trial_results]),
                'H_correct_mean': np.mean([r['H_correct'] for r in trial_results]),
                'H_total_over_E': np.mean([r['H_total']/r['E'] for r in trial_results]),
            }
            config_results.append(avg)
        
        results[config.name] = config_results
    
    return results


def run_divergence_experiment(E_values: List[int], n_trials: int = 100) -> dict:
    """
    Simulate agent trajectory divergence (random walk model).
    Shows that without checkpoints, error grows as sqrt(E),
    and checkpoints needed scale linearly with E.
    """
    rng = np.random.default_rng(123)
    results = []
    
    for E in E_values:
        deviations = []
        for _ in range(n_trials):
            # Random walk: each step adds N(0, 1) error
            errors = rng.normal(0, 0.1, size=E)
            cumulative = np.cumsum(errors)
            final_deviation = np.abs(cumulative[-1])
            max_deviation = np.max(np.abs(cumulative))
            deviations.append({
                'final': final_deviation,
                'max': max_deviation,
            })
        
        results.append({
            'E': E,
            'mean_final_deviation': np.mean([d['final'] for d in deviations]),
            'mean_max_deviation': np.mean([d['max'] for d in deviations]),
        })
    
    return results


def run_mutual_info_experiment(E_values: List[int], 
                                MI_values: List[float],
                                n_trials: int = 50) -> dict:
    """
    Test how mutual information (shared prior) affects H scaling.
    MI_value represents fraction of intent bits the agent can infer.
    """
    rng = np.random.default_rng(456)
    results = {}
    
    for mi in MI_values:
        mi_results = []
        for E in E_values:
            trial_H = []
            for _ in range(n_trials):
                H = 0
                for i in range(E):
                    # Each decision has 1 bit of intent
                    # Agent can infer with probability = mi
                    if rng.random() > mi:
                        # Human must specify
                        H += 1.0
                    # Verification: always some cost
                    H += 0.05  # small per-decision verification cost
                trial_H.append(H)
            
            mi_results.append({
                'E': E,
                'H_mean': np.mean(trial_H),
                'H_std': np.std(trial_H),
                'H_over_E': np.mean(trial_H) / E,
            })
        results[f'MI={mi:.1f}'] = mi_results
    
    return results


def run_novelty_fraction_experiment(E_max: int = 1000, n_trials: int = 50) -> dict:
    """
    Test the claim that when E is large and some fraction is novel,
    the linear component dominates.
    
    H = ν*E (novel, linear) + (1-ν)*log(E) (routine, sublinear) + verification
    """
    rng = np.random.default_rng(789)
    novelty_values = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0]
    E_values = list(range(10, E_max + 1, 10))
    
    results = {}
    for nu in novelty_values:
        nu_results = []
        for E in E_values:
            # Analytical model
            H_novel = nu * E * 1.0  # linear component
            H_routine = (1 - nu) * np.log2(max(E, 1)) * 2.0  # sublinear component  
            H_verify = 0.05 * E  # always linear in output size
            H_total = H_novel + H_routine + H_verify
            
            nu_results.append({
                'E': E,
                'H_total': H_total,
                'H_novel': H_novel,
                'H_routine': H_routine,
                'H_verify': H_verify,
                'H_over_E': H_total / E,
            })
        results[f'nu={nu}'] = nu_results
    
    return results


def plot_all(results_scaling, results_divergence, results_mi, results_novelty):
    """Generate all figures for the paper."""
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    # --- Plot 1: H vs E for different configurations ---
    ax = axes[0, 0]
    for name, data in results_scaling.items():
        Es = [d['E'] for d in data]
        Hs = [d['H_total_mean'] for d in data]
        ax.plot(Es, Hs, '-o', label=name, markersize=3)
    ax.set_xlabel('Task Effort E')
    ax.set_ylabel('Human Effort H')
    ax.set_title('H vs E: Different Agent Configurations')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    # --- Plot 2: H/E ratio vs E ---
    ax = axes[0, 1]
    for name, data in results_scaling.items():
        Es = [d['E'] for d in data]
        ratios = [d['H_total_over_E'] for d in data]
        ax.plot(Es, ratios, '-o', label=name, markersize=3)
    ax.set_xlabel('Task Effort E')
    ax.set_ylabel('H/E Ratio')
    ax.set_title('H/E Convergence (Linear → Constant)')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    # --- Plot 3: Random Walk Divergence ---
    ax = axes[0, 2]
    Es = [d['E'] for d in results_divergence]
    devs = [d['mean_max_deviation'] for d in results_divergence]
    sqrt_Es = [np.sqrt(E) * 0.1 * np.sqrt(2/np.pi) * np.sqrt(np.log(E)) for E in Es]
    ax.plot(Es, devs, '-', label='Mean Max Deviation', linewidth=2)
    ax.plot(Es, [np.sqrt(E)*0.15 for E in Es], '--', label='O(√E) reference', alpha=0.7)
    ax.set_xlabel('Task Length E')
    ax.set_ylabel('Max Trajectory Deviation')
    ax.set_title('Agent Trajectory Divergence')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # --- Plot 4: Mutual Information Effect ---
    ax = axes[1, 0]
    for name, data in results_mi.items():
        Es = [d['E'] for d in data]
        Hs = [d['H_mean'] for d in data]
        ax.plot(Es, Hs, '-o', label=name, markersize=3)
    # Add reference lines
    Es_ref = [d['E'] for d in list(results_mi.values())[0]]
    ax.plot(Es_ref, Es_ref, ':', color='gray', alpha=0.5, label='H=E (no agent)')
    ax.set_xlabel('Task Effort E')
    ax.set_ylabel('Human Effort H')
    ax.set_title('Effect of Mutual Information on H')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    # --- Plot 5: Novelty Fraction - H/E convergence ---
    ax = axes[1, 1]
    for name, data in results_novelty.items():
        Es = [d['E'] for d in data]
        ratios = [d['H_over_E'] for d in data]
        ax.plot(Es, ratios, '-', label=name, linewidth=1.5)
    ax.set_xlabel('Task Effort E')
    ax.set_ylabel('H/E Ratio')
    ax.set_title('Novelty Fraction: Linear Dominance')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    # --- Plot 6: H decomposition for high-novelty case ---
    ax = axes[1, 2]
    high_novelty_data = results_scaling.get('High Novelty (ν=0.8)', 
                         results_scaling.get(list(results_scaling.keys())[-1]))
    Es = [d['E'] for d in high_novelty_data]
    H_spec = [d['H_spec_mean'] for d in high_novelty_data]
    H_verify = [d['H_verify_mean'] for d in high_novelty_data]
    H_correct = [d['H_correct_mean'] for d in high_novelty_data]
    
    ax.stackplot(Es, H_spec, H_verify, H_correct, 
                 labels=['Specification', 'Verification', 'Correction'],
                 alpha=0.7)
    ax.set_xlabel('Task Effort E')
    ax.set_ylabel('Human Effort H')
    ax.set_title('H Decomposition (High Novelty)')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/claude/paper/figures/scaling_results.png', dpi=150, bbox_inches='tight')
    plt.savefig('/home/claude/paper/figures/scaling_results.pdf', dpi=150, bbox_inches='tight')
    plt.close()
    
    # --- Additional figure: Log-log plot to show scaling exponent ---
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    ax = axes[0]
    for name, data in results_scaling.items():
        Es = [d['E'] for d in data]
        Hs = [d['H_total_mean'] for d in data]
        ax.loglog(Es, Hs, '-o', label=name, markersize=3)
    # Reference lines
    ax.loglog(Es, Es, ':', color='gray', alpha=0.5, label='O(E)')
    ax.loglog(Es, [np.sqrt(e)*5 for e in Es], '--', color='gray', alpha=0.5, label='O(√E)')
    ax.loglog(Es, [np.log2(e)*10 for e in Es], '-.', color='gray', alpha=0.5, label='O(log E)')
    ax.set_xlabel('Task Effort E (log scale)')
    ax.set_ylabel('Human Effort H (log scale)')
    ax.set_title('Log-Log Scaling Analysis')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    # Fit scaling exponents
    ax = axes[1]
    exponents = {}
    for name, data in results_scaling.items():
        Es = np.array([d['E'] for d in data])
        Hs = np.array([d['H_total_mean'] for d in data])
        # Fit log(H) = α * log(E) + c
        mask = Es > 0
        log_E = np.log(Es[mask])
        log_H = np.log(Hs[mask])
        coeffs = np.polyfit(log_E, log_H, 1)
        exponents[name] = coeffs[0]
    
    names = list(exponents.keys())
    exp_vals = [exponents[n] for n in names]
    bars = ax.barh(range(len(names)), exp_vals, color=['#2196F3', '#4CAF50', '#FF9800', '#F44336'])
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel('Scaling Exponent α (H ~ E^α)')
    ax.set_title('Fitted Scaling Exponents')
    ax.axvline(x=1.0, color='red', linestyle='--', alpha=0.5, label='Linear (α=1)')
    ax.axvline(x=0.5, color='blue', linestyle='--', alpha=0.5, label='√E (α=0.5)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    for i, v in enumerate(exp_vals):
        ax.text(v + 0.02, i, f'{v:.2f}', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('/home/claude/paper/figures/scaling_exponents.png', dpi=150, bbox_inches='tight')
    plt.savefig('/home/claude/paper/figures/scaling_exponents.pdf', dpi=150, bbox_inches='tight')
    plt.close()
    
    return exponents


def main():
    print("=" * 60)
    print("Running Human Effort Scaling Simulations")
    print("=" * 60)
    
    # Define configurations
    configs = [
        SimConfig("Low Novelty (ν=0.1)", novelty=0.1, 
                  agent_accuracy_routine=0.95, agent_accuracy_novel=0.3,
                  self_correction_rate=0.0, verification_cost=0.05,
                  correction_cost=2.0, spec_cost=1.0),
        SimConfig("Medium Novelty (ν=0.3)", novelty=0.3,
                  agent_accuracy_routine=0.95, agent_accuracy_novel=0.3,
                  self_correction_rate=0.0, verification_cost=0.05,
                  correction_cost=2.0, spec_cost=1.0),
        SimConfig("High Novelty (ν=0.8)", novelty=0.8,
                  agent_accuracy_routine=0.95, agent_accuracy_novel=0.3,
                  self_correction_rate=0.0, verification_cost=0.05,
                  correction_cost=2.0, spec_cost=1.0),
        SimConfig("High Cap + Self-Correct", novelty=0.3,
                  agent_accuracy_routine=0.99, agent_accuracy_novel=0.7,
                  self_correction_rate=0.8, verification_cost=0.02,
                  correction_cost=2.0, spec_cost=1.0),
    ]
    
    E_values = [10, 25, 50, 100, 200, 500, 1000, 2000, 5000]
    
    # Run experiments
    print("\n1. Running scaling experiment...")
    results_scaling = run_scaling_experiment(configs, E_values)
    
    print("2. Running divergence experiment...")
    results_divergence = run_divergence_experiment(E_values)
    
    print("3. Running mutual information experiment...")
    MI_values = [0.0, 0.3, 0.6, 0.9, 0.99]
    results_mi = run_mutual_info_experiment(E_values, MI_values)
    
    print("4. Running novelty fraction experiment...")
    results_novelty = run_novelty_fraction_experiment(E_max=2000)
    
    # Generate plots
    print("5. Generating figures...")
    exponents = plot_all(results_scaling, results_divergence, results_mi, results_novelty)
    
    # Print summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    
    print("\nScaling Exponents (H ~ E^α):")
    for name, exp in exponents.items():
        print(f"  {name}: α = {exp:.3f}")
    
    print("\nH/E ratios at E=5000:")
    for name, data in results_scaling.items():
        last = data[-1]
        print(f"  {name}: H/E = {last['H_total_over_E']:.3f}")
    
    print("\nMutual Information effect at E=5000:")
    for name, data in results_mi.items():
        last = data[-1]
        print(f"  {name}: H/E = {last['H_over_E']:.3f}")
    
    print("\nNovelty dominance at E=2000:")
    for name, data in results_novelty.items():
        last = data[-1]
        print(f"  {name}: H/E = {last['H_over_E']:.4f}")
    
    # Save numerical results
    summary = {
        'exponents': exponents,
        'scaling_results': {k: v[-1] for k, v in results_scaling.items()},
        'mi_results': {k: v[-1] for k, v in results_mi.items()},
    }
    with open('/home/claude/paper/notes/simulation_results.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\nFigures saved to /home/claude/paper/figures/")
    print("Results saved to /home/claude/paper/notes/simulation_results.json")


if __name__ == '__main__':
    main()
