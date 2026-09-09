# 🎨 Interactive Visualization Dashboard (`frontend/`)

> **Owner:** M5 (VIZ Lead - React, Leaflet, D3.js)

The `frontend` directory contains the modern, responsive web application for real-time visualization of fleet routing, dynamic congestion heatmaps, live vehicle movement animations, and live D3 convergence analytics.

---

## 📂 Directory Layout

```
frontend/
├── README.md               # This file - UI architecture & development instructions
├── package.json            # Node dependencies (React 18, Leaflet, D3, Lucide-react)
├── vite.config.js          # Vite build configuration & proxy settings
├── index.html              # HTML5 entrypoint with Google Fonts (Inter)
└── src/
    ├── main.jsx            # React root application mount
    ├── App.jsx             # Main layout, state coordination, WebSocket listeners
    ├── index.css           # Global modern styling, sleek dark-mode design system
    ├── components/
    │   ├── MapCanvas.jsx       # Leaflet.js interactive road network & vehicle routes
    │   ├── ConvergencePlot.jsx # Real-time D3 line chart of algorithm fitness vs iterations
    │   ├── ScenarioControl.jsx # Inject road accidents, congestion surges, closures
    │   ├── MetricsBar.jsx      # Fleet KPIs (transit time, distance, CO2, capacity)
    │   ├── BenchmarkModal.jsx  # Multi-algorithm comparative performance bar charts
    │   └── RouteTable.jsx      # Per-vehicle turn-by-turn stop allocations
    ├── hooks/
    │   ├── useWebSocket.js     # Manages persistent WebSocket connection to backend
    │   └── useTrafficData.js   # Fetches network GeoJSON and live edge updates
    └── assets/                 # Icons, marker assets, custom map styling
```

---

## 🗺️ Leaflet Map Implementation Details

1. **Base Layers**: Sleek dark tile layer (CartoDB Dark Matter / Stadia Alidade Smooth Dark) optimized for glowing route overlays.
2. **Vehicle Routes**: Color-coded polylines (e.g., Vehicle 1: Cyan `#00e5ff`, Vehicle 2: Amber `#ffb300`, Vehicle 3: Emerald `#00e676`, Vehicle 4: Violet `#d500f9`).
3. **Interactive Markers**:
   - 🏭 **Depot Marker**: Highlighted central hub icon.
   - 📍 **Customer Stops**: Circle markers with delivery package badges and demand quantity labels.
   - 🚚 **Animated Vehicle Markers**: Interpolate along route geometry according to `/ws/telemetry` updates.
   - ⚠️ **Incident Markers**: Flashing warning icons at edges with active simulated blockages.

---

## 📈 Real-Time D3 Convergence Chart

The `ConvergencePlot.jsx` component provides an interactive D3 visualization:
- **X-Axis:** Iteration count ($0 \to T_{\max}$).
- **Y-Axis:** Swarm Best Fitness score (lower is better).
- **Multi-Line Series:** Live side-by-side traces for **QPSO**, **Classical PSO**, **GA**, and **ACO**.
- **Visual Proof for Judges:** Clearly showcases QPSO escaping the local minima plateaus where classical PSO flattens out.

---

## 🛠️ Development & Build Commands

```bash
# Install dependencies
npm install

# Start local development server with Hot Module Replacement (HMR)
npm run dev

# Build optimized production bundle
npm run build

# Preview production build locally
npm run preview
```
Default local port: `http://localhost:3000` (proxied to `http://localhost:8000` for API calls).
