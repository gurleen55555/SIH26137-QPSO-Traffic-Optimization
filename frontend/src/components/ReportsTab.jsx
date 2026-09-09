import React, { useState } from 'react'

export default function ReportsTab({ routes }) {
  const [activePreview, setActivePreview] = useState(null)

  const downloadJSON = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(routes || { demo: true, vehicles: 5 }, null, 2))
    const downloadAnchor = document.createElement('a')
    downloadAnchor.setAttribute("href", dataStr)
    downloadAnchor.setAttribute("download", "q_itros_optimized_routes.json")
    document.body.appendChild(downloadAnchor)
    downloadAnchor.click()
    downloadAnchor.remove()
  }

  const downloadGeoJSON = () => {
    const geojson = {
      type: "FeatureCollection",
      features: [
        {
          type: "Feature",
          geometry: {
            type: "LineString",
            coordinates: [
              [77.5946, 12.9716],
              [77.6412, 12.9784],
              [77.6245, 12.9352],
            ]
          },
          properties: { vehicle: "V1", distance_km: 7.2 }
        }
      ]
    }
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(geojson, null, 2))
    const downloadAnchor = document.createElement('a')
    downloadAnchor.setAttribute("href", dataStr)
    downloadAnchor.setAttribute("download", "q_itros_routes.geojson")
    document.body.appendChild(downloadAnchor)
    downloadAnchor.click()
    downloadAnchor.remove()
  }

  const handlePrintReport = () => {
    window.print()
  }

  return (
    <div className="tab-content" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div className="glass-card">
        <h2 style={{ margin: 0, color: 'var(--text-primary)', fontSize: '1.2rem' }}>
          📑 Reports, Data Exports & Executive Intelligence
        </h2>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
          Export optimized route manifests, spatial GIS polylines, or generate executive PDF summaries for municipal traffic authorities.
        </p>
      </div>

      {/* 4 Report Options Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div className="report-card">
          <div className="report-icon">📄</div>
          <div style={{ flex: 1 }}>
            <h3 style={{ fontSize: '1rem', fontWeight: '700', marginBottom: '4px' }}>Executive PDF Summary Report</h3>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '12px' }}>
              Comprehensive 3-page printable report containing QPSO convergence telemetry, baseline benchmarks, fuel savings, and urban corridor heatmaps.
            </p>
            <div style={{ display: 'flex', gap: '10px' }}>
              <button className="btn-primary-v2" onClick={handlePrintReport}>
                🖨️ Print / Save PDF
              </button>
              <button className="btn-secondary-v2" onClick={() => setActivePreview('executive')}>
                👁️ Preview
              </button>
            </div>
          </div>
        </div>

        <div className="report-card">
          <div className="report-icon">🗺️</div>
          <div style={{ flex: 1 }}>
            <h3 style={{ fontSize: '1rem', fontWeight: '700', marginBottom: '4px' }}>GeoJSON Spatial Polylines</h3>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '12px' }}>
              Standard GeoJSON FeatureCollection formatted for QGIS, ArcGIS, or Google Earth mapping tools.
            </p>
            <div style={{ display: 'flex', gap: '10px' }}>
              <button className="btn-primary-v2" onClick={downloadGeoJSON}>
                ⬇️ Download .geojson
              </button>
              <button className="btn-secondary-v2" onClick={() => setActivePreview('geojson')}>
                👁️ Inspect JSON
              </button>
            </div>
          </div>
        </div>

        <div className="report-card">
          <div className="report-icon">📦</div>
          <div style={{ flex: 1 }}>
            <h3 style={{ fontSize: '1rem', fontWeight: '700', marginBottom: '4px' }}>Route Dispatch JSON Payload</h3>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '12px' }}>
              Structured REST API JSON response containing vehicle stop sequences, ETA timestamps, and edge travel costs for FMS integration.
            </p>
            <div style={{ display: 'flex', gap: '10px' }}>
              <button className="btn-primary-v2" onClick={downloadJSON}>
                ⬇️ Export API JSON
              </button>
              <button className="btn-secondary-v2" onClick={() => setActivePreview('json')}>
                👁️ Inspect Payload
              </button>
            </div>
          </div>
        </div>

        <div className="report-card">
          <div className="report-icon">📋</div>
          <div style={{ flex: 1 }}>
            <h3 style={{ fontSize: '1rem', fontWeight: '700', marginBottom: '4px' }}>Driver Dispatch Timetable Manifest</h3>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '12px' }}>
              Printable per-vehicle delivery schedule with stop arrival ETAs, driver signature blocks, and emergency detour instructions.
            </p>
            <div style={{ display: 'flex', gap: '10px' }}>
              <button className="btn-primary-v2" onClick={handlePrintReport}>
                🖨️ Print Dispatch Sheets
              </button>
              <button className="btn-secondary-v2" onClick={() => setActivePreview('dispatch')}>
                👁️ Preview Timetable
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Preview Modal */}
      {activePreview && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0,0,0,0.8)',
            backdropFilter: 'blur(8px)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
          }}
        >
          <div
            className="glass-card"
            style={{ width: '600px', maxHeight: '80vh', overflowY: 'auto', background: 'var(--bg-secondary)', border: '1px solid var(--accent-cyan)' }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h3 style={{ margin: 0, color: 'var(--accent-cyan)' }}>Document Preview: {activePreview.toUpperCase()}</h3>
              <button className="btn-secondary-v2" onClick={() => setActivePreview(null)}>✕ Close</button>
            </div>

            <pre style={{ background: '#000', padding: '16px', borderRadius: '8px', fontSize: '0.75rem', color: '#00e5ff', overflowX: 'auto' }}>
              {activePreview === 'geojson' && JSON.stringify({ type: "FeatureCollection", features: ["Polyline V1", "Polyline V2"] }, null, 2)}
              {activePreview === 'json' && JSON.stringify(routes || { demo: true, vehicles: 5 }, null, 2)}
              {activePreview === 'dispatch' && `VEHICLE DISPATCH MANIFEST (Q-ITROS)
Depot: KSR Bengaluru Central
Vehicle V1: Depot ➔ Indiranagar (ETA: 12:45) ➔ Koramangala (ETA: 13:10)
Vehicle V2: Depot ➔ MG Road (ETA: 12:40) ➔ Cubbon Park (ETA: 13:00)`}
              {activePreview === 'executive' && `EXECUTIVE ROUTE OPTIMIZATION REPORT
System: Q-ITROS SIH 2026 PS 137
Solver: Quantum-Inspired Particle Swarm Optimization (QPSO)
Total Distance Saved: 10.3 km (-28.4%)
Total CO2 Avoided: 24.2 kg`}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}
