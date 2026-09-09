"""Health check endpoint."""

from fastapi import APIRouter
from backend.state import app_state

router = APIRouter()


@router.get("/health")
async def health_check():
    graph = app_state.get("graph")
    return {
        "status": "healthy" if graph is not None else "degraded",
        "graph_loaded": graph is not None,
        "nodes": graph.number_of_nodes() if graph is not None else 0,
        "edges": graph.number_of_edges() if graph is not None else 0,
    }
