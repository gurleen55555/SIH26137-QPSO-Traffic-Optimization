"""
Convergence Analyzer — runs all algorithms on an identical VRP instance
and collects comparative benchmark statistics.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

import numpy as np

from algos.vrp_formulator import (
    VRPInstance,
    FitnessWeights,
    DEFAULT_WEIGHTS,
    route_total_distance,
    route_total_time,
)
from algos.qpso import QPSOSolver, OptimizationResult
from algos.pso import PSOSolver
from algos.classical.dijkstra import DijkstraSolver
from algos.classical.astar import AStarSolver
from algos.classical.genetic_algo import GeneticAlgorithmSolver
from algos.classical.ant_colony import AntColonySolver


@dataclass
class BenchmarkResult:
    """Aggregated benchmark comparison across all algorithms."""
    results: Dict[str, OptimizationResult]
    summary: List[Dict]  # [{algorithm, best_fitness, runtime_s, iterations, ...}]


class ConvergenceAnalyzer:
    """Runs QPSO and all baselines on the same VRP instance for fair comparison.

    Parameters
    ----------
    algorithms : list[str] | None
        Which algorithms to run.  Default: all five.
    weights : FitnessWeights
    seed : int | None
        Base random seed (each algorithm gets seed + offset for independence).
    callback : callable | None
        Called with (algorithm_name, iteration_record) for streaming.
    """

    ALL_ALGORITHMS = ["QPSO", "PSO", "GA", "ACO", "Dijkstra", "A*"]

    def __init__(
        self,
        algorithms: Optional[List[str]] = None,
        weights: FitnessWeights = DEFAULT_WEIGHTS,
        seed: Optional[int] = None,
        callback: Optional[Callable] = None,
    ):
        self.algorithms = algorithms or self.ALL_ALGORITHMS
        self.weights = weights
        self.seed = seed
        self.callback = callback

    def run(self, vrp: VRPInstance) -> BenchmarkResult:
        """Execute all requested algorithms on the same VRP instance.

        Returns
        -------
        BenchmarkResult
        """
        results: Dict[str, OptimizationResult] = {}

        for algo_name in self.algorithms:
            solver = self._make_solver(algo_name)
            result = solver.solve(vrp)
            results[algo_name] = result

        # Build summary table
        summary = []
        for name, res in results.items():
            entry = {
                "algorithm": name,
                "best_fitness": res.best_fitness,
                "runtime_s": res.execution_time_s,
                "iterations": res.total_iterations,
                "total_distance_m": route_total_distance(res.best_routes, vrp),
                "total_time_s": route_total_time(res.best_routes, vrp),
                "num_routes": len([r for r in res.best_routes if r]),
            }
            summary.append(entry)

        return BenchmarkResult(results=results, summary=summary)

    def _make_solver(self, algo_name: str):
        """Instantiate the solver for the given algorithm name."""
        base_seed = self.seed

        def _cb(record):
            if self.callback:
                self.callback(algo_name, record)

        if algo_name == "QPSO":
            return QPSOSolver(
                swarm_size=30, max_iterations=150,
                weights=self.weights,
                seed=base_seed,
                callback=_cb,
            )
        elif algo_name == "PSO":
            return PSOSolver(
                swarm_size=30, max_iterations=150,
                weights=self.weights,
                seed=(base_seed + 1) if base_seed else None,
                callback=_cb,
            )
        elif algo_name == "GA":
            return GeneticAlgorithmSolver(
                population_size=50, generations=150,
                weights=self.weights,
                seed=(base_seed + 2) if base_seed else None,
                callback=_cb,
            )
        elif algo_name == "ACO":
            return AntColonySolver(
                num_ants=25, iterations=100,
                weights=self.weights,
                seed=(base_seed + 3) if base_seed else None,
                callback=_cb,
            )
        elif algo_name == "Dijkstra":
            return DijkstraSolver(weights=self.weights, callback=_cb)
        elif algo_name == "A*":
            return AStarSolver(weights=self.weights, callback=_cb)
        else:
            raise ValueError(f"Unknown algorithm: {algo_name}")
