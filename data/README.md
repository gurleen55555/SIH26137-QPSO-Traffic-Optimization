# 🗺️ Spatial Data & Traffic Simulation (`data/`)

> **Owner:** M2 (DATA Lead - Graph Pipeline & Simulation)

The `data` directory manages the urban road network graph ingestion using **OSMnx**, spatial road network caching, real-time traffic simulation via **synthetic Gaussian-noise perturbation** and **Eclipse SUMO**, and boundary zone partitioning.

---

## 📂 Directory Layout

```
data/
├── README.md              # This file - data ingestion & simulation guide
├── osm_loader.py          # OSMnx fetcher, graph cleaner, and pickle cache builder
├── traffic_updater.py     # Live edge speed & congestion injector
├── zone_partitioner.py    # Divides graph into geographic sub-zones for scalability
├── sumo_config/           # Eclipse SUMO micro-simulation files (optional/enrichment)
│   ├── network.net.xml
│   └── routes.rou.xml
└── backups/               # Pre-serialized fallback graphs (.pkl)
    ├── bengaluru_lscc.pkl # Pre-cleaned Largest Strongly Connected Component
    └── toy_network.pkl    # 15-node toy test graph for unit tests
```

---

## 🏙️ Urban Graph Extraction (Bengaluru Case Study)

The primary road network covers central Bengaluru (Shivajinagar, MG Road, Koramangala corridor):
- **Target Size:** ~600–800 nodes, ~1,500 directed edges.
- **Node Attributes:** `node_id`, `latitude`, `longitude`, `elevation`.
- **Edge Attributes:** `u`, `v`, `length_m`, `speed_kph`, `lanes`, `highway_type`, `base_travel_time_s`.

### Extraction Command
```python
import osmnx as ox

# Define bounding box or center point for Bengaluru CBD
G = ox.graph_from_point((12.9716, 77.5946), dist=2500, network_type="drive")
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)
```

### Graph Cleaning Rules
1. **Strongly Connected Component:** Road networks with dead ends or one-way traps can make VRP routes infeasible. We extract `G_scc = G.subgraph(max(nx.strongly_connected_components(G), key=len)).copy()`.
2. **Deterministic Node Indexing:** Nodes are mapped to contiguous $0 \dots N-1$ integers for ultra-fast NumPy matrix indexing during optimization.

---

## 🚦 Traffic Generation Models

### 1. Synthetic Gaussian-Noise Generator (Primary Demo Path)
To eliminate external network dependencies during live judging, edge speeds are dynamically adjusted every $\Delta t = 5\text{ s}$ using a stochastic model with diurnal rush-hour multipliers:

$$v_e(t) = v_{e,\text{free}} \cdot \mu_{\text{tod}}(t) \cdot \left(1 - \text{congestion\_index}_e(t)\right) + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2)$$

- **Morning Rush (08:30 - 10:30):** Flow multiplier $\times 1.8$ on arterial roads.
- **Evening Rush (17:30 - 20:00):** Flow multiplier $\times 2.1$ on outbound corridors.
- **Random Incident Injection:** Simulates sudden road closures ($v_e \to 0$, $t_e \to \infty$) to demonstrate dynamic QPSO re-routing in real-time.

### 2. Eclipse SUMO Integration (Secondary Mode)
For micro-simulation validation:
- Generates vehicle traces and lane-occupancy metrics.
- Uses TraCI (Traffic Control Interface) Python bridge to read induction loop data and update Redis edge weights.

---

## 🧩 Scalability: Zone Partitioning

For graphs exceeding ~800 nodes:
1. The bounding box is divided into 4 spatial quadrants ($Q_1, Q_2, Q_3, Q_4$).
2. Customer delivery nodes are clustered into zones using K-Means or spatial bounding boxes.
3. QPSO solves each sub-VRP independently in parallel threads.
4. Boundary inter-zone transfer nodes stitch the routes seamlessly.
