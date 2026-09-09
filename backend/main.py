"""
FastAPI Application — main entry point.

Loads the city graph on startup, mounts all REST routes and WebSocket
endpoints, and configures CORS for the React frontend.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any, Dict

import networkx as nx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.state import app_state
from backend.routes import optimize, benchmark, network, scenario, health
from backend.ws import convergence

# ---------------------------------------------------------------------------
# Lifespan — load graph once on startup
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the city graph on startup; clean up on shutdown."""
    from data.osm_loader import generate_toy_graph

    print(f"🚦 Loading city graph (toy {settings.toy_graph_nodes} nodes)...")
    G = generate_toy_graph(n_nodes=settings.toy_graph_nodes, seed=42)

    # Try to load a real OSMnx graph if available
    try:
        from data.osm_loader import load_backup_graph
        G = load_backup_graph("bengaluru_lscc")
        print(f"📦 Loaded backup Bengaluru graph: {G.number_of_nodes()} nodes")
    except Exception:
        print(f"⚡ Using toy graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    app_state.set("graph", G)
    app_state.set("graph_info", {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "type": "toy" if G.number_of_nodes() <= 30 else "osmnx",
    })

    yield  # app is running

    # Cleanup
    app_state.set("graph", None)
    print("🛑 Graph unloaded.")


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------
app = FastAPI(
    title="SIH26137 — QPSO Traffic Route Optimization API",
    description="Quantum-Inspired Intelligent Traffic Route Optimization using QPSO",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount route modules
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(optimize.router, prefix="/api/v1", tags=["Optimization"])
app.include_router(benchmark.router, prefix="/api/v1", tags=["Benchmark"])
app.include_router(network.router, prefix="/api/v1", tags=["Network"])
app.include_router(scenario.router, prefix="/api/v1", tags=["Scenario"])

# WebSocket endpoints
app.include_router(convergence.router, tags=["WebSocket"])
