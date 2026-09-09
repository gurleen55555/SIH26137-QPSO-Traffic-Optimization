"""
WebSocket /ws/convergence — streams per-iteration fitness data to the D3 chart.
"""

from __future__ import annotations

import asyncio
import json

import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.main import app_state
from algos.vrp_formulator import build_vrp_from_graph
from algos.convergence_analyzer import ConvergenceAnalyzer
from data.osm_loader import get_random_depot_and_destinations

router = APIRouter()


@router.websocket("/ws/convergence")
async def convergence_stream(ws: WebSocket):
    """Stream real-time convergence data for all algorithms.

    Client sends a start message (optional JSON config), then receives
    per-iteration fitness records as they are computed.
    """
    await ws.accept()

    try:
        # Wait for config from client (or use defaults)
        config_msg = await asyncio.wait_for(ws.receive_text(), timeout=5.0)
        try:
            config = json.loads(config_msg)
        except (json.JSONDecodeError, TypeError):
            config = {}
    except asyncio.TimeoutError:
        config = {}

    G = app_state.get("graph")
    if G is None:
        await ws.send_json({"error": "Graph not loaded"})
        await ws.close()
        return

    num_dest = config.get("num_destinations", 10)
    num_vehicles = config.get("num_vehicles", 3)
    seed = config.get("seed", 42)

    depot, destinations = get_random_depot_and_destinations(G, num_destinations=num_dest, seed=seed)
    rng = np.random.default_rng(seed)
    demands = rng.uniform(5, 25, len(destinations)).tolist()

    vrp = build_vrp_from_graph(
        G, depot, destinations, demands,
        num_vehicles=num_vehicles,
        vehicle_capacity=config.get("vehicle_capacity", 100.0),
    )

    # Buffer records to send via WebSocket
    records = []

    def on_progress(algo_name, record):
        records.append({"algorithm": algo_name, **record})

    # Run synchronously (algorithms are CPU-bound and complete quickly on toy graphs)
    analyzer = ConvergenceAnalyzer(seed=seed, callback=on_progress)

    try:
        # Run in a thread to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        benchmark = await loop.run_in_executor(None, analyzer.run, vrp)

        # Stream all records
        for record in records:
            await ws.send_json(record)

        # Send final summary
        await ws.send_json({
            "type": "summary",
            "summary": benchmark.summary,
        })

    except WebSocketDisconnect:
        pass
    finally:
        try:
            await ws.close()
        except Exception:
            pass
