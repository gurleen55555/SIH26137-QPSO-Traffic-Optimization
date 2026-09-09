"""
OSM Loader — fetches, cleans, and caches city road networks.

Supports three modes:
  1. Live download from OpenStreetMap via OSMnx.
  2. Load from pre-pickled backup graph.
  3. Generate a deterministic toy graph for unit testing.
"""

from __future__ import annotations

import math
import os
import pickle
from pathlib import Path
from typing import Optional, Tuple

import networkx as nx
import numpy as np

# OSMnx is optional — only needed for live downloads
try:
    import osmnx as ox
    HAS_OSMNX = True
except ImportError:
    HAS_OSMNX = False


BACKUP_DIR = Path(__file__).parent / "backups"


def load_city_graph(
    center: Tuple[float, float] = (12.9716, 77.5946),  # Bengaluru
    radius: int = 2500,
    network_type: str = "drive",
) -> nx.DiGraph:
    """Download a city road network from OpenStreetMap and clean it.

    Parameters
    ----------
    center : (lat, lon)
        Centre of the search circle.
    radius : int
        Radius in meters.
    network_type : str
        OSMnx network type (drive, walk, bike, all).

    Returns
    -------
    nx.DiGraph
        Cleaned graph with 'length', 'travel_time', 'speed_kph' edge attrs
        and 'x' (lon), 'y' (lat) node attrs.  Restricted to the largest
        strongly connected component.
    """
    if not HAS_OSMNX:
        raise RuntimeError(
            "osmnx is not installed.  Install it with: pip install osmnx\n"
            "Or use load_backup_graph() / generate_toy_graph() instead."
        )

    G = ox.graph_from_point(center, dist=radius, network_type=network_type)
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    # Extract largest strongly connected component
    G = _extract_lscc(G)

    # Add congestion attribute (default 0 — no congestion)
    for u, v, data in G.edges(data=True):
        data.setdefault("congestion", 0.0)

    return G


def _extract_lscc(G: nx.DiGraph) -> nx.DiGraph:
    """Return the Largest Strongly Connected Component as a fresh DiGraph."""
    scc = max(nx.strongly_connected_components(G), key=len)
    return G.subgraph(scc).copy()


def save_backup_graph(G: nx.DiGraph, name: str = "bengaluru_lscc") -> Path:
    """Pickle a graph to the backups directory."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    path = BACKUP_DIR / f"{name}.pkl"
    with open(path, "wb") as f:
        pickle.dump(G, f, protocol=pickle.HIGHEST_PROTOCOL)
    return path


def load_backup_graph(name: str = "bengaluru_lscc") -> nx.DiGraph:
    """Load a pre-pickled backup graph."""
    path = BACKUP_DIR / f"{name}.pkl"
    if not path.exists():
        raise FileNotFoundError(
            f"Backup graph not found: {path}\n"
            f"Available backups: {list(BACKUP_DIR.glob('*.pkl'))}"
        )
    with open(path, "rb") as f:
        return pickle.load(f)


def generate_toy_graph(
    n_nodes: int = 15,
    seed: int = 42,
    area_km: float = 5.0,
) -> nx.DiGraph:
    """Generate a deterministic small city-like graph for testing.

    Creates a random geometric graph in 2D (lat/lon space) with bidirectional
    road edges, realistic lengths and travel times.

    Parameters
    ----------
    n_nodes : int
        Number of intersection nodes.
    seed : int
        Deterministic seed.
    area_km : float
        Simulated area side length in km.

    Returns
    -------
    nx.DiGraph
        A connected graph suitable for VRP testing.
    """
    rng = np.random.default_rng(seed)

    # Base coordinates (Bengaluru center)
    base_lat, base_lon = 12.9716, 77.5946
    km_per_deg_lat = 111.0
    km_per_deg_lon = 111.0 * math.cos(math.radians(base_lat))

    # Random node positions
    lats = base_lat + rng.uniform(-area_km / 2, area_km / 2, n_nodes) / km_per_deg_lat
    lons = base_lon + rng.uniform(-area_km / 2, area_km / 2, n_nodes) / km_per_deg_lon

    G = nx.DiGraph()

    for i in range(n_nodes):
        G.add_node(i, y=float(lats[i]), x=float(lons[i]))

    # Connect each node to its K nearest neighbors (bidirectional)
    k_neighbors = min(4, n_nodes - 1)
    for i in range(n_nodes):
        dists = []
        for j in range(n_nodes):
            if i == j:
                dists.append(np.inf)
            else:
                d = _haversine(lats[i], lons[i], lats[j], lons[j])
                dists.append(d)
        nearest = np.argsort(dists)[:k_neighbors]
        for j in nearest:
            d = dists[j]
            speed = rng.uniform(20, 60)  # km/h
            travel_time = (d / 1000.0) / (speed / 3600.0)  # seconds
            G.add_edge(i, j, length=d, travel_time=travel_time,
                       speed_kph=speed, congestion=0.0)
            # Reverse edge (bidirectional road)
            if not G.has_edge(j, i):
                G.add_edge(j, i, length=d, travel_time=travel_time,
                           speed_kph=speed, congestion=0.0)

    # Ensure strong connectivity
    if not nx.is_strongly_connected(G):
        G = _extract_lscc(G)

    return G


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine distance in meters between two lat/lon points."""
    R = 6_371_000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_random_depot_and_destinations(
    G: nx.DiGraph,
    num_destinations: int = 10,
    seed: int = 42,
) -> Tuple[int, list]:
    """Pick a random depot and destination nodes from a graph.

    Returns
    -------
    (depot_node_id, [dest_node_id_1, ..., dest_node_id_N])
    """
    rng = np.random.default_rng(seed)
    nodes = list(G.nodes())
    selected = rng.choice(nodes, size=min(num_destinations + 1, len(nodes)), replace=False)
    depot = int(selected[0])
    destinations = [int(n) for n in selected[1:]]
    return depot, destinations
