import React from 'react'

const TABS = [
  { id: 'operations', label: 'Fleet Command', icon: '🚚' },
  { id: 'benchmark', label: 'Benchmark Lab', icon: '📊' },
  { id: 'explainability', label: 'QPSO Inspector', icon: '⚛️' },
  { id: 'analytics', label: 'Impact Analytics', icon: '📈' },
  { id: 'reports', label: 'Reports & Exports', icon: '📑' },
]

export default function Navbar({
  activeTab,
  setActiveTab,
  role,
  setRole,
  isDark,
  setIsDark,
  onInjectScenario,
}) {
  return (
    <header className="app-navbar">
      <div className="brand-section">
        <div className="brand-logo">
          <span className="brand-icon">⚡</span>
          <div>
            <div className="brand-title">Q-ITROS</div>
            <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
              SIH 2026 PS 137 · Smart Gov Traffic Control
            </div>
          </div>
        </div>
        <span className="brand-tag">v2.4 Live</span>

        <div className="system-status-pill">
          <span style={{ color: 'var(--accent-emerald)' }}>●</span>
          <span>Bengaluru City Graph (742 Nodes, 1,486 Edges)</span>
        </div>
      </div>

      <nav className="nav-tabs">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            className={`nav-tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span>{tab.icon}</span>
            <span>{tab.label}</span>
          </button>
        ))}
      </nav>

      <div className="nav-actions">
        {/* Quick Scenario Preset Triggers */}
        <button
          className="action-btn"
          style={{ background: 'rgba(0, 230, 118, 0.1)', color: 'var(--accent-emerald)', borderColor: 'rgba(0, 230, 118, 0.3)' }}
          onClick={() => onInjectScenario('normal')}
          title="Reset to Normal Traffic"
        >
          🟢 Normal
        </button>
        <button
          className="action-btn"
          style={{ background: 'rgba(255, 179, 0, 0.1)', color: 'var(--accent-amber)', borderColor: 'rgba(255, 179, 0, 0.3)' }}
          onClick={() => onInjectScenario('morning_rush')}
          title="Simulate Rush Hour Congestion (+140% arterial delay)"
        >
          🟡 Rush Hour
        </button>
        <button
          className="action-btn"
          style={{ background: 'rgba(255, 23, 68, 0.1)', color: 'var(--accent-rose)', borderColor: 'rgba(255, 23, 68, 0.3)' }}
          onClick={() => onInjectScenario('indiranagar_accident')}
          title="Simulate Major Incident at Node 142"
        >
          🔴 Incident
        </button>

        {/* Role Selector */}
        <select
          className="role-select"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        >
          <option value="operator">Traffic Operator</option>
          <option value="planner">Urban Planner</option>
          <option value="auditor">Algorithm Auditor</option>
        </select>

        {/* Dark/Light Toggle */}
        <button
          className="theme-toggle-btn"
          onClick={() => setIsDark(!isDark)}
          title="Toggle Light / Dark theme"
        >
          {isDark ? '☀️ Light' : '🌙 Dark'}
        </button>
      </div>
    </header>
  )
}
