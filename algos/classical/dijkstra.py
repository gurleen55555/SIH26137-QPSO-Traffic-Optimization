"""
Dijkstra baseline — single-vehicle exact shortest path with nearest-neighbor
greedy multi-stop and round-robin vehicle assignment.

Not a VRP solver per se — it's the simplest possible baseline.
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


class DijkstraSolver:
    """Nearest-neighbor heuristic using Dijkstra shortest paths.

    For multi-vehicle: assigns stops greedily to vehicles round-robin,
    ordering each vehicle's stops by nearest-neighbor from the depot.
    """

    def __init__(
        self,
        weights: FitnessWeights = DEFAULT_WEIGHTS,
        callback: Optional[Callable] = None,
    ):
        self.weights = weights
        self.callback = callback

    def solve(self, vrp: VRPInstance) -> OptimizationResult:
        t_start = time.perf_counter()
        N = vrp.num_destinations
        K = vrp.num_vehicles

        # Nearest-neighbor tour from depot through all destinations
        visited = set()
        tour: List[int] = []
        current = 0  # depot index

        for _ in range(N):
            best_next = -1
            best_dist = np.inf
            for j in range(1, N + 1):
                if j not in visited and vrp.distance_matrix[current, j] < best_dist:
                    best_dist = vrp.distance_matrix[current, j]
                    best_next = j
            if best_next == -1:
                # Add remaining unvisited
                remaining = [j for j in range(1, N + 1) if j not in visited]
                tour.extend(remaining)
                break
            visited.add(best_next)
            tour.append(best_next)
            current = best_next

        # Split tour into K routes respecting capacity
        routes: List[List[int]] = []
        current_route: List[int] = []
        current_load = 0.0

        for dest_idx in tour:
            demand = vrp.demands[dest_idx - 1]
            if current_load + demand > vrp.vehicle_capacity and current_route:
                routes.append(current_route)
                current_route = []
                current_load = 0.0
            current_route.append(dest_idx)
            current_load += demand

        if current_route:
            routes.append(current_route)

        while len(routes) < K:
            routes.append([])
        while len(routes) > K:
            routes.sort(key=len)
            smallest = routes.pop(0)
            routes[0] = smallest + routes[0]

        fitness = evaluate_fitness(routes, vrp, self.weights)
        elapsed = time.perf_counter() - t_start

        record = {"iteration": 0, "best_fitness": fitness, "mean_fitness": fitness}
        if self.callback:
            self.callback(record)

        return OptimizationResult(
            algorithm="Dijkstra",
            best_fitness=fitness,
            best_routes=routes,
            convergence_history=[record],
            execution_time_s=elapsed,
            total_iterations=1,
        )
