export default function MetricsPanel({ routes }) {
  if (!routes?.vehicles) {
    return (
      <div className="kpi-grid">
        <KpiCard value="—" label="Total Distance" />
        <KpiCard value="—" label="Total Time" />
        <KpiCard value="—" label="Active Vehicles" />
        <KpiCard value="—" label="Best Fitness" />
      </div>
    )
  }

  const totalDistance = routes.vehicles.reduce((s, v) => s + (v.route_distance_m || 0), 0)
  const totalTime = routes.vehicles.reduce((s, v) => s + (v.route_time_s || 0), 0)
  const activeVehicles = routes.vehicles.filter(v => v.route_node_ids?.length > 0).length
  const co2 = (totalDistance * 0.00012).toFixed(2) // kg CO2

  return (
    <>
      <div className="kpi-grid">
        <KpiCard
          value={`${(totalDistance / 1000).toFixed(1)} km`}
          label="Total Distance"
        />
        <KpiCard
          value={`${(totalTime / 60).toFixed(1)} min`}
          label="Total Time"
        />
        <KpiCard
          value={activeVehicles}
          label="Active Vehicles"
        />
        <KpiCard
          value={routes.best_fitness?.toFixed(1) || '—'}
          label="Best Fitness"
        />
        <KpiCard
          value={`${co2} kg`}
          label="Est. CO₂"
        />
        <KpiCard
          value={`${(routes.execution_time_s * 1000).toFixed(0)} ms`}
          label="Runtime"
        />
      </div>

      {/* Per-vehicle breakdown */}
      <div style={{ marginTop: 12 }}>
        <h2 style={{ fontSize: '0.7rem', color: '#64748b', marginBottom: 8 }}>Vehicle Routes</h2>
        {routes.vehicles.map((v, i) => (
          <div
            key={i}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              padding: '4px 0',
              fontSize: '0.78rem',
              color: '#94a3b8',
              borderBottom: '1px solid rgba(255,255,255,0.04)',
            }}
          >
            <span style={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              background: ['#00e5ff', '#ffb300', '#00e676', '#d500f9', '#ff6e40'][i % 5],
              flexShrink: 0,
            }} />
            <span style={{ fontWeight: 600, color: '#f1f5f9' }}>V{v.vehicle_id}</span>
            <span>{v.route_node_ids?.length || 0} stops</span>
            <span style={{ marginLeft: 'auto', fontVariantNumeric: 'tabular-nums' }}>
              {(v.route_distance_m / 1000).toFixed(1)} km
            </span>
          </div>
        ))}
      </div>
    </>
  )
}

function KpiCard({ value, label }) {
  return (
    <div className="kpi-card">
      <div className="value">{value}</div>
      <div className="label">{label}</div>
    </div>
  )
}
