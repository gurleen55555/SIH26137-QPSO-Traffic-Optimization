"""
Genetic Algorithm for Multi-Vehicle VRP.

Permutation-based GA with:
  - Order Crossover (OX)
  - Swap mutation
  - Roulette-wheel selection
  - Elitism (top-2 survive)
  - Capacity-split route decode (same as QPSO)
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


class GeneticAlgorithmSolver:
    """Permutation-based Genetic Algorithm for CVRP.

    Parameters
    ----------
    population_size : int
    generations : int
    crossover_rate : float
    mutation_rate : float
    elitism_count : int
    weights : FitnessWeights
    seed : int | None
    callback : callable | None
    """

    def __init__(
        self,
        population_size: int = 50,
        generations: int = 150,
        crossover_rate: float = 0.85,
        mutation_rate: float = 0.15,
        elitism_count: int = 2,
        weights: FitnessWeights = DEFAULT_WEIGHTS,
        early_stop_patience: int = 20,
        early_stop_delta: float = 1e-3,
        seed: Optional[int] = None,
        callback: Optional[Callable] = None,
    ):
        self.P = population_size
        self.G = generations
        self.cx_rate = crossover_rate
        self.mut_rate = mutation_rate
        self.elite = elitism_count
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

        # Initialize population — random permutations of 1..N (destination indices)
        pop = [rng.permutation(N) + 1 for _ in range(self.P)]
        fitness = np.array([self._eval(ind, vrp) for ind in pop])

        gbest_idx = int(np.argmin(fitness))
        gbest_fitness = fitness[gbest_idx]
        gbest_perm = pop[gbest_idx].copy()

        convergence: List[Dict] = []
        no_improve = 0
        prev_best = gbest_fitness

        for gen in range(self.G):
            # Selection + Crossover + Mutation → new population
            new_pop: List[np.ndarray] = []

            # Elitism: carry top individuals
            elite_idxs = np.argsort(fitness)[:self.elite]
            for idx in elite_idxs:
                new_pop.append(pop[idx].copy())

            while len(new_pop) < self.P:
                p1 = self._roulette(pop, fitness, rng)
                p2 = self._roulette(pop, fitness, rng)

                if rng.random() < self.cx_rate:
                    c1, c2 = self._order_crossover(p1, p2, rng)
                else:
                    c1, c2 = p1.copy(), p2.copy()

                if rng.random() < self.mut_rate:
                    self._swap_mutation(c1, rng)
                if rng.random() < self.mut_rate:
                    self._swap_mutation(c2, rng)

                new_pop.append(c1)
                if len(new_pop) < self.P:
                    new_pop.append(c2)

            pop = new_pop[:self.P]
            fitness = np.array([self._eval(ind, vrp) for ind in pop])

            gen_best_idx = int(np.argmin(fitness))
            if fitness[gen_best_idx] < gbest_fitness:
                gbest_fitness = fitness[gen_best_idx]
                gbest_perm = pop[gen_best_idx].copy()

            record = {
                "iteration": gen,
                "best_fitness": gbest_fitness,
                "mean_fitness": float(np.mean(fitness)),
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

        gbest_routes = self._decode_perm(gbest_perm, vrp)
        elapsed = time.perf_counter() - t_start

        return OptimizationResult(
            algorithm="GA",
            best_fitness=gbest_fitness,
            best_routes=gbest_routes,
            convergence_history=convergence,
            execution_time_s=elapsed,
            total_iterations=len(convergence),
        )

    # -- Helper methods -------------------------------------------------------

    def _decode_perm(self, perm: np.ndarray, vrp: VRPInstance) -> List[List[int]]:
        """Split a permutation of destination indices into K routes."""
        K = vrp.num_vehicles
        routes: List[List[int]] = []
        current: List[int] = []
        load = 0.0
        for d in perm:
            demand = vrp.demands[int(d) - 1]
            if load + demand > vrp.vehicle_capacity and current:
                routes.append(current)
                current = []
                load = 0.0
            current.append(int(d))
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

    def _eval(self, perm: np.ndarray, vrp: VRPInstance) -> float:
        routes = self._decode_perm(perm, vrp)
        return evaluate_fitness(routes, vrp, self.weights)

    @staticmethod
    def _roulette(pop, fitness, rng) -> np.ndarray:
        # Inverse fitness for minimization (lower fitness → higher selection prob)
        inv = 1.0 / (fitness + 1e-10)
        probs = inv / inv.sum()
        idx = rng.choice(len(pop), p=probs)
        return pop[idx].copy()

    @staticmethod
    def _order_crossover(p1: np.ndarray, p2: np.ndarray, rng) -> tuple:
        """Order Crossover (OX) for permutation chromosomes."""
        N = len(p1)
        a, b = sorted(rng.choice(N, 2, replace=False))

        c1 = np.full(N, -1, dtype=p1.dtype)
        c2 = np.full(N, -1, dtype=p2.dtype)
        c1[a:b + 1] = p1[a:b + 1]
        c2[a:b + 1] = p2[a:b + 1]

        def fill(child, donor, a, b):
            pos = (b + 1) % N
            for gene in np.concatenate([donor[b + 1:], donor[:b + 1]]):
                if gene not in child:
                    child[pos] = gene
                    pos = (pos + 1) % N

        fill(c1, p2, a, b)
        fill(c2, p1, a, b)
        return c1, c2

    @staticmethod
    def _swap_mutation(perm: np.ndarray, rng):
        """In-place swap of two random positions."""
        i, j = rng.choice(len(perm), 2, replace=False)
        perm[i], perm[j] = perm[j], perm[i]
