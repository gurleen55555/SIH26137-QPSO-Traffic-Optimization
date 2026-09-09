import React, { useState } from 'react'

const ALGORITHMS = ['QPSO', 'PSO', 'GA', 'ACO', 'Dijkstra', 'A*']

export default function ControlPanel({
  status,
  onOptimize,
  onBenchmark,
  onLoadGraph,
  onInjectScenario,
  mapProvider,
  setMapProvider,
  apiKey,
  setApiKey,
}) {
  const [algorithm, setAlgorithm] = useState('QPSO')
  const [numVehicles, setNumVehicles] = useState(5)
  const [numDestinations, setNumDestinations] = useState(9)
  const [maxIterations, setMaxIterations] = useState(150)
  const [depot, setDepot] = useState('ksr_bengaluru')

  // Multi-objective weighting sliders
  const [wTime, setWTime] = useState(40)
  const [wFuel, setWFuel] = useState(30)
  const [wBalance, setWBalance] = useState(20)

  const isRunning = status === 'running'

  const handleOptimize = () => {
    onOptimize({
      algorithm,
      num_vehicles: numVehicles,
      num_destinations: numDestinations,
      max_iterations: maxIterations,
      vehicle_capacity: 100,
      weights: {
        time: wTime / 100,
        fuel: wFuel / 100,
        balance: wBalance / 100,
      },
    })
  }

  const handleBenchmark = () => {
    onBenchmark({
      algorithms: ALGORITHMS,
      num_vehicles: numVehicles,
      num_destinations: numDestinations,
    })
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
      <div className="card-title">
        <span>⚙️ Optimization & Map Engine</span>
      </div>

      {/* Map Engine Selection */}
      <div className="form-group">
        <label>Map Tile Engine</label>
        <select
          className="form-control"
          value={mapProvider}
          onChange={(e) => setMapProvider(e.target.value)}
        >
          <option value="leaflet">🌐 Dark Vector Leaflet (Offline / Carto)</option>
          <option value="google">🗺️ Google Maps JavaScript API</option>
        </select>
      </div>

      {/* API Key Box with Styled Glass Background */}
      {mapProvider === 'google' && (
        <div
          className="form-group"
          style={{
            background: 'rgba(0, 229, 255, 0.06)',
            border: '1px solid rgba(0, 229, 255, 0.25)',
            borderRadius: '10px',
            padding: '12px',
            boxShadow: '0 4px 12px rgba(0, 229, 255, 0.08)',
          }}
        >
          <label style={{ color: 'var(--accent-cyan)', fontWeight: '700' }}>
            🔑 Google Maps API Key
          </label>
          <input
            type="password"
            className="form-control"
            placeholder="AIzaSy... (Enter API Key)"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            style={{
              background: 'rgba(15, 23, 42, 0.9)',
              borderColor: 'rgba(0, 229, 255, 0.3)',
            }}
          />
          <div style={{ fontSize: '0.68rem', color: 'var(--text-secondary)', marginTop: '6px' }}>
            ✨ Custom Google Maps styling enabled. Blank defaults to Dark Leaflet tiles.
          </div>
        </div>
      )}

      <div className="form-group">
        <label>Primary Optimization Algorithm</label>
        <select
          className="form-control"
          value={algorithm}
          onChange={(e) => setAlgorithm(e.target.value)}
        >
          {ALGORITHMS.map((a) => (
            <option key={a} value={a}>
              {a} {a === 'QPSO' ? '⚡ (Quantum-Inspired - Recommended)' : ''}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Depot Hub Location</label>
        <select
          className="form-control"
          value={depot}
          onChange={(e) => setDepot(e.target.value)}
        >
          <option value="ksr_bengaluru">📍 KSR Bengaluru Central Depot</option>
          <option value="indiranagar">📍 Indiranagar Hub</option>
          <option value="electronic_city">📍 Electronic City Hub</option>
        </select>
      </div>

      <div className="form-group">
        <label>
          <span>Active Fleet Size (Vehicles)</span>
          <span style={{ color: 'var(--accent-cyan)' }}>{numVehicles} Vehicles</span>
        </label>
        <input
          type="range"
          className="form-range"
          min="1"
          max="10"
          value={numVehicles}
          onChange={(e) => setNumVehicles(parseInt(e.target.value))}
        />
      </div>

      <div className="form-group">
        <label>
          <span>Delivery Destinations</span>
          <span style={{ color: 'var(--accent-cyan)' }}>{numDestinations} Locations</span>
        </label>
        <input
          type="range"
          className="form-range"
          min="3"
          max="20"
          value={numDestinations}
          onChange={(e) => setNumDestinations(parseInt(e.target.value))}
        />
      </div>

      {/* Multi-Objective Weighting */}
      <div style={{ borderTop: '1px solid var(--border-glass)', paddingTop: '10px' }}>
        <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)', marginBottom: '8px' }}>
          🎯 MULTI-OBJECTIVE WEIGHTS
        </div>

        <div className="form-group">
          <label>
            <span>Travel Time</span>
            <span>{wTime}%</span>
          </label>
          <input
            type="range"
            className="form-range"
            min="0"
            max="100"
            value={wTime}
            onChange={(e) => setWTime(parseInt(e.target.value))}
          />
        </div>

        <div className="form-group">
          <label>
            <span>Fuel Efficiency</span>
            <span>{wFuel}%</span>
          </label>
          <input
            type="range"
            className="form-range"
            min="0"
            max="100"
            value={wFuel}
            onChange={(e) => setWFuel(parseInt(e.target.value))}
          />
        </div>
      </div>

      {/* Action Buttons */}
      <button
        className="btn-primary-v2"
        onClick={handleOptimize}
        disabled={isRunning}
        style={{ width: '100%', justifyContent: 'center' }}
      >
        {isRunning ? '⚡ Running Optimization...' : `🚀 Solve Route with ${algorithm}`}
      </button>

      <button
        className="btn-secondary-v2"
        onClick={handleBenchmark}
        disabled={isRunning}
        style={{ width: '100%', justifyContent: 'center' }}
      >
        📊 Run 6-Algorithm Benchmark
      </button>
    </div>
  )
}
