# 🧬 Algorithm & AI Optimization Core (`algos/`)

> **Owners:** M1 (ALGO Lead - QPSO, PSO, VRP) & M3 (ML Lead - GA, ACO, Benchmarks)

This directory contains the mathematical heart of the project: the **Quantum-Inspired Particle Swarm Optimization (QPSO)** engine, the multi-vehicle **Vehicle Routing Problem (VRP)** matrix formulator, the classical benchmark algorithms (**PSO**, **GA**, **ACO**, **Dijkstra**, **A***), and the statistical convergence analyzer.

---

## 🔬 Directory Organization

```
algos/
├── README.md                 # This file - mathematical & implementation reference
├── qpso.py                   # Quantum-Inspired PSO implementation (M1)
├── pso.py                    # Classical Velocity-Position PSO baseline (M1)
├── vrp_formulator.py         # Encodes OSMnx graph to distance/cost/demand matrices (M1)
├── convergence_analyzer.py   # Statistical comparisons & speedup metrics (M3)
├── algorithm_config.yaml     # Swarm size, iteration limits, hyperparameter bounds
└── classical/                # Benchmark implementations (M3)
    ├── __init__.py
    ├── dijkstra.py           # Single-vehicle exact shortest path
    ├── astar.py              # Euclidean-guided shortest path
    ├── genetic_algo.py       # Permutation GA with Order Crossover (OX) & swap mutation
    └── ant_colony.py         # ACO with pheromone deposit & evaporation (MMAS / ACS)
```

---

## ⚡ QPSO Mathematical Implementation Details

### Continuous-to-Discrete Mapping for VRP
The VRP permutation sequence for $N$ delivery stops and $K$ vehicles is encoded into continuous particle coordinates using **Random Keys (RK)** or **Smallest Position Value (SPV)**:
1. Each particle $X_i \in \mathbb{R}^N$ represents continuous values.
2. An ascending sort of indices maps the continuous vector $X_i$ to a discrete permutation sequence $\pi_i = (\pi_1, \pi_2, \dots, \pi_N)$.
3. Vehicle assignment partitions the permutation when cumulative vehicle load exceeds capacity $Q_{\max}$ or via $K-1$ divider thresholds.

### The Delta Potential Well Wave Equation
Unlike classical PSO which tracks particle velocity $V(t)$, QPSO assumes each particle is bound by a one-dimensional quantum delta potential well $V(x) = -\gamma \delta(x - p)$ centered at attractor $p$:

$$p_{ij}(t) = \phi \cdot P_{ij}(t) + (1 - \phi) \cdot G_j(t), \quad \phi \sim \mathcal{U}(0, 1)$$

Solving the time-independent Schrödinger equation:
$$\frac{d^2 \psi}{dx^2} + \frac{2m}{\hbar^2} [E + \gamma \delta(x - p)] \psi = 0$$

The normalized ground state wave function is:
$$\psi(x) = \frac{1}{\sqrt{L}} \exp\left(-\frac{|x - p|}{L}\right)$$

where $L = \frac{\hbar^2}{m\gamma}$ is the characteristic length of the potential well.
The probability density function is:
$$Q(x) = |\psi(x)|^2 = \frac{1}{L} \exp\left(-\frac{2|x - p|}{L}\right)$$

By Monte Carlo inversion sampling with $u \sim \mathcal{U}(0, 1)$:
$$X_{ij}(t+1) = p_{ij}(t) \pm \beta(t) \cdot |C_j(t) - X_{ij}(t)| \cdot \ln\left(\frac{1}{u}\right)$$

where $C(t) = \frac{1}{M}\sum_{i=1}^M P_i(t)$ is the **Mean Best Position (MBEST)**.

### Contraction-Expansion Parameter ($\beta$)
$$\beta(t) = \beta_{\max} - (\beta_{\max} - \beta_{\min}) \cdot \frac{t}{T_{\max}}$$
- Standard parameters: $\beta_{\max} = 1.0$, $\beta_{\min} = 0.5$
- In early iterations ($t \to 0$), $\beta \approx 1.0$, enabling broad quantum tunneling across barriers to find global basins.
- In late iterations ($t \to T_{\max}$), $\beta \approx 0.5$, concentrating particles tightly around the optimal attractor.

---

## 🎯 Fitness Function Specification

The total cost to minimize:
$$\min f(\mathbf{R}) = \alpha \cdot \hat{T}(\mathbf{R}) + \beta_w \cdot \hat{D}(\mathbf{R}) + \gamma \cdot \hat{C}(\mathbf{R}) + \delta \cdot \hat{E}(\mathbf{R}) + \lambda \sum_{k=1}^K \max(0, \text{load}_k - Q_{\max})$$

Where each term is normalized against estimated worst-case values:
- $\hat{T}(\mathbf{R}) = \frac{\sum_{k} \sum_{(u,v) \in R_k} \text{time}(u, v, t)}{T_{\text{baseline}}}$
- $\hat{D}(\mathbf{R}) = \frac{\sum_{k} \sum_{(u,v) \in R_k} \text{dist}(u, v)}{D_{\text{baseline}}}$
- $\hat{C}(\mathbf{R}) = \frac{\sum_{k} \sum_{(u,v) \in R_k} \text{congestion\_factor}(u, v)}{C_{\text{baseline}}}$
- $\hat{E}(\mathbf{R}) = \frac{\sum_{k} \text{emissions}(R_k)}{E_{\text{baseline}}}$
- Default weights: $\alpha=0.40, \beta_w=0.30, \gamma=0.20, \delta=0.10$

---

## 📊 Benchmark Harness Guidelines (M3)

1. **Fairness Mandate**: All algorithms must be fed the **exact same NetworkX graph instance**, identical depot coordinates, identical destination array, and identical capacity thresholds.
2. **Monte Carlo Repeats**: Run each algorithm for 10 independent trials with distinct random seeds; record mean, standard deviation, best fitness, and wall-clock execution time.
3. **Early Stopping**: If $\Delta f_{\text{best}} < 10^{-4}$ for 20 consecutive iterations, trigger early termination to save compute.
