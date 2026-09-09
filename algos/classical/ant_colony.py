"""
Ant Colony Optimization (ACO) for Multi-Vehicle VRP.

Implements a simplified Ant System / Max-Min Ant System hybrid:
  - Pheromone-based probabilistic next-node selection
  - Pheromone deposit proportional to solution quality
  - Pheromone evaporation (ρ)
  - Capacity-split route assignment
"""

from __future__ import annotations

import time
from typing import Callable, Dict, List, Optional

import numpy as np

from algos.vrp_formulator import (
    VRPInstance,
    FitnessWeights,
    DEFAULT_WEIGHTS,
    evaluate_fitness,
)
from algos.qpso import OptimizationResult


class AntColonySolver:
    """ACO solver for CVRP benchmarking.

    Parameters
    ----------
    num_ants : int
    iterations : int
    alpha : float
        Pheromone importance exponent.
    beta : float
        Heuristic (inverse distance) importance exponent.
    evaporation : float
        Pheromone evaporation rate ρ ∈ (0, 1).
    q_deposit : float
        Pheromone deposit constant Q.
    weights : FitnessWeights
    seed : int | None
    callback : callable | None
    """

    def __init__(
        self,
        num_ants: int = 25,
        iterations: int = 100,
        alpha: float = 1.0,
        beta: float = 2.5,
        evaporation: float = 0.1,
        q_deposit: float = 100.0,
        weights: FitnessWeights = DEFAULT_WEIGHTS,
        early_stop_patience: int = 20,
        early_stop_delta: float = 1e-3,
        seed: Optional[int] = None,
        callback: Optional[Callable] = None,
    ):
        self.num_ants = num_ants
        self.T_max = iterations
        self.alpha = alpha
        self.beta_h = beta
        self.rho = evaporation
        self.Q = q_deposit
        self.weights = weights
        self.patience = early_stop_patience
        self.delta = early_stop_delta
        self.seed = seed
        self.callback = callback

    def solve(self, vrp: VRPInstance) -> OptimizationResult:
        rng = np.random.default_rng(self.seed)
        N = vrp.num_destinations
        K = vrp.num_vehicles
        t_start = time.perf_counter()

        # Initialize pheromone matrix τ — uniform initial deposit
        tau = np.ones((N + 1, N + 1)) * 0.1

        # Heuristic matrix η = 1 / distance (avoid div by zero)
        dist = vrp.distance_matrix.copy()
        dist[dist == 0] = 1e-10
        dist[np.isinf(dist)] = 1e10
        eta = 1.0 / dist

        gbest_fitness = np.inf
        gbest_routes: List[List[int]] = []
        convergence: List[Dict] = []
        no_improve = 0
        prev_best = gbest_fitness

        for t in range(self.T_max):
            all_tours: List[List[int]] = []
            all_fitness: List[float] = []

            for _ in range(self.num_ants):
                tour = self._construct_tour(tau, eta, N, rng)
                routes = self._split_routes(tour, vrp, K)
                f = evaluate_fitness(routes, vrp, self.weights)
                all_tours.append(tour)
                all_fitness.append(f)

                if f < gbest_fitness:
                    gbest_fitness = f
                    gbest_routes = routes

            # Pheromone evaporation
            tau *= (1.0 - self.rho)

            # Pheromone deposit — proportional to solution quality
            for tour, f in zip(all_tours, all_fitness):
                deposit = self.Q / (f + 1e-10)
                full_tour = [0] + tour + [0]
                for k in range(len(full_tour) - 1):
                    i, j = full_tour[k], full_tour[k + 1]
                    if 0 <= i <= N and 0 <= j <= N:
                        tau[i, j] += deposit

            # Clamp pheromones to prevent stagnation
            tau = np.clip(tau, 0.01, 10.0)

            mean_fit = float(np.mean(all_fitness))
            record = {
                "iteration": t,
                "best_fitness": gbest_fitness,
                "mean_fitness": mean_fit,
            }
            convergence.append(record)
            if self.callback:
                self.callback(record)

            if abs(prev_best - gbest_fitness) < self.delta:
                no_improve += 1
            else:
                no_improve = 0
            prev_best = gbest_fitness
            if no_improve >= self.patience:
                break

        elapsed = time.perf_counter() - t_start

        return OptimizationResult(
            algorithm="ACO",
            best_fitness=gbest_fitness,
            best_routes=gbest_routes,
            convergence_history=convergence,
            execution_time_s=elapsed,
            total_iterations=len(convergence),
        )

    def _construct_tour(
        self,
        tau: np.ndarray,
        eta: np.ndarray,
        N: int,
        rng: np.random.Generator,
    ) -> List[int]:
        """Construct a single ant tour visiting all N destinations from depot."""
        visited = set()
        tour: List[int] = []
        current = 0  # depot

        for _ in range(N):
            # Compute transition probabilities for unvisited nodes
            unvisited = [j for j in range(1, N + 1) if j not in visited]
            if not unvisited:
                break

            probs = np.array([
                (tau[current, j] ** self.alpha) * (eta[current, j] ** self.beta_h)
                for j in unvisited
            ])
            prob_sum = probs.sum()
            if prob_sum == 0:
                probs = np.ones(len(unvisited))
                prob_sum = len(unvisited)
            probs /= prob_sum

            chosen = rng.choice(unvisited, p=probs)
            visited.add(chosen)
            tour.append(chosen)
            current = chosen

        return tour

    @staticmethod
    def _split_routes(
        tour: List[int],
        vrp: VRPInstance,
        K: int,
    ) -> List[List[int]]:
        """Split a single ant tour into K capacity-feasible routes."""
        routes: List[List[int]] = []
        current: List[int] = []
        load = 0.0
        for d in tour:
            demand = vrp.demands[d - 1]
            if load + demand > vrp.vehicle_capacity and current:
                routes.append(current)
                current = []
                load = 0.0
            current.append(d)
            load += demand
        if current:
            routes.append(current)
        while len(routes) < K:
            routes.append([])
        while len(routes) > K:
            routes.sort(key=len)
            s = routes.pop(0)
            routes[0] = s + routes[0]
        return routes
