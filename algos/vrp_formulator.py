"""
VRP Formulator — encodes a NetworkX city graph into a Vehicle Routing Problem
instance suitable for all optimizers (QPSO, PSO, GA, ACO, Dijkstra/A*).

Key responsibilities:
  1. Build shortest-path distance & time matrices from a graph.
  2. Decode continuous particle positions → discrete VRP routes (SPV rule).
  3. Evaluate the multi-objective fitness function with capacity penalties.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import networkx as nx
import numpy as np


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class VRPInstance:
    """Immutable snapshot of a multi-vehicle VRP problem instance.

    All matrices are square (N+1)×(N+1) where index 0 = depot and
    indices 1..N = delivery destinations.
    """
    depot: int                          # original graph node ID for the depot
    destinations: List[int]             # original graph node IDs for delivery stops
    demands: np.ndarray                 # shape (N,), demand at each destination
    vehicle_capacity: float             # max load per vehicle (Q_max)
    num_vehicles: int                   # K — fleet size
    distance_matrix: np.ndarray         # (N+1) × (N+1) shortest-path distances (m)
    time_matrix: np.ndarray             # (N+1) × (N+1) estimated travel times (s)
    congestion_matrix: np.ndarray       # (N+1) × (N+1) congestion factors [0, 1]
    node_id_map: List[int] = field(default_factory=list)  # index → original node ID
    graph: Optional[nx.DiGraph] = None  # reference to the source graph (for path recovery)

    @property
    def num_destinations(self) -> int:
        return len(self.destinations)


# ---------------------------------------------------------------------------
# Build VRP from a NetworkX Graph
# ---------------------------------------------------------------------------

def build_vrp_from_graph(
    G: nx.DiGraph,
    depot: int,
    destinations: List[int],
    demands: Optional[List[float]] = None,
    num_vehicles: int = 3,
    vehicle_capacity: float = 100.0,
) -> VRPInstance:
    """Construct a VRPInstance from a weighted city graph.

    Parameters
    ----------
    G : nx.DiGraph
        Road network.  Edges must have 'length' (meters) and 'travel_time' (seconds).
        An optional 'congestion' attribute ∈ [0, 1] is used if present.
    depot : int
        Node ID of the shared depot.
    destinations : list[int]
        Node IDs of the N delivery stops.
    demands : list[float] | None
        Demand at each destination. If None, uniform demand of 10 is assigned.
    num_vehicles : int
        Number of vehicles K (must be ≥ 1).
    vehicle_capacity : float
        Maximum load per vehicle Q_max.

    Returns
    -------
    VRPInstance
    """
    N = len(destinations)
    if demands is None:
        demands = np.full(N, 10.0)
    else:
        demands = np.asarray(demands, dtype=np.float64)

    # Ordered list: index 0 = depot, 1..N = destinations
    nodes = [depot] + list(destinations)

    # Pre-compute all-pairs shortest paths for the subset of interest
    dist_mat = np.full((N + 1, N + 1), np.inf)
    time_mat = np.full((N + 1, N + 1), np.inf)
    cong_mat = np.zeros((N + 1, N + 1))

    for i, src in enumerate(nodes):
        for j, tgt in enumerate(nodes):
            if i == j:
                dist_mat[i, j] = 0.0
                time_mat[i, j] = 0.0
                continue
            try:
                path = nx.shortest_path(G, src, tgt, weight="length")
                d = sum(
                    G[path[k]][path[k + 1]].get("length", 1.0)
                    for k in range(len(path) - 1)
                )
                t = sum(
                    G[path[k]][path[k + 1]].get("travel_time", d / 13.89)  # fallback 50 km/h
                    for k in range(len(path) - 1)
                )
                c = np.mean([
                    G[path[k]][path[k + 1]].get("congestion", 0.0)
                    for k in range(len(path) - 1)
                ]) if len(path) > 1 else 0.0
                dist_mat[i, j] = d
                time_mat[i, j] = t
                cong_mat[i, j] = c
            except nx.NetworkXNoPath:
                pass  # leave as inf — route validator will catch this

    return VRPInstance(
        depot=depot,
        destinations=destinations,
        demands=demands,
        vehicle_capacity=vehicle_capacity,
        num_vehicles=num_vehicles,
        distance_matrix=dist_mat,
        time_matrix=time_mat,
        congestion_matrix=cong_mat,
        node_id_map=nodes,
        graph=G,
    )


# ---------------------------------------------------------------------------
# SPV Decode: Continuous → Discrete Permutation → Route Assignment
# ---------------------------------------------------------------------------

def decode_permutation(
    continuous_vector: np.ndarray,
    vrp: VRPInstance,
) -> List[List[int]]:
    """Decode a continuous particle position into K vehicle routes using the
    Smallest Position Value (SPV) rule with capacity-based route splitting.

    Parameters
    ----------
    continuous_vector : np.ndarray, shape (N,)
        Continuous position of one particle (one float per destination).
    vrp : VRPInstance
        The problem instance.

    Returns
    -------
    list[list[int]]
        K routes.  Each route is an ordered list of destination *indices*
        (1-based into the node_id_map, i.e. 1..N).
        The depot (index 0) is NOT included — callers must prepend/append it.
    """
    N = vrp.num_destinations
    K = vrp.num_vehicles

    # SPV: sort destination indices by their continuous values
    perm = np.argsort(continuous_vector[:N]).tolist()  # permutation of 0..N-1
    perm = [p + 1 for p in perm]  # shift to 1-based (0 = depot)

    # Split the permutation into K routes respecting capacity
    routes: List[List[int]] = []
    current_route: List[int] = []
    current_load = 0.0

    for dest_idx in perm:
        demand = vrp.demands[dest_idx - 1]  # demands is 0-based for destinations
        if current_load + demand > vrp.vehicle_capacity and current_route:
            routes.append(current_route)
            current_route = []
            current_load = 0.0
        current_route.append(dest_idx)
        current_load += demand

    if current_route:
        routes.append(current_route)

    # Pad or merge to exactly K routes
    while len(routes) < K:
        routes.append([])
    while len(routes) > K:
        # Merge the smallest route into the least loaded route
        routes.sort(key=len)
        smallest = routes.pop(0)
        routes[0] = smallest + routes[0]

    return routes


# ---------------------------------------------------------------------------
# Multi-Objective Fitness Evaluation
# ---------------------------------------------------------------------------

@dataclass
class FitnessWeights:
    """Weights for the multi-objective cost function."""
    alpha_time: float = 0.40
    beta_distance: float = 0.30
    gamma_congestion: float = 0.20
    delta_emissions: float = 0.10
    capacity_penalty: float = 1000.0  # λ — large penalty for overloading


DEFAULT_WEIGHTS = FitnessWeights()


def evaluate_fitness(
    routes: List[List[int]],
    vrp: VRPInstance,
    weights: FitnessWeights = DEFAULT_WEIGHTS,
) -> float:
    """Compute the penalized multi-objective fitness for a set of K routes.

    Lower is better.

    Parameters
    ----------
    routes : list[list[int]]
        K routes, each a list of destination indices (1-based).
    vrp : VRPInstance
    weights : FitnessWeights

    Returns
    -------
    float
        Total cost (fitness).  Lower is better.
    """
    total_distance = 0.0
    total_time = 0.0
    total_congestion = 0.0
    total_penalty = 0.0

    for route in routes:
        if not route:
            continue

        # Depot → first stop → ... → last stop → depot
        full_route = [0] + route + [0]
        route_load = sum(vrp.demands[d - 1] for d in route)

        for k in range(len(full_route) - 1):
            i, j = full_route[k], full_route[k + 1]
            d = vrp.distance_matrix[i, j]
            t = vrp.time_matrix[i, j]
            c = vrp.congestion_matrix[i, j]

            if np.isinf(d):
                # Infeasible edge — heavy penalty
                total_distance += 1e6
                total_time += 1e6
            else:
                total_distance += d
                total_time += t
                total_congestion += c

        # Capacity violation penalty
        violation = max(0.0, route_load - vrp.vehicle_capacity)
        total_penalty += violation

    # Normalize each term against a baseline (use raw sums — normalization is
    # implicit when comparing same-instance solutions).  For cross-instance
    # comparisons, divide by worst-case; within a single optimization run the
    # relative ranking is unaffected.
    # Simple emission proxy: 0.12 kg CO₂ per meter (avg urban truck)
    total_emissions = total_distance * 0.00012  # kg CO₂

    fitness = (
        weights.alpha_time * total_time
        + weights.beta_distance * total_distance
        + weights.gamma_congestion * total_congestion
        + weights.delta_emissions * total_emissions
        + weights.capacity_penalty * total_penalty
    )

    return fitness


def route_total_distance(routes: List[List[int]], vrp: VRPInstance) -> float:
    """Sum of edge distances across all vehicle routes (meters)."""
    total = 0.0
    for route in routes:
        full = [0] + route + [0]
        for k in range(len(full) - 1):
            d = vrp.distance_matrix[full[k], full[k + 1]]
            total += d if not np.isinf(d) else 0.0
    return total


def route_total_time(routes: List[List[int]], vrp: VRPInstance) -> float:
    """Sum of edge travel times across all vehicle routes (seconds)."""
    total = 0.0
    for route in routes:
        full = [0] + route + [0]
        for k in range(len(full) - 1):
            t = vrp.time_matrix[full[k], full[k + 1]]
            total += t if not np.isinf(t) else 0.0
    return total
