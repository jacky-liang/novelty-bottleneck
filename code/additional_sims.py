"""
Additional simulations: March of Nines and Verifiability Frontier

1. March of Nines: Shows that per-step reliability compounds, requiring
   O(E) human checkpoints to maintain end-to-end reliability.

2. Verifiability Frontier: Shows how the verifiable/non-verifiable distinction
   interacts with novelty to determine human effort scaling.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def march_of_nines():
    """
    Karpathy's March of Nines: each additional nine of reliability
    requires roughly equal engineering effort.
    
    For a multi-step workflow of E steps, end-to-end reliability is p^E.
    To achieve target reliability R, need per-step p = R^(1/E).
    The number of nines needed: -log10(1-p).
    """
    E_values = np.array([1, 5, 10, 20, 50, 100, 200, 500])
    target_reliability = 0.95  # 95% end-to-end success
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    
    # Plot 1: End-to-end reliability vs steps for different per-step reliabilities
    ax = axes[0]
    steps = np.arange(1, 201)
    for p in [0.999, 0.99, 0.95, 0.90, 0.80]:
        e2e = p ** steps
        nines_label = f'{p*100:.1f}%'
        ax.plot(steps, e2e, '-', label=f'p={nines_label}', linewidth=1.5)
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='50% success')
    ax.set_xlabel('Number of Steps E')
    ax.set_ylabel('End-to-End Reliability')
    ax.set_title('Reliability Decay in Multi-Step Workflows')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.05)
    
    # Plot 2: Required per-step reliability to achieve target end-to-end
    ax = axes[1]
    targets = [0.99, 0.95, 0.90, 0.80]
    for R in targets:
        required_p = R ** (1.0 / steps)
        nines = -np.log10(1 - required_p)
        ax.plot(steps, nines, '-', label=f'Target={R*100:.0f}%', linewidth=1.5)
    ax.set_xlabel('Number of Steps E')
    ax.set_ylabel('Required Nines per Step')
    ax.set_title('Nines Required vs Task Length')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Human checkpoints needed vs E
    # Model: human checks every k steps; if error detected, corrects.
    # To keep end-to-end reliability above R with per-step p:
    # Need checkpoint interval k such that p^k > threshold
    # Number of checkpoints = E/k = E * (-log(threshold)) / (-log(p))
    ax = axes[2]
    per_step_ps = [0.99, 0.95, 0.90]
    threshold = 0.8  # minimum segment reliability before checkpoint
    E_range = np.arange(10, 501)
    
    for p in per_step_ps:
        if p >= 1.0:
            continue
        k = np.log(threshold) / np.log(p)  # max steps between checkpoints
        checkpoints = E_range / k
        ax.plot(E_range, checkpoints, '-', 
                label=f'p={p*100:.0f}%, k≈{k:.0f}', linewidth=1.5)
    
    # Reference: linear
    ax.plot(E_range, E_range * 0.01, ':', color='gray', alpha=0.5, label='O(E) reference')
    ax.set_xlabel('Task Length E')
    ax.set_ylabel('Human Checkpoints Required')
    ax.set_title('Checkpoints Scale Linearly with E')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/claude/paper/figures/march_of_nines.pdf', dpi=150, bbox_inches='tight')
    plt.savefig('/home/claude/paper/figures/march_of_nines.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("March of Nines results:")
    print(f"  At p=99%, E=100: end-to-end = {0.99**100:.3f}")
    print(f"  At p=95%, E=100: end-to-end = {0.95**100:.6f}")
    print(f"  At p=99%, E=10: end-to-end = {0.99**10:.3f}")
    print(f"  Checkpoints for p=95%, threshold=80%: every {np.log(0.8)/np.log(0.95):.1f} steps")
    print(f"  Checkpoints for p=99%, threshold=80%: every {np.log(0.8)/np.log(0.99):.1f} steps")


def verifiability_frontier():
    """
    Model combining novelty and verifiability.
    
    Two dimensions:
    - novelty ν: whether agent prior covers the task
    - verifiability v: whether output correctness can be automatically checked
    
    H depends on both:
    - Low ν, high v: agent handles it autonomously (H ≈ 0)
    - Low ν, low v: agent does it but human must verify (H ~ c_v * E)
    - High ν, high v: agent tries, self-corrects via verification (H ~ ν * E, low coeff)
    - High ν, low v: agent can't self-correct, human must specify + verify (H ~ ν * E, high coeff)
    """
    E = 1000
    nu_values = np.linspace(0, 1, 50)
    v_values = np.linspace(0, 1, 50)
    
    NU, V = np.meshgrid(nu_values, v_values)
    
    # H/E ratio as function of novelty and verifiability
    # When verifiable: agent can self-correct, reducing effective novelty
    effective_nu = NU * (1 - 0.8 * V)  # verifiability reduces novelty impact by up to 80%
    c_v = 0.05 * (1 - V)  # verification cost drops when auto-verifiable
    H_over_E = effective_nu + c_v + 0.02  # small base cost
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    
    # Plot 1: Heatmap of H/E
    ax = axes[0]
    im = ax.contourf(NU, V, H_over_E, levels=20, cmap='RdYlGn_r')
    plt.colorbar(im, ax=ax, label='H/E ratio')
    ax.set_xlabel('Novelty ν')
    ax.set_ylabel('Verifiability v')
    ax.set_title('H/E Ratio: Novelty × Verifiability')
    
    # Annotate quadrants
    ax.text(0.15, 0.85, 'Auto\nagent', ha='center', va='center', fontsize=8, 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.text(0.85, 0.85, 'Self-\ncorrecting', ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.text(0.15, 0.15, 'Human\nverifies', ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.text(0.85, 0.15, 'Human\nbottleneck', ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Plot 2: H/E vs novelty for different verifiability levels
    ax = axes[1]
    for v in [0.0, 0.3, 0.6, 0.9, 1.0]:
        eff_nu = nu_values * (1 - 0.8 * v)
        cv = 0.05 * (1 - v)
        h_ratio = eff_nu + cv + 0.02
        ax.plot(nu_values, h_ratio, '-', label=f'v={v:.1f}', linewidth=1.5)
    ax.set_xlabel('Novelty ν')
    ax.set_ylabel('H/E Ratio')
    ax.set_title('Verifiability Reduces but Doesn\'t Eliminate Linear Scaling')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Where different task types fall
    ax = axes[2]
    tasks = {
        'Code\n(tests exist)': (0.3, 0.9),
        'Code\n(novel arch.)': (0.8, 0.7),
        'Scientific\nwriting': (0.6, 0.2),
        'Data\npipeline': (0.2, 0.8),
        'Product\nstrategy': (0.9, 0.1),
        'Bug fix\n(repro)': (0.1, 0.95),
        'Research\n(frontier)': (0.95, 0.15),
        'Refactoring': (0.15, 0.85),
    }
    
    for name, (nu, v) in tasks.items():
        eff_nu = nu * (1 - 0.8 * v)
        cv = 0.05 * (1 - v)
        h_ratio = eff_nu + cv + 0.02
        color = plt.cm.RdYlGn_r(h_ratio / 1.0)
        ax.scatter(nu, v, s=100, c=[color], edgecolors='black', linewidth=0.5, zorder=5)
        ax.annotate(name, (nu, v), textcoords="offset points", 
                   xytext=(0, 12), ha='center', fontsize=6.5)
    
    ax.set_xlabel('Novelty ν')
    ax.set_ylabel('Verifiability v')
    ax.set_title('Task Taxonomy: Where Work Falls')
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/claude/paper/figures/verifiability.pdf', dpi=150, bbox_inches='tight')
    plt.savefig('/home/claude/paper/figures/verifiability.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("\nVerifiability Frontier results:")
    for name, (nu, v) in sorted(tasks.items(), key=lambda x: x[1][0]):
        eff_nu = nu * (1 - 0.8 * v)
        cv = 0.05 * (1 - v)
        h_ratio = eff_nu + cv + 0.02
        print(f"  {name.replace(chr(10), ' ')}: ν={nu:.2f}, v={v:.2f}, H/E={h_ratio:.3f}")


if __name__ == '__main__':
    march_of_nines()
    verifiability_frontier()
    print("\nFigures saved.")
