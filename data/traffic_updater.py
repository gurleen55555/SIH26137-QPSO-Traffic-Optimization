"""
Traffic Updater — applies synthetic traffic patterns and incident injection
onto a NetworkX city graph's edge weights.

The synthetic model is the primary/critical-path traffic generator.
External APIs (HERE/TomTom) and SUMO are optional enrichments only.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional, Tuple

import networkx as nx
import numpy as np


class TrafficScenario(str, Enum):
    """Pre-defined traffic scenarios for demo."""
    NORMAL = "normal"
    MORNING_RUSH = "morning_rush"
    EVENING_RUSH = "evening_rush"
    HEAVY_CONGESTION = "heavy_congestion"
    ACCIDENT = "accident"
    ROAD_CLOSURE = "road_closure"


# Rush-hour multipliers: how much slower traffic moves
_SCENARIO_MULTIPLIERS = {
    TrafficScenario.NORMAL:           {"mean": 1.0, "std": 0.1},
    TrafficScenario.MORNING_RUSH:     {"mean": 1.8, "std": 0.3},
    TrafficScenario.EVENING_RUSH:     {"mean": 2.1, "std": 0.4},
    TrafficScenario.HEAVY_CONGESTION: {"mean": 3.0, "std": 0.5},
}


def apply_synthetic_traffic(
    G: nx.DiGraph,
    scenario: TrafficScenario = TrafficScenario.NORMAL,
    seed: Optional[int] = None,
    arterial_fraction: float = 0.3,
) -> nx.DiGraph:
    """Apply Gaussian-noise traffic perturbation to all edge weights.

    Modifies edge attributes in-place:
      - `travel_time` is scaled by a stochastic congestion factor.
      - `congestion` ∈ [0, 1] is set based on the delay ratio.
      - `speed_kph` is adjusted inversely.

    Parameters
    ----------
    G : nx.DiGraph
        City road graph (must have 'length', 'travel_time', 'speed_kph').
    scenario : TrafficScenario
        Which traffic pattern to simulate.
    seed : int | None
        Random seed for reproducibility.
    arterial_fraction : float
        Fraction of edges treated as arterial roads (get heavier traffic).

    Returns
    -------
    nx.DiGraph
        The same graph object (modified in-place).
    """
    rng = np.random.default_rng(seed)
    params = _SCENARIO_MULTIPLIERS.get(scenario, _SCENARIO_MULTIPLIERS[TrafficScenario.NORMAL])

    edges = list(G.edges(data=True))
    n_arterial = int(len(edges) * arterial_fraction)

    # Randomly designate some edges as "arterial" (higher traffic impact)
    arterial_idxs = set(rng.choice(len(edges), size=n_arterial, replace=False))

    for idx, (u, v, data) in enumerate(edges):
        base_time = data.get("travel_time", data.get("length", 100.0) / 13.89)
        base_speed = data.get("speed_kph", 50.0)

        # Arterial roads get the full scenario multiplier; local roads get less
        if idx in arterial_idxs:
            multiplier = max(0.5, rng.normal(params["mean"], params["std"]))
        else:
            # Local roads: dampened effect
            multiplier = max(0.5, rng.normal(
                1.0 + (params["mean"] - 1.0) * 0.4,
                params["std"] * 0.5,
            ))

        new_time = base_time * multiplier
        congestion = min(1.0, max(0.0, (multiplier - 1.0) / 2.0))  # normalize to [0, 1]
        new_speed = max(5.0, base_speed / multiplier)

        G[u][v]["travel_time"] = new_time
        G[u][v]["congestion"] = congestion
        G[u][v]["speed_kph"] = new_speed

    return G


def inject_incident(
    G: nx.DiGraph,
    edge: Tuple[int, int],
    severity: str = "closure",
) -> nx.DiGraph:
    """Inject a traffic incident on a specific edge.

    Parameters
    ----------
    G : nx.DiGraph
    edge : (u, v)
        The edge to affect.
    severity : str
        'closure' — sets travel time to near-infinity (road blocked).
        'accident' — 5x travel time increase.
        'slowdown' — 2x travel time increase.

    Returns
    -------
    nx.DiGraph
    """
    u, v = edge
    if not G.has_edge(u, v):
        return G

    if severity == "closure":
        G[u][v]["travel_time"] = 1e7
        G[u][v]["congestion"] = 1.0
        G[u][v]["speed_kph"] = 0.1
    elif severity == "accident":
        G[u][v]["travel_time"] = G[u][v].get("travel_time", 100.0) * 5.0
        G[u][v]["congestion"] = 0.9
        G[u][v]["speed_kph"] = max(2.0, G[u][v].get("speed_kph", 50.0) / 5.0)
    elif severity == "slowdown":
        G[u][v]["travel_time"] = G[u][v].get("travel_time", 100.0) * 2.0
        G[u][v]["congestion"] = 0.5
        G[u][v]["speed_kph"] = max(10.0, G[u][v].get("speed_kph", 50.0) / 2.0)

    return G


def clear_incidents(G: nx.DiGraph) -> nx.DiGraph:
    """Reset all congestion attributes to baseline (normal scenario)."""
    for u, v, data in G.edges(data=True):
        length = data.get("length", 500.0)
        speed = data.get("speed_kph", 50.0)
        data["travel_time"] = (length / 1000.0) / (speed / 3600.0)
        data["congestion"] = 0.0
    return G
