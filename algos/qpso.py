"""
QPSO — Quantum-Inspired Particle Swarm Optimization for Multi-Vehicle VRP.

Implements the authentic Delta Potential Well model (Sun et al., 2004):
  • Mean Best Position (MBEST)
  • Quantum position update with ln(1/u) sampling
  • Contraction-Expansion β(t) linear decay

This is NOT a renamed classical PSO.  The velocity vector is entirely absent;
particles are updated via quantum wave function collapse sampling.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np

from algos.vrp_formulator import (
    VRPInstance,
    FitnessWeights,
    DEFAULT_WEIGHTS,
    decode_permutation,
    evaluate_fitness,
)


@dataclass
class OptimizationResult:
    """Result container returned by any solver."""
    algorithm: str
    best_fitness: float
    best_routes: List[List[int]]
    convergence_history: List[Dict]  # [{iteration, best_fitness, mean_fitness}, ...]
    execution_time_s: float
    total_iterations: int


class QPSOSolver:
    """Quantum-Inspired Particle Swarm Optimization solver for CVRP.

    Each particle X_i ∈ ℝ^N represents continuous positions that are decoded
    to a discrete VRP route assignment via the Smallest Position Value (SPV) rule.

    Parameters
    ----------
    swarm_size : int
        Number of particles M in the swarm.
    max_iterations : int
        Maximum number of iterations T_max.
    beta_max : float
        Starting value of the contraction-expansion coefficient.
    beta_min : float
        Ending value of β at t = T_max.
    weights : FitnessWeights
        Multi-objective cost function weights.
    early_stop_patience : int
        Stop if best fitness does not improve by `early_stop_delta` for this
        many consecutive iterations.
    early_stop_delta : float
        Minimum improvement in best fitness to reset the patience counter.
    seed : int | None
        Random seed for reproducibility.
    callback : callable | None
        Called every iteration with (iteration, best_fitness, mean_fitness).
        Useful for WebSocket streaming.
    """

    def __init__(
        self,
        swarm_size: int = 30,
        max_iterations: int = 150,
        beta_max: float = 1.0,
        beta_min: float = 0.5,
        weights: FitnessWeights = DEFAULT_WEIGHTS,
        early_stop_patience: int = 20,
        early_stop_delta: float = 1e-3,
        seed: Optional[int] = None,
        callback: Optional[Callable] = None,
    ):
        self.M = swarm_size
        self.T_max = max_iterations
        self.beta_max = beta_max
        self.beta_min = beta_min
        self.weights = weights
        self.patience = early_stop_patience
        self.delta = early_stop_delta
        self.seed = seed
        self.callback = callback

    def solve(self, vrp: VRPInstance) -> OptimizationResult:
        """Run QPSO on the given VRP instance.

        Returns
        -------
        OptimizationResult
        """
        rng = np.random.default_rng(self.seed)
        N = vrp.num_destinations
        M = self.M
        t_start = time.perf_counter()

        # ------------------------------------------------------------------
        # 1. Initialize swarm — uniform random positions in [0, 1)^N
        # ------------------------------------------------------------------
        X = rng.random((M, N))  # particle positions
        pbest = X.copy()        # personal best positions
        pbest_fitness = np.full(M, np.inf)

        gbest = np.zeros(N)
        gbest_fitness = np.inf
        gbest_routes: List[List[int]] = []

        # Evaluate initial fitness
        for i in range(M):
            routes = decode_permutation(X[i], vrp)
            f = evaluate_fitness(routes, vrp, self.weights)
            pbest_fitness[i] = f
            if f < gbest_fitness:
                gbest_fitness = f
                gbest = X[i].copy()
                gbest_routes = routes

        convergence: List[Dict] = []
        no_improve_count = 0
        prev_best = gbest_fitness

        # ------------------------------------------------------------------
        # 2. Main QPSO loop
        # ------------------------------------------------------------------
        for t in range(self.T_max):
            # β decay: linear from beta_max → beta_min
            beta = self.beta_max - (self.beta_max - self.beta_min) * t / self.T_max

            # ---------------------------------------------------------------
            # 2a. Compute Mean Best Position (MBEST) — centroid of all pbest
            # ---------------------------------------------------------------
            mbest = np.mean(pbest, axis=0)  # shape (N,)

            fitness_values = np.empty(M)

            for i in range(M):
                # -----------------------------------------------------------
                # 2b. Local attractor point
                #     p_i = φ·pbest_i + (1−φ)·gbest,  φ ~ U(0,1) per dim
                # -----------------------------------------------------------
                phi = rng.random(N)
                p = phi * pbest[i] + (1.0 - phi) * gbest

                # -----------------------------------------------------------
                # 2c. Quantum position update (Delta potential well sampling)
                #     X_new = p ± β·|MBEST − X|·ln(1/u),  u ~ U(0,1)
                #     sign chosen randomly with prob 0.5
                # -----------------------------------------------------------
                u = rng.random(N)
                u = np.clip(u, 1e-12, 1.0)  # avoid log(0)

                sign = np.where(rng.random(N) < 0.5, 1.0, -1.0)

                X[i] = p + sign * beta * np.abs(mbest - X[i]) * np.log(1.0 / u)

                # -----------------------------------------------------------
                # 2d. Decode, evaluate, update pbest & gbest
                # -----------------------------------------------------------
                routes = decode_permutation(X[i], vrp)
                f = evaluate_fitness(routes, vrp, self.weights)
                fitness_values[i] = f

                if f < pbest_fitness[i]:
                    pbest[i] = X[i].copy()
                    pbest_fitness[i] = f

                if f < gbest_fitness:
                    gbest_fitness = f
                    gbest = X[i].copy()
                    gbest_routes = routes

            # ---------------------------------------------------------------
            # 2e. Record convergence & early stopping
            # ---------------------------------------------------------------
            mean_fit = float(np.mean(fitness_values))
            record = {
                "iteration": t,
                "best_fitness": gbest_fitness,
                "mean_fitness": mean_fit,
            }
            convergence.append(record)

            if self.callback:
                self.callback(record)

            # Early stopping check
            if abs(prev_best - gbest_fitness) < self.delta:
                no_improve_count += 1
            else:
                no_improve_count = 0
            prev_best = gbest_fitness

            if no_improve_count >= self.patience:
                break

        elapsed = time.perf_counter() - t_start

        return OptimizationResult(
            algorithm="QPSO",
            best_fitness=gbest_fitness,
            best_routes=gbest_routes,
            convergence_history=convergence,
            execution_time_s=elapsed,
            total_iterations=len(convergence),
        )
