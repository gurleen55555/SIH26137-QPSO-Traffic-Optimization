"""
POST /api/v1/benchmark — Run all algorithms on the same VRP instance.
"""

from __future__ import annotations

from typing import List, Optional

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.state import app_state
from algos.vrp_formulator import build_vrp_from_graph
from algos.convergence_analyzer import ConvergenceAnalyzer
from data.osm_loader import get_random_depot_and_destinations

router = APIRouter()


class BenchmarkRequest(BaseModel):
    algorithms: List[str] = ["QPSO", "PSO", "GA", "ACO", "Dijkstra", "A*"]
    num_destinations: int = Field(default=10, ge=3, le=50)
    num_vehicles: int = Field(default=3, ge=1, le=10)
    vehicle_capacity: float = Field(default=100.0, gt=0)
    seed: Optional[int] = 42


class BenchmarkResponse(BaseModel):
    status: str
    summary: List[dict]
    convergence: dict  # {algorithm_name: [convergence_records]}


@router.post("/benchmark", response_model=BenchmarkResponse)
async def run_benchmark(req: BenchmarkRequest):
    """Run all algorithms on the same VRP instance for fair comparison."""
    G = app_state.get("graph")
    if G is None:
        raise HTTPException(status_code=503, detail="Graph not loaded")

    depot, destinations = get_random_depot_and_destinations(
        G, num_destinations=req.num_destinations, seed=req.seed or 42,
    )

    rng = np.random.default_rng(req.seed or 42)
    demands = rng.uniform(5, 25, len(destinations)).tolist()

    vrp = build_vrp_from_graph(
        G, depot, destinations, demands,
        num_vehicles=req.num_vehicles,
        vehicle_capacity=req.vehicle_capacity,
    )

    analyzer = ConvergenceAnalyzer(algorithms=req.algorithms, seed=req.seed)
    benchmark = analyzer.run(vrp)

    # Collect convergence histories
    conv = {}
    for name, result in benchmark.results.items():
        conv[name] = result.convergence_history

    return BenchmarkResponse(
        status="success",
        summary=benchmark.summary,
        convergence=conv,
    )
