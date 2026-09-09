import React, { useState, useEffect, useRef } from 'react'

export default function ExplainabilityTab() {
  const [betaStart, setBetaStart] = useState(1.0)
  const [betaEnd, setBetaEnd] = useState(0.2)
  const [swarmSize, setSwarmSize] = useState(50)
  const [iterations, setIterations] = useState(100)
  const [currentIter, setCurrentIter] = useState(42)

  const canvasRef = useRef(null)

  // HTML5 Canvas Swarm Animation
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    let animationFrameId

    // Generate random particle field around global optimum center (250, 150)
    const particles = Array.from({ length: swarmSize }, (_, i) => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 2,
      vy: (Math.random() - 0.5) * 2,
      pbestX: 250 + (Math.random() - 0.5) * 120,
      pbestY: 150 + (Math.random() - 0.5) * 80,
    }))

    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Draw background grid
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)'
      ctx.lineWidth = 1
      for (let x = 0; x < canvas.width; x += 40) {
        ctx.beginPath()
        ctx.moveTo(x, 0)
        ctx.lineTo(x, canvas.height)
        ctx.stroke()
      }
      for (let y = 0; y < canvas.height; y += 40) {
        ctx.beginPath()
        ctx.moveTo(0, y)
        ctx.lineTo(canvas.width, y)
        ctx.stroke()
      }

      // Target mbest center
      const mbestX = 250
      const mbestY = 150

      // Draw mbest glow center
      const gradient = ctx.createRadialGradient(mbestX, mbestY, 5, mbestX, mbestY, 40)
      gradient.addColorStop(0, 'rgba(0, 229, 255, 0.8)')
      gradient.addColorStop(1, 'rgba(0, 229, 255, 0)')
      ctx.fillStyle = gradient
      ctx.beginPath()
      ctx.arc(mbestX, mbestY, 40, 0, Math.PI * 2)
      ctx.fill()

      ctx.fillStyle = '#00e5ff'
      ctx.beginPath()
      ctx.arc(mbestX, mbestY, 6, 0, Math.PI * 2)
      ctx.fill()
      ctx.fillStyle = '#ffffff'
      ctx.font = '10px Inter'
      ctx.fillText('MBEST (Global Target)', mbestX - 45, mbestY - 12)

      // Update and draw quantum particles
      particles.forEach((p, idx) => {
        // Quantum Delta Potential Well pull equation simulation
        const dx = mbestX - p.x
        const dy = mbestY - p.y
        const dist = Math.sqrt(dx * dx + dy * dy)
        
        // Quantum random jump factor: beta * |mbest - x| * ln(1/u)
        const beta = betaStart - (currentIter / iterations) * (betaStart - betaEnd)
        const pull = 0.05 * beta

        p.vx = p.vx * 0.9 + dx * pull + (Math.random() - 0.5) * beta * 3
        p.vy = p.vy * 0.9 + dy * pull + (Math.random() - 0.5) * beta * 3

        p.x += p.vx
        p.y += p.vy

        // Draw particle line to pbest
        ctx.strokeStyle = 'rgba(0, 229, 255, 0.15)'
        ctx.beginPath()
        ctx.moveTo(p.x, p.y)
        ctx.lineTo(p.pbestX, p.pbestY)
        ctx.stroke()

        // Draw particle dot
        ctx.fillStyle = idx % 2 === 0 ? '#00e5ff' : '#d500f9'
        ctx.beginPath()
        ctx.arc(p.x, p.y, 3, 0, Math.PI * 2)
        ctx.fill()
      })

      animationFrameId = requestAnimationFrame(render)
    }

    render()

    return () => cancelAnimationFrame(animationFrameId)
  }, [swarmSize, betaStart, betaEnd, currentIter, iterations])

  return (
    <div className="tab-content" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Math & Physics Core Explanation */}
      <div className="math-card">
        <h2 style={{ margin: 0, color: 'var(--text-primary)', fontSize: '1.2rem' }}>
          ⚛️ QPSO Mathematical Core & Quantum Mechanics Mechanics
        </h2>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '6px' }}>
          In Quantum-Behaved Particle Swarm Optimization (QPSO), particles do not have fixed velocity vectors. Instead, each particle moves in a <strong>quantum delta potential well</strong> centered around its local attractor <em>p<sub>i</sub></em>, enabling global search without velocity limits.
        </p>

        {/* Formulated Equations */}
        <div className="math-formula">
          x<sub>i</sub><sup>t+1</sup> = p<sub>i</sub><sup>t</sup> ± β · |mbest - x<sub>i</sub><sup>t</sup>| · ln(1/u)
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px', fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
          <div style={{ background: 'rgba(0,0,0,0.2)', padding: '10px', borderRadius: '8px', border: '1px solid var(--border-glass)' }}>
            <strong style={{ color: 'var(--accent-cyan)' }}>1. Mean Best Position (mbest)</strong>
            <p style={{ marginTop: '4px' }}>Center of gravity of all personal best positions: mbest = (1/M) ∑ p<sub>i</sub>(t)</p>
          </div>
          <div style={{ background: 'rgba(0,0,0,0.2)', padding: '10px', borderRadius: '8px', border: '1px solid var(--border-glass)' }}>
            <strong style={{ color: 'var(--accent-violet)' }}>2. Contraction-Expansion (β)</strong>
            <p style={{ marginTop: '4px' }}>Linear decay factor controlling swarm convergence speed from exploration to exploitation.</p>
          </div>
          <div style={{ background: 'rgba(0,0,0,0.2)', padding: '10px', borderRadius: '8px', border: '1px solid var(--border-glass)' }}>
            <strong style={{ color: 'var(--accent-emerald)' }}>3. SPV Permutation Mapping</strong>
            <p style={{ marginTop: '4px' }}>Smallest-Position-Value rule maps continuous positions R<sup>n</sup> to discrete vehicle route sequences.</p>
          </div>
        </div>
      </div>

      {/* Inspector Controls & Live Swarm Visualizer Canvas */}
      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '20px' }}>
        {/* Controls */}
        <div className="glass-card">
          <div className="card-title">
            <span>⚙️ Quantum Parameter Knobs</span>
          </div>

          <div className="form-group">
            <label>
              <span>Initial Expansion β<sub>start</sub></span>
              <span>{betaStart}</span>
            </label>
            <input
              type="range"
              className="form-range"
              min="0.5"
              max="1.5"
              step="0.05"
              value={betaStart}
              onChange={(e) => setBetaStart(parseFloat(e.target.value))}
            />
          </div>

          <div className="form-group">
            <label>
              <span>Final Contraction β<sub>end</sub></span>
              <span>{betaEnd}</span>
            </label>
            <input
              type="range"
              className="form-range"
              min="0.05"
              max="0.5"
              step="0.05"
              value={betaEnd}
              onChange={(e) => setBetaEnd(parseFloat(e.target.value))}
            />
          </div>

          <div className="form-group">
            <label>
              <span>Swarm Population Size (M)</span>
              <span>{swarmSize} particles</span>
            </label>
            <input
              type="range"
              className="form-range"
              min="10"
              max="150"
              value={swarmSize}
              onChange={(e) => setSwarmSize(parseInt(e.target.value))}
            />
          </div>

          <div className="form-group">
            <label>
              <span>Iteration Progress</span>
              <span>{currentIter} / {iterations}</span>
            </label>
            <input
              type="range"
              className="form-range"
              min="1"
              max={iterations}
              value={currentIter}
              onChange={(e) => setCurrentIter(parseInt(e.target.value))}
            />
          </div>

          <div className="kpi-card" style={{ marginTop: '16px' }}>
            <div className="value">{(betaStart - (currentIter / iterations) * (betaStart - betaEnd)).toFixed(3)}</div>
            <div className="label">Current Active β Parameter</div>
          </div>
        </div>

        {/* HTML5 Canvas Swarm Visualizer */}
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column' }}>
          <div className="card-title">
            <span>🌌 Quantum Particle Swarm Field Visualizer</span>
            <span style={{ fontSize: '0.75rem', color: 'var(--accent-cyan)' }}>Live Simulation</span>
          </div>

          <div style={{ flex: 1, minHeight: '320px', position: 'relative', borderRadius: '8px', overflow: 'hidden', border: '1px solid var(--border-glass)', background: '#040711' }}>
            <canvas ref={canvasRef} width={650} height={320} style={{ width: '100%', height: '100%' }} />
          </div>
        </div>
      </div>
    </div>
  )
}
