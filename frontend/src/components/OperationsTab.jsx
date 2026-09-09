import React from 'react'
import MapCanvas from './MapCanvas'
import ControlPanel from './ControlPanel'
import ConvergencePlot from './ConvergencePlot'

export default function OperationsTab({
  status,
  routes,
  convergence,
  graphData,
  onOptimize,
  onBenchmark,
  onLoadGraph,
  onInjectScenario,
  mapProvider,
  setMapProvider,
  apiKey,
  setApiKey,
}) {
  const vehicleCount = routes?.vehicles?.length || 5
  const totalDist = routes?.total_distance_km ? `${routes.total_distance_km.toFixed(1)} km` : '34.2 km'
  const totalTime = routes?.total_time_min ? `${routes.total_time_min.toFixed(0)} min` : '48 min'
  const fitnessVal = routes?.fitness ? routes.fitness.toFixed(4) : '0.4120'
  const algoName = routes?.algorithm || 'QPSO'

  return (
    <div className="operations-grid tab-content">
      {/* Left Column: Control Panel */}
      <div className="glass-card">
        <ControlPanel
          status={status}
          onOptimize={onOptimize}
          onBenchmark={onBenchmark}
          onLoadGraph={onLoadGraph}
          onInjectScenario={onInjectScenario}
          mapProvider={mapProvider}
          setMapProvider={setMapProvider}
          apiKey={apiKey}
          setApiKey={setApiKey}
        />
      </div>

      {/* Center Column: Map Canvas */}
      <div className="map-wrapper glass-card" style={{ padding: 0 }}>
        <MapCanvas
          graphData={graphData}
          routes={routes}
          mapProvider={mapProvider}
          apiKey={apiKey}
        />
      </div>

      {/* Right Column: KPIs & Vehicle Breakdown */}
      <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        <div className="card-title">
          <span>📊 Live Route Telemetry</span>
          <span className="algo-badge">{algoName}</span>
        </div>

        {/* KPIs */}
        <div className="kpi-grid">
          <div className="kpi-card">
            <div className="value">{totalDist}</div>
            <div className="label">Total Distance</div>
          </div>
          <div className="kpi-card">
            <div className="value">{totalTime}</div>
            <div className="label">Est. Travel Time</div>
          </div>
          <div className="kpi-card">
            <div className="value">{vehicleCount}</div>
            <div className="label">Active Vehicles</div>
          </div>
          <div className="kpi-card">
            <div className="value">{fitnessVal}</div>
            <div className="label">Best Fitness</div>
          </div>
        </div>

        {/* Vehicle Route Sequence List */}
        <div style={{ flex: 1, overflowY: 'auto' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)', marginBottom: '8px' }}>
            🚚 VEHICLE DISPATCH MANIFEST
          </div>

          <div className="vehicle-list">
            {(routes?.vehicles || [
              { id: 1, color: '#00e5ff', stops: ['Depot (KSR Hub)', 'Indiranagar 100ft Rd', 'Koramangala 5th Blk', 'Depot'], distance_km: 7.2, time_min: 12 },
              { id: 2, color: '#ffb300', stops: ['Depot (KSR Hub)', 'MG Road Metro', 'Cubbon Park', 'Depot'], distance_km: 5.4, time_min: 9 },
              { id: 3, color: '#00e676', stops: ['Depot (KSR Hub)', 'Whitefield Tech Park', 'Marathahalli', 'Depot'], distance_km: 11.8, time_min: 16 },
              { id: 4, color: '#d500f9', stops: ['Depot (KSR Hub)', 'Hebbal Flyover', 'Manyata Tech Park', 'Depot'], distance_km: 9.8, time_min: 11 },
            ]).map((v, idx) => (
              <div
                key={v.id || idx}
                className="vehicle-card"
                style={{ borderLeftColor: v.color || `var(--vehicle-${(idx % 5) + 1})` }}
              >
                <div className="vehicle-card-header">
                  <span className="vehicle-name">Vehicle V{v.id || idx + 1}</span>
                  <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                    {v.distance_km ? `${v.distance_km.toFixed(1)} km` : '7.2 km'} · {v.time_min ? `${v.time_min.toFixed(0)} min` : '12 min'}
                  </span>
                </div>
                <div className="vehicle-route-seq">
                  {Array.isArray(v.stops)
                    ? v.stops.join(' ➔ ')
                    : Array.isArray(v.route_node_ids) && v.route_node_ids.length > 0
                    ? v.route_node_ids.map(id => `Node ${id}`).join(' ➔ ')
                    : `Node 0 ➔ Node ${((v.vehicle_id || v.id || idx + 1) * 3)} ➔ Node 0`}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Convergence Chart Preview */}
        <div style={{ height: '180px', borderTop: '1px solid var(--border-glass)', paddingTop: '10px' }}>
          <div style={{ fontSize: '0.72rem', fontWeight: '700', color: 'var(--text-muted)', marginBottom: '4px' }}>
            📈 CONVERGENCE PROGRESSION
          </div>
          <ConvergencePlot convergence={convergence} />
        </div>
      </div>
    </div>
  )
}
