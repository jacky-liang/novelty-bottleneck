"""
Simulation: Organizational Scaling of Human Effort with AI Agents

Models n humans, each paired with AI agents, collaborating on a task of effort E.

Key components:
- Work term: c * E distributed across n humans
- Coordination term: beta * n^2 (Brooks's Law)
- Integration amplification: gamma * n * agent_throughput
- Agent throughput amplification factor

We measure:
- Wall-clock time T(n) = c*E/n + beta*n + gamma*n*throughput_amplifier
- Total human effort H_total(n) = c*E + beta*n^2 + gamma*n^2*throughput_amplifier
- Optimal team size n* as a function of agent capability
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List
import json


@dataclass
class OrgConfig:
    name: str
    c: float          # per-decision human effort coefficient
    beta: float        # coordination cost per pair of humans
    gamma: float       # integration cost amplified by agent throughput
    agent_throughput: float  # how much more output each human-agent pair produces vs human alone


def wall_clock_time(E: int, n: int, config: OrgConfig) -> float:
    """Wall-clock time for n humans with agents on task E."""
    if n == 0:
        return float('inf')
    work = config.c * E / n
    coordination = config.beta * n
    integration = config.gamma * n * config.agent_throughput
    return work + coordination + integration


def total_human_effort(E: int, n: int, config: OrgConfig) -> float:
    """Total human-hours across all n humans."""
    work = config.c * E
    coordination = config.beta * n * (n - 1) / 2  # pairwise
    integration = config.gamma * n * (n - 1) / 2 * config.agent_throughput
    return work + coordination + integration


def optimal_team_size(E: int, config: OrgConfig) -> float:
    """Analytical optimal n minimizing wall-clock time."""
    # T(n) = cE/n + (beta + gamma*throughput)*n
    # dT/dn = -cE/n^2 + beta + gamma*throughput = 0
    # n* = sqrt(cE / (beta + gamma*throughput))
    denom = config.beta + config.gamma * config.agent_throughput
    if denom <= 0:
        return float('inf')
    return np.sqrt(config.c * E / denom)


def run_org_scaling_experiment():
    """Run the full organizational scaling experiment."""
    
    # Define configurations representing different AI capability levels
    configs = [
        OrgConfig("No AI", c=1.0, beta=0.5, gamma=0.0, agent_throughput=1.0),
        OrgConfig("Basic AI (2x throughput)", c=0.5, beta=0.5, gamma=0.1, agent_throughput=2.0),
        OrgConfig("Strong AI (5x throughput)", c=0.2, beta=0.5, gamma=0.1, agent_throughput=5.0),
        OrgConfig("Frontier AI (10x throughput)", c=0.1, beta=0.5, gamma=0.1, agent_throughput=10.0),
    ]
    
    E_values = [100, 500, 1000, 5000, 10000]
    n_values = list(range(1, 51))
    
    results = {}
    
    # --- Experiment 1: Wall-clock time vs team size for fixed E ---
    E_fixed = 5000
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    # Plot 1: Wall-clock time vs n
    ax = axes[0, 0]
    for config in configs:
        times = [wall_clock_time(E_fixed, n, config) for n in n_values]
        ax.plot(n_values, times, '-', label=config.name, linewidth=2)
        n_opt = optimal_team_size(E_fixed, config)
        if n_opt < 50:
            t_opt = wall_clock_time(E_fixed, max(1, int(round(n_opt))), config)
            ax.plot(n_opt, t_opt, 'o', markersize=8, color=ax.get_lines()[-1].get_color())
    ax.set_xlabel('Team Size n')
    ax.set_ylabel('Wall-Clock Time T')
    ax.set_title(f'Wall-Clock Time vs Team Size (E={E_fixed})')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, min(3000, max([wall_clock_time(E_fixed, 1, c) for c in configs]) * 1.1))
    
    # Plot 2: Total human effort vs n
    ax = axes[0, 1]
    for config in configs:
        efforts = [total_human_effort(E_fixed, n, config) for n in n_values]
        ax.plot(n_values, efforts, '-', label=config.name, linewidth=2)
    ax.set_xlabel('Team Size n')
    ax.set_ylabel('Total Human Effort H_total')
    ax.set_title(f'Total Human Effort vs Team Size (E={E_fixed})')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Optimal team size vs E
    ax = axes[0, 2]
    for config in configs:
        n_opts = [optimal_team_size(E, config) for E in E_values]
        ax.plot(E_values, n_opts, '-o', label=config.name, linewidth=2, markersize=5)
    ax.set_xlabel('Task Effort E')
    ax.set_ylabel('Optimal Team Size n*')
    ax.set_title('Optimal Team Size vs Task Complexity')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    
    # Plot 4: Optimal team size vs agent throughput (for fixed E)
    ax = axes[1, 0]
    throughputs = np.linspace(1, 20, 50)
    for E_val in [500, 2000, 10000]:
        n_opts = []
        for t in throughputs:
            cfg = OrgConfig("", c=0.3, beta=0.5, gamma=0.1, agent_throughput=t)
            n_opts.append(optimal_team_size(E_val, cfg))
        ax.plot(throughputs, n_opts, '-', label=f'E={E_val}', linewidth=2)
    ax.set_xlabel('Agent Throughput Multiplier')
    ax.set_ylabel('Optimal Team Size n*')
    ax.set_title('Better Agents → Smaller Teams')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 5: Minimum wall-clock time vs E (at optimal n)
    ax = axes[1, 1]
    E_range = np.logspace(1, 5, 50).astype(int)
    for config in configs:
        min_times = []
        for E in E_range:
            n_opt = max(1, int(round(optimal_team_size(E, config))))
            min_times.append(wall_clock_time(E, n_opt, config))
        ax.loglog(E_range, min_times, '-', label=config.name, linewidth=2)
    # Reference lines
    ax.loglog(E_range, np.sqrt(E_range) * 3, ':', color='gray', alpha=0.5, label='O(√E)')
    ax.loglog(E_range, E_range * 0.1, '--', color='gray', alpha=0.5, label='O(E)')
    ax.set_xlabel('Task Effort E')
    ax.set_ylabel('Minimum Wall-Clock Time T*')
    ax.set_title('Best-Case Time vs Task Complexity')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    # Plot 6: Efficiency - fraction of human effort that is "useful work" vs coordination
    ax = axes[1, 2]
    for config in configs:
        if config.agent_throughput == 1.0 and config.gamma == 0.0:
            continue  # skip no-AI for clearer plot
        efficiencies = []
        for n in n_values:
            work = config.c * E_fixed
            coord = config.beta * n * (n - 1) / 2
            integ = config.gamma * n * (n - 1) / 2 * config.agent_throughput
            total = work + coord + integ
            efficiencies.append(work / total if total > 0 else 0)
        ax.plot(n_values, efficiencies, '-', label=config.name, linewidth=2)
    ax.set_xlabel('Team Size n')
    ax.set_ylabel('Work Efficiency (useful / total)')
    ax.set_title('Coordination Overhead Fraction')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.05)
    
    plt.tight_layout()
    plt.savefig('/home/claude/paper/figures/org_scaling.png', dpi=150, bbox_inches='tight')
    plt.savefig('/home/claude/paper/figures/org_scaling.pdf', dpi=150, bbox_inches='tight')
    plt.close()
    
    # --- Compute and print key results ---
    print("=" * 60)
    print("ORGANIZATIONAL SCALING RESULTS")
    print("=" * 60)
    
    print(f"\nOptimal team sizes for E={E_fixed}:")
    for config in configs:
        n_opt = optimal_team_size(E_fixed, config)
        t_opt = wall_clock_time(E_fixed, max(1, int(round(n_opt))), config)
        print(f"  {config.name}: n* = {n_opt:.1f}, T* = {t_opt:.1f}")
    
    print(f"\nOptimal team size scaling with agent throughput (E=5000, c=0.3, β=0.5, γ=0.1):")
    for t in [1, 2, 5, 10, 20]:
        cfg = OrgConfig("", c=0.3, beta=0.5, gamma=0.1, agent_throughput=t)
        print(f"  Throughput={t}x: n* = {optimal_team_size(5000, cfg):.1f}")
    
    print(f"\nMinimum wall-clock time scaling:")
    for config in configs:
        times_at_E = {}
        for E in [100, 1000, 10000]:
            n_opt = max(1, int(round(optimal_team_size(E, config))))
            times_at_E[E] = wall_clock_time(E, n_opt, config)
        # Fit scaling exponent
        Es = list(times_at_E.keys())
        Ts = list(times_at_E.values())
        if all(t > 0 for t in Ts):
            coeffs = np.polyfit(np.log(Es), np.log(Ts), 1)
            print(f"  {config.name}: T* ~ E^{coeffs[0]:.2f}")
    
    # Save key results
    summary = {
        'optimal_team_sizes': {
            config.name: {
                'n_star': round(optimal_team_size(E_fixed, config), 1),
                'T_star': round(wall_clock_time(E_fixed, max(1, int(round(optimal_team_size(E_fixed, config)))), config), 1)
            }
            for config in configs
        },
    }
    with open('/home/claude/paper/notes/org_scaling_results.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\nFigures saved to /home/claude/paper/figures/org_scaling.pdf")
    return summary


if __name__ == '__main__':
    run_org_scaling_experiment()
