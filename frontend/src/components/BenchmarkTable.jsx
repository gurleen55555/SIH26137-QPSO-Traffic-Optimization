export default function BenchmarkTable({ summary }) {
  if (!summary?.length) return null

  const sorted = [...summary].sort((a, b) => a.best_fitness - b.best_fitness)
  const bestFitness = sorted[0]?.best_fitness

  return (
    <table className="benchmark-table">
      <thead>
        <tr>
          <th>Algorithm</th>
          <th>Fitness</th>
          <th>Runtime</th>
          <th>Iters</th>
        </tr>
      </thead>
      <tbody>
        {sorted.map((entry, i) => (
          <tr key={entry.algorithm} className={entry.best_fitness === bestFitness ? 'best' : ''}>
            <td style={{ fontWeight: 600 }}>
              {entry.best_fitness === bestFitness ? '🏆 ' : ''}
              {entry.algorithm}
            </td>
            <td>{entry.best_fitness.toFixed(1)}</td>
            <td>{(entry.runtime_s * 1000).toFixed(0)} ms</td>
            <td>{entry.iterations}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
