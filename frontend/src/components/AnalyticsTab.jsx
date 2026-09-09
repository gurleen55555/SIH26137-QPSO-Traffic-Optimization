import React from 'react'

export default function AnalyticsTab() {
  const bottlenecks = [
    { name: 'Silk Board Junction', avg_delay_min: 84, queue_length_km: 8.2, congestion_index: '94.2%', priority: 'Critical' },
    { name: 'Indiranagar 100ft Road', avg_delay_min: 68, queue_length_km: 5.4, congestion_index: '86.5%', priority: 'High' },
    { name: 'MG Road Metro Corridor', avg_delay_min: 61, queue_length_km: 4.1, congestion_index: '78.1%', priority: 'High' },
    { name: 'Hebbal Flyover Junction', avg_delay_min: 42, queue_length_km: 3.2, congestion_index: '65.0%', priority: 'Moderate' },
  ]

  const auditLog = [
    { id: 'RUN-9042', time: '12:24:10 PM', algo: 'QPSO', vehicles: 5, stops: 9, dist_saved: '10.3 km', co2_saved: '24.2 kg', status: 'Completed' },
    { id: 'RUN-9041', time: '11:50:02 AM', algo: 'QPSO', vehicles: 3, stops: 8, dist_saved: '7.8 km', co2_saved: '18.1 kg', status: 'Completed' },
    { id: 'RUN-9040', time: '11:15:45 AM', algo: 'ACO', vehicles: 4, stops: 12, dist_saved: '6.4 km', co2_saved: '14.9 kg', status: 'Completed' },
    { id: 'RUN-9039', time: '10:30:12 AM', algo: 'GA', vehicles: 5, stops: 10, dist_saved: '5.2 km', co2_saved: '12.1 kg', status: 'Completed' },
  ]

  return (
    <div className="tab-content" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Impact KPI Banner Grid */}
      <div className="kpi-row">
        <div className="kpi-card-v2">
          <div className="title">Total Routes Optimized</div>
          <div className="value" style={{ color: 'var(--accent-cyan)' }}>1,248</div>
          <div className="subtext">📈 +18.6% from last month</div>
        </div>

        <div className="kpi-card-v2 emerald">
          <div className="title">Avg Travel Time Savings</div>
          <div className="value" style={{ color: 'var(--accent-emerald)' }}>28.4%</div>
          <div className="subtext">⚡ 15.2 minutes saved per vehicle</div>
        </div>

        <div className="kpi-card-v2 amber">
          <div className="title">Fleet Fuel Savings</div>
          <div className="value" style={{ color: 'var(--accent-amber)' }}>3,420 L</div>
          <div className="subtext">⛽ Estimated ₹3.2L cost reduction</div>
        </div>

        <div className="kpi-card-v2 violet">
          <div className="title">CO₂ Emissions Avoided</div>
          <div className="value" style={{ color: 'var(--accent-violet)' }}>8.9 Tons</div>
          <div className="subtext">🌱 Equivalent to 410 trees planted</div>
        </div>
      </div>

      {/* Grid: Bottlenecks & Corridor Watchlist */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div className="glass-card">
          <div className="card-title">
            <span>🚨 Real-Time Traffic Bottleneck Watchlist</span>
          </div>

          <table className="data-table-v2">
            <thead>
              <tr>
                <th>Corridor Location</th>
                <th>Avg Delay</th>
                <th>Queue Length</th>
                <th>Congestion %</th>
                <th>Priority</th>
              </tr>
            </thead>
            <tbody>
              {bottlenecks.map((b) => (
                <tr key={b.name}>
                  <td style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{b.name}</td>
                  <td>{b.avg_delay_min} min</td>
                  <td>{b.queue_length_km} km</td>
                  <td style={{ color: 'var(--accent-rose)' }}>{b.congestion_index}</td>
                  <td>
                    <span
                      style={{
                        padding: '2px 6px',
                        borderRadius: '4px',
                        fontSize: '0.68rem',
                        background: b.priority === 'Critical' ? 'rgba(255,23,68,0.2)' : 'rgba(255,179,0,0.2)',
                        color: b.priority === 'Critical' ? 'var(--accent-rose)' : 'var(--accent-amber)',
                      }}
                    >
                      {b.priority}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="glass-card">
          <div className="card-title">
            <span>📊 QPSO Route Optimization Impact vs Baselines</span>
          </div>

          <div style={{ padding: '10px', fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
            <div style={{ marginBottom: '14px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span>Travel Time Reduction vs Dijkstra Baseline</span>
                <span style={{ fontWeight: '700', color: 'var(--accent-cyan)' }}>-28.4%</span>
              </div>
              <div style={{ height: '8px', background: 'rgba(255,255,255,0.06)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: '82%', height: '100%', background: 'var(--accent-cyan)' }} />
              </div>
            </div>

            <div style={{ marginBottom: '14px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span>Fuel Consumption Reduction vs A* Standard</span>
                <span style={{ fontWeight: '700', color: 'var(--accent-emerald)' }}>-18.6%</span>
              </div>
              <div style={{ height: '8px', background: 'rgba(255,255,255,0.06)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: '74%', height: '100%', background: 'var(--accent-emerald)' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span>Fleet Workload Balance Improvement vs GA</span>
                <span style={{ fontWeight: '700', color: 'var(--accent-amber)' }}>+32.1%</span>
              </div>
              <div style={{ height: '8px', background: 'rgba(255,255,255,0.06)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: '68%', height: '100%', background: 'var(--accent-amber)' }} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Historical Audit Trail */}
      <div className="glass-card">
        <div className="card-title">
          <span>📜 Historical Optimization Execution Audit Trail</span>
        </div>

        <table className="data-table-v2">
          <thead>
            <tr>
              <th>Run ID</th>
              <th>Timestamp</th>
              <th>Algorithm</th>
              <th>Vehicles</th>
              <th>Stops</th>
              <th>Distance Saved</th>
              <th>CO₂ Avoided</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {auditLog.map((log) => (
              <tr key={log.id}>
                <td style={{ fontFamily: 'monospace', color: 'var(--accent-cyan)' }}>{log.id}</td>
                <td>{log.time}</td>
                <td><span className="algo-badge">{log.algo}</span></td>
                <td>{log.vehicles}</td>
                <td>{log.stops}</td>
                <td style={{ color: 'var(--accent-emerald)' }}>{log.dist_saved}</td>
                <td>{log.co2_saved}</td>
                <td><span style={{ color: 'var(--accent-emerald)' }}>● {log.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
