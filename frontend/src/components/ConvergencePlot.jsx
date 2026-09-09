import { useEffect, useRef } from 'react'
import * as d3 from 'd3'

const ALGO_COLORS = {
  QPSO: '#00e5ff',
  PSO: '#ff6e40',
  GA: '#00e676',
  ACO: '#ffb300',
  Dijkstra: '#94a3b8',
  'A*': '#b388ff',
}

export default function ConvergencePlot({ convergence }) {
  const svgRef = useRef(null)
  const containerRef = useRef(null)

  useEffect(() => {
    if (!convergence || Object.keys(convergence).length === 0) return
    if (!containerRef.current) return

    const container = containerRef.current
    const width = container.clientWidth
    const height = container.clientHeight - 40 // leave room for legend
    const margin = { top: 16, right: 20, bottom: 36, left: 60 }
    const innerW = width - margin.left - margin.right
    const innerH = height - margin.top - margin.bottom

    // Clear previous
    d3.select(svgRef.current).selectAll('*').remove()

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`)

    // Compute scales
    let maxIter = 0
    let minFit = Infinity
    let maxFit = -Infinity

    for (const [name, history] of Object.entries(convergence)) {
      if (!history?.length) continue
      maxIter = Math.max(maxIter, history.length)
      for (const d of history) {
        if (d.best_fitness < minFit) minFit = d.best_fitness
        if (d.best_fitness > maxFit) maxFit = d.best_fitness
      }
    }

    if (maxIter === 0) return

    const x = d3.scaleLinear().domain([0, maxIter - 1]).range([0, innerW])
    const y = d3.scaleLinear().domain([minFit * 0.95, maxFit * 1.05]).range([innerH, 0])

    // Grid lines
    g.append('g')
      .attr('class', 'grid')
      .call(d3.axisLeft(y).ticks(5).tickSize(-innerW).tickFormat(''))

    // Axes
    g.append('g')
      .attr('class', 'axis')
      .attr('transform', `translate(0,${innerH})`)
      .call(d3.axisBottom(x).ticks(Math.min(maxIter, 8)))

    g.append('g')
      .attr('class', 'axis')
      .call(d3.axisLeft(y).ticks(5).tickFormat(d => d >= 1000 ? `${(d/1000).toFixed(1)}k` : d.toFixed(0)))

    // Axis labels
    svg.append('text')
      .attr('x', margin.left + innerW / 2)
      .attr('y', height - 4)
      .attr('text-anchor', 'middle')
      .attr('fill', '#64748b')
      .attr('font-size', '0.7rem')
      .text('Iteration')

    svg.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('x', -(margin.top + innerH / 2))
      .attr('y', 14)
      .attr('text-anchor', 'middle')
      .attr('fill', '#64748b')
      .attr('font-size', '0.7rem')
      .text('Best Fitness (lower = better)')

    // Draw lines
    const line = d3.line()
      .x((d, i) => x(i))
      .y(d => y(d.best_fitness))
      .curve(d3.curveMonotoneX)

    for (const [name, history] of Object.entries(convergence)) {
      if (!history?.length) continue
      const color = ALGO_COLORS[name] || '#888'

      g.append('path')
        .datum(history)
        .attr('fill', 'none')
        .attr('stroke', color)
        .attr('stroke-width', name === 'QPSO' ? 2.5 : 1.5)
        .attr('stroke-opacity', name === 'QPSO' ? 1 : 0.7)
        .attr('d', line)

      // Endpoint dot
      const last = history[history.length - 1]
      g.append('circle')
        .attr('cx', x(history.length - 1))
        .attr('cy', y(last.best_fitness))
        .attr('r', 4)
        .attr('fill', color)
        .attr('stroke', '#0a0e1a')
        .attr('stroke-width', 2)
    }
  }, [convergence])

  const algoNames = Object.keys(convergence || {})

  return (
    <div ref={containerRef} style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <svg ref={svgRef} style={{ flex: 1 }} />
      {algoNames.length > 0 && (
        <div className="chart-legend">
          {algoNames.map(name => (
            <div key={name} className="chart-legend-item">
              <div className="chart-legend-swatch" style={{ background: ALGO_COLORS[name] || '#888' }} />
              <span>{name}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
