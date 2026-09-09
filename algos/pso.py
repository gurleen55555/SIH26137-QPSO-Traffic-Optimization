"""
Classical Velocity-Position PSO — inertia weight model.

Used as a fair baseline to benchmark against QPSO.  Same interface, same
VRP instance, same fitness function, same SPV decode.
"""

from __future__ import annotations

import time
from typing import Callable, Dict, List, Optional

import numpy as np

from algos.vrp_formulator import (
    VRPInstance,
    FitnessWeights,
    DEFAULT_WEIGHTS,
    decode_permutation,
    evaluate_fitness,
)
from algos.qpso import OptimizationResult


class PSOSolver:
    """Standard Particle Swarm Optimization with inertia weight.

    Parameters
    ----------
    swarm_size : int
        Number of particles.
    max_iterations : int
        Iteration limit.
    w : float
        Inertia weight (default 0.729, Clerc constriction).
    c1 : float
        Cognitive coefficient.
    c2 : float
        Social coefficient.
    weights : FitnessWeights
        Multi-objective fitness weights.
    seed : int | None
        Random seed.
    callback : callable | None
        Per-iteration callback.
    """

    def __init__(
        self,
        swarm_size: int = 30,
        max_iterations: int = 150,
        w: float = 0.729,
        c1: float = 1.494,
        c2: float = 1.494,
        weights: FitnessWeights = DEFAULT_WEIGHTS,
        early_stop_patience: int = 20,
        early_stop_delta: float = 1e-3,
        seed: Optional[int] = None,
        callback: Optional[Callable] = None,
    ):
        self.M = swarm_size
        self.T_max = max_iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.weights = weights
        self.patience = early_stop_patience
        self.delta = early_stop_delta
        self.seed = seed
        self.callback = callback

    def solve(self, vrp: VRPInstance) -> OptimizationResult:
        rng = np.random.default_rng(self.seed)
        N = vrp.num_destinations
        M = self.M
        t_start = time.perf_counter()

        # Initialize
        X = rng.random((M, N))
        V = rng.uniform(-0.5, 0.5, (M, N))  # velocity vectors
        pbest = X.copy()
        pbest_fitness = np.full(M, np.inf)

        gbest = np.zeros(N)
        gbest_fitness = np.inf
        gbest_routes: List[List[int]] = []

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

        for t in range(self.T_max):
            fitness_values = np.empty(M)

            for i in range(M):
                r1 = rng.random(N)
                r2 = rng.random(N)

                # Velocity update: v = w*v + c1*r1*(pbest - x) + c2*r2*(gbest - x)
                V[i] = (
                    self.w * V[i]
                    + self.c1 * r1 * (pbest[i] - X[i])
                    + self.c2 * r2 * (gbest - X[i])
                )

                # Position update: x = x + v
                X[i] = X[i] + V[i]

                # Decode & evaluate
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

            mean_fit = float(np.mean(fitness_values))
            record = {
                "iteration": t,
                "best_fitness": gbest_fitness,
                "mean_fitness": mean_fit,
            }
            convergence.append(record)
            if self.callback:
                self.callback(record)

            if abs(prev_best - gbest_fitness) < self.delta:
                no_improve_count += 1
            else:
                no_improve_count = 0
            prev_best = gbest_fitness

            if no_improve_count >= self.patience:
                break

        elapsed = time.perf_counter() - t_start

        return OptimizationResult(
            algorithm="PSO",
            best_fitness=gbest_fitness,
            best_routes=gbest_routes,
            convergence_history=convergence,
            execution_time_s=elapsed,
            total_iterations=len(convergence),
        )
