# ⚙️ Backend API & Streaming Server (`backend/`)

> **Owners:** M2 (DATA Lead - Models, DB, Redis) & M4 (STACK Lead - FastAPI, WebSockets, Deployment)

The `backend` directory provides the production web application layer built with **FastAPI**, high-performance **WebSockets**, **PostgreSQL/PostGIS** for spatial data storage, and **Redis** for in-memory pub/sub edge weight updates.

---

## 📂 Directory Layout

```
backend/
├── README.md              # This file - API specifications & operational guide
├── main.py                # Application initialization, middleware, lifecycle events
├── requirements.txt       # Python backend dependencies
├── config.py              # Environment variables & runtime settings
├── routes/                # REST endpoints
│   ├── __init__.py
│   ├── optimize.py        # POST /api/v1/optimize - VRP solving trigger
│   ├── benchmark.py       # POST /api/v1/benchmark - multi-algorithm evaluation
│   ├── network.py         # GET /api/v1/network/graph - GeoJSON graph output
│   ├── scenario.py        # POST /api/v1/scenario/inject - road closures & incidents
│   └── health.py          # GET /api/v1/health - system & database readiness
├── ws/                    # WebSocket streaming handlers
│   ├── __init__.py
│   ├── telemetry.py       # /ws/telemetry - live vehicle position stream
│   └── convergence.py     # /ws/convergence - per-iteration fitness stream for D3
├── db/                    # Spatial database & cache abstractions
│   ├── __init__.py
│   ├── connection.py      # SQLAlchemy engine & async sessionmaker
│   ├── models.py          # PostGIS Node, Edge, Route, and Incident ORM models
│   └── redis_client.py    # Redis pub/sub listener for dynamic edge weights
└── export/                # File exporters
    ├── __init__.py
    ├── geojson_export.py  # Converts optimized routes to standard GeoJSON FeatureCollection
    └── csv_export.py      # Exports benchmark comparison matrices
```

---

## 📡 REST API Specifications

### 1. Execute Optimization
- **Endpoint:** `POST /api/v1/optimize`
- **Request Body:**
```json
{
  "depot_node_id": 104523,
  "destination_node_ids": [104529, 104580, 104612, 104701, 104820],
  "num_vehicles": 3,
  "vehicle_capacity": 100,
  "demands": [20, 35, 15, 25, 30],
  "algorithm": "QPSO",
  "max_iterations": 150,
  "swarm_size": 30
}
```
- **Response:**
```json
{
  "status": "success",
  "run_id": "c8e2f89b-46a2-4a0b-9c71-081e6a9f4c32",
  "algorithm": "QPSO",
  "total_cost": 142.85,
  "execution_time_ms": 328.4,
  "vehicles": [
    {
      "vehicle_id": 1,
      "route_nodes": [104523, 104529, 104612, 104523],
      "route_distance_km": 12.4,
      "estimated_time_min": 24.5,
      "assigned_load": 35
    }
  ]
}
```

### 2. Run Comparative Benchmark
- **Endpoint:** `POST /api/v1/benchmark`
- **Request Body:**
```json
{
  "algorithms": ["QPSO", "PSO", "GA", "ACO", "DIJKSTRA"],
  "destination_node_ids": [104529, 104580, 104612, 104701, 104820],
  "num_vehicles": 3,
  "monte_carlo_trials": 5
}
```
- **Response:** Summary statistics table with mean fitness, standard deviation, convergence iteration, and runtime speedup relative to standard PSO.

---

## 🔌 WebSocket Channels

### 1. `/ws/convergence`
Broadcasts real-time optimization progress to the D3 line chart on every iteration:
```json
{
  "algorithm": "QPSO",
  "iteration": 42,
  "max_iterations": 150,
  "best_fitness": 164.21,
  "mean_fitness": 182.04,
  "timestamp": 1725883200.412
}
```

### 2. `/ws/telemetry`
Streams vehicle coordinates as simulated vehicles progress along their computed optimal routes:
```json
{
  "vehicle_id": 1,
  "latitude": 12.9716,
  "longitude": 77.5946,
  "current_edge": [104523, 104529],
  "speed_kmh": 32.5,
  "progress_pct": 45.0
}
```

---

## 🛡️ Reliability & Degradation Protocol

1. **Disconnected Graph Nodes:** If OSMnx ingestion produces disconnected components, the preprocessor filters the graph down to the **Largest Strongly Connected Component (LSCC)**.
2. **Missing Edge Weights:** If live traffic feed fails for an edge, default to free-flow travel time ($t = \text{length} / \text{speed\_limit}$).
3. **Database Unavailability:** If PostGIS is offline, the backend automatically fails over to the pre-pickled graph in `data/backups/bengaluru_lscc.pkl`.
