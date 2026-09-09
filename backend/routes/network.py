"""
GET /api/v1/network/graph — Return the city graph as GeoJSON.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from backend.state import app_state

router = APIRouter()


@router.get("/network/graph")
async def get_network_graph():
    graph = app_state.get("graph")
    if graph is None:
        raise HTTPException(status_code=503, detail="Graph not loaded yet")

    features = []

    # Node features
    for node_id, data in graph.nodes(data=True):
        lat = data.get("y", 12.9716 + (node_id * 0.001))
        lon = data.get("x", 77.5946 + (node_id * 0.001))
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat],
            },
            "properties": {
                "node_id": node_id,
                "label": f"Node {node_id}",
            },
        })

    # Edge features
    for u, v, data in graph.edges(data=True):
        u_data = graph.nodes[u]
        v_data = graph.nodes[v]
        u_lat = u_data.get("y", 12.9716 + (u * 0.001))
        u_lon = u_data.get("x", 77.5946 + (u * 0.001))
        v_lat = v_data.get("y", 12.9716 + (v * 0.001))
        v_lon = v_data.get("x", 77.5946 + (v * 0.001))

        length = data.get("length", 1.0)
        congestion = data.get("congestion", 0.0)

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[u_lon, u_lat], [v_lon, v_lat]],
            },
            "properties": {
                "source": u,
                "target": v,
                "length_m": length,
                "congestion": congestion,
            },
        })

    return {
        "type": "FeatureCollection",
        "features": features,
    }
