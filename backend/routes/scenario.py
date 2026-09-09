"""
POST /api/v1/scenario/inject — Inject traffic events and optionally re-optimize.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.state import app_state
from data.traffic_updater import (
    TrafficScenario,
    apply_synthetic_traffic,
    inject_incident,
    clear_incidents,
)

router = APIRouter()


class ScenarioRequest(BaseModel):
    scenario: str = Field(
        default="normal",
        description="Traffic scenario: normal, morning_rush, evening_rush, heavy_congestion",
    )
    incident_edge: Optional[list] = Field(
        default=None,
        description="[u, v] edge to inject incident on",
    )
    incident_severity: str = Field(
        default="closure",
        description="Incident severity: closure, accident, slowdown",
    )
    seed: Optional[int] = None


@router.post("/scenario/inject")
async def inject_scenario(req: ScenarioRequest):
    """Apply a traffic scenario and/or inject an incident."""
    G = app_state.get("graph")
    if G is None:
        raise HTTPException(status_code=503, detail="Graph not loaded")

    # Apply scenario
    try:
        scenario = TrafficScenario(req.scenario)
    except ValueError:
        scenario = TrafficScenario.NORMAL

    apply_synthetic_traffic(G, scenario=scenario, seed=req.seed)

    # Inject specific incident if provided
    if req.incident_edge and len(req.incident_edge) == 2:
        u, v = req.incident_edge
        inject_incident(G, (u, v), severity=req.incident_severity)

    return {
        "status": "success",
        "scenario": scenario.value,
        "incident_edge": req.incident_edge,
        "incident_severity": req.incident_severity if req.incident_edge else None,
        "message": f"Applied {scenario.value} traffic scenario to graph",
    }


@router.post("/scenario/clear")
async def clear_scenario():
    """Reset all traffic to baseline."""
    G = app_state.get("graph")
    if G is None:
        raise HTTPException(status_code=503, detail="Graph not loaded")

    clear_incidents(G)
    return {"status": "success", "message": "All traffic cleared to baseline"}
