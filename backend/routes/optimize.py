"""
POST /api/v1/optimize — Run a single algorithm on a VRP instance.
"""

from __future__ import annotations

from typing import List, Optional

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.state import app_state
from algos.vrp_formulator import build_vrp_from_graph, route_total_distance, route_total_time
from algos.qpso import QPSOSolver
from algos.pso import PSOSolver
from algos.classical.dijkstra import DijkstraSolver
from algos.classical.astar import AStarSolver
from algos.classical.genetic_algo import GeneticAlgorithmSolver
from algos.classical.ant_colony import AntColonySolver
from data.osm_loader import get_random_depot_and_destinations

router = APIRouter()


class OptimizeRequest(BaseModel):
    depot_node_id: Optional[int] = None
    destination_node_ids: Optional[List[int]] = None
    num_destinations: int = Field(default=10, ge=3, le=50)
    num_vehicles: int = Field(default=3, ge=1, le=10)
    vehicle_capacity: float = Field(default=100.0, gt=0)
    demands: Optional[List[float]] = None
    algorithm: str = Field(default="QPSO", pattern="^(QPSO|PSO|GA|ACO|Dijkstra|A\\*)$")
    max_iterations: int = Field(default=150, ge=10, le=500)
    swarm_size: int = Field(default=30, ge=5, le=100)
    seed: Optional[int] = None


class VehicleRoute(BaseModel):
    vehicle_id: int
    route_node_ids: List[int]
    route_distance_m: float
    route_time_s: float
    assigned_load: float


class OptimizeResponse(BaseModel):
    status: str
    algorithm: str
    best_fitness: float
    execution_time_s: float
    total_iterations: int
    vehicles: List[VehicleRoute]
    convergence_history: List[dict]


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize(req: OptimizeRequest):
    """Solve VRP using the chosen algorithm."""
    G = app_state.get("graph")
    if G is None:
        raise HTTPException(status_code=503, detail="Graph not loaded")

    # Determine depot & destinations
    if req.depot_node_id is not None and req.destination_node_ids is not None:
        depot = req.depot_node_id
        destinations = req.destination_node_ids
    else:
        depot, destinations = get_random_depot_and_destinations(
            G, num_destinations=req.num_destinations, seed=req.seed or 42,
        )

    N = len(destinations)

    # Demands
    if req.demands and len(req.demands) == N:
        demands = req.demands
    else:
        rng = np.random.default_rng(req.seed or 42)
        demands = rng.uniform(5, 25, N).tolist()

    # Build VRP
    vrp = build_vrp_from_graph(
        G, depot, destinations, demands,
        num_vehicles=req.num_vehicles,
        vehicle_capacity=req.vehicle_capacity,
    )

    # Select solver
    solver = _make_solver(req)
    result = solver.solve(vrp)

    # Build vehicle response
    vehicles = []
    for i, route in enumerate(result.best_routes):
        if route:
            full = [0] + route + [0]
            rd = sum(
                vrp.distance_matrix[full[k], full[k + 1]]
                for k in range(len(full) - 1)
                if not np.isinf(vrp.distance_matrix[full[k], full[k + 1]])
            )
            rt = sum(
                vrp.time_matrix[full[k], full[k + 1]]
                for k in range(len(full) - 1)
                if not np.isinf(vrp.time_matrix[full[k], full[k + 1]])
            )
            load = sum(vrp.demands[d - 1] for d in route)
            node_ids = [vrp.node_id_map[d] for d in route]
        else:
            rd, rt, load, node_ids = 0.0, 0.0, 0.0, []

        vehicles.append(VehicleRoute(
            vehicle_id=i + 1,
            route_node_ids=node_ids,
            route_distance_m=round(rd, 2),
            route_time_s=round(rt, 2),
            assigned_load=round(load, 2),
        ))

    return OptimizeResponse(
        status="success",
        algorithm=result.algorithm,
        best_fitness=round(result.best_fitness, 4),
        execution_time_s=round(result.execution_time_s, 4),
        total_iterations=result.total_iterations,
        vehicles=vehicles,
        convergence_history=result.convergence_history,
    )


def _make_solver(req: OptimizeRequest):
    if req.algorithm == "QPSO":
        return QPSOSolver(swarm_size=req.swarm_size, max_iterations=req.max_iterations, seed=req.seed)
    elif req.algorithm == "PSO":
        return PSOSolver(swarm_size=req.swarm_size, max_iterations=req.max_iterations, seed=req.seed)
    elif req.algorithm == "GA":
        return GeneticAlgorithmSolver(generations=req.max_iterations, seed=req.seed)
    elif req.algorithm == "ACO":
        return AntColonySolver(iterations=req.max_iterations, seed=req.seed)
    elif req.algorithm == "Dijkstra":
        return DijkstraSolver()
    elif req.algorithm == "A*":
        return AStarSolver()
    raise HTTPException(status_code=400, detail=f"Unknown algorithm: {req.algorithm}")
