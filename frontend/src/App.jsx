import { useState, useCallback, useEffect } from 'react'
import Navbar from './components/Navbar'
import OperationsTab from './components/OperationsTab'
import BenchmarkTab from './components/BenchmarkTab'
import ExplainabilityTab from './components/ExplainabilityTab'
import AnalyticsTab from './components/AnalyticsTab'
import ReportsTab from './components/ReportsTab'

import { getFallbackGraphData, getFallbackOptimization, getFallbackBenchmark } from './utils/mockEngine'

const API_BASE = '/api/v1'

function App() {
  const [activeTab, setActiveTab] = useState('operations')
  const [role, setRole] = useState('operator')
  const [isDark, setIsDark] = useState(true)

  // Map Engine state — default to Leaflet for instant clean rendering without key requirement
  const envApiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''
  const [mapProvider, setMapProvider] = useState(envApiKey ? 'google' : 'leaflet')
  const [apiKey, setApiKey] = useState(envApiKey)

  const [status, setStatus] = useState('idle') // idle | running | success | error
  const [routes, setRoutes] = useState(null)
  const [convergence, setConvergence] = useState({})
  const [benchmarkSummary, setBenchmarkSummary] = useState([])
  const [graphData, setGraphData] = useState(null)
  const [errorMsg, setErrorMsg] = useState('')

  // Handle theme class on <html> element
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.remove('light')
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
      document.documentElement.classList.add('light')
    }
  }, [isDark])

  // Load network graph with automatic fallback
  const loadGraph = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/network/graph`)
      if (!res.ok) throw new Error('Failed to load graph from API')
      const data = await res.json()
      setGraphData(data)
    } catch (err) {
      console.warn('Backend API unavailable, loading self-contained graph data:', err)
      setGraphData(getFallbackGraphData())
    }
  }, [])

  // Auto-load graph on initial render
  useEffect(() => {
    loadGraph()
    // Initial optimization load
    setRoutes(getFallbackOptimization({ algorithm: 'QPSO', num_vehicles: 5 }))
    setConvergence({ QPSO: getFallbackOptimization({ algorithm: 'QPSO' }).convergence_history })
  }, [loadGraph])

  // Run single algorithm optimization with automatic fallback
  const runOptimize = useCallback(async (config) => {
    setStatus('running')
    setErrorMsg('')
    try {
      const res = await fetch(`${API_BASE}/optimize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setRoutes(data)
      setConvergence((prev) => ({
        ...prev,
        [data.algorithm]: data.convergence_history,
      }))
      setStatus('success')
    } catch (err) {
      console.warn('API error, computing local fallback optimization:', err)
      const data = getFallbackOptimization(config)
      setRoutes(data)
      setConvergence((prev) => ({
        ...prev,
        [data.algorithm]: data.convergence_history,
      }))
      setStatus('success')
    }
  }, [])

  // Run full benchmark with automatic fallback
  const runBenchmark = useCallback(async (config) => {
    setStatus('running')
    setErrorMsg('')
    setConvergence({})
    setBenchmarkSummary([])
    try {
      const res = await fetch(`${API_BASE}/benchmark`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setConvergence(data.convergence)
      setBenchmarkSummary(data.summary)
      setStatus('success')
    } catch (err) {
      console.warn('API error, running local fallback benchmark:', err)
      const data = getFallbackBenchmark()
      setConvergence(data.convergence)
      setBenchmarkSummary(data.summary)
      setStatus('success')
    }
  }, [])

  // Inject traffic scenario with automatic fallback
  const injectScenario = useCallback(
    async (scenario) => {
      try {
        await fetch(`${API_BASE}/scenario/inject`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ scenario }),
        })
      } catch (err) {
        console.warn('Scenario inject API call handled locally:', err)
      }
      loadGraph()
    },
    [loadGraph]
  )

  return (
    <div className="app-container">
      {/* Top Navbar Header */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        role={role}
        setRole={setRole}
        isDark={isDark}
        setIsDark={setIsDark}
        onInjectScenario={injectScenario}
      />

      {/* Main Tab Content */}
      <main className="main-content">
        {activeTab === 'operations' && (
          <OperationsTab
            status={status}
            routes={routes}
            convergence={convergence}
            graphData={graphData}
            onOptimize={runOptimize}
            onBenchmark={runBenchmark}
            onLoadGraph={loadGraph}
            onInjectScenario={injectScenario}
            mapProvider={mapProvider}
            setMapProvider={setMapProvider}
            apiKey={apiKey}
            setApiKey={setApiKey}
          />
        )}

        {activeTab === 'benchmark' && (
          <BenchmarkTab
            status={status}
            convergence={convergence}
            benchmarkSummary={benchmarkSummary}
            onBenchmark={runBenchmark}
          />
        )}

        {activeTab === 'explainability' && <ExplainabilityTab />}

        {activeTab === 'analytics' && <AnalyticsTab />}

        {activeTab === 'reports' && <ReportsTab routes={routes} />}
      </main>

      {/* Toast status indicators */}
      {status === 'running' && (
        <div className="status-bar running pulse" style={{ position: 'fixed', bottom: 20, right: 20, zIndex: 1000 }}>
          ⚡ Executing QPSO Optimization Engine...
        </div>
      )}
      {status === 'error' && (
        <div className="status-bar error" style={{ position: 'fixed', bottom: 20, right: 20, zIndex: 1000 }}>
          ❌ {errorMsg || 'An error occurred'}
        </div>
      )}
    </div>
  )
}

export default App
