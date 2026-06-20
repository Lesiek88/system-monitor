import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'
import { FetchStatus } from './api'
import type { HistoryPoint } from './types'

const MAX_POINTS = 30

function App() {
  const [history, setHistory] = useState<HistoryPoint[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const interval = setInterval(() => {
      FetchStatus()
        .then((dane) => {
          const point: HistoryPoint = {
            time: new Date().toLocaleTimeString(),
            cpu: dane.cpu.Zużycie_procenty,
            ram: dane.ram.ram.procenty,
          }
          setHistory((prev) => [...prev, point].slice(-MAX_POINTS))
        })
        .catch((err) => setError(err.message))
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  if (error) {
    return <div>Błąd: {error}</div>
  }

  return (
    <div>
      <h1>System Monitor</h1>
      <LineChart width={700} height={300} data={history}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis domain={[0, 100]} />
        <Tooltip />
        <Line type="monotone" dataKey="cpu" stroke="#38bdf8" name="CPU %" dot={false} />
        <Line type="monotone" dataKey="ram" stroke="#2dd4bf" name="RAM %" dot={false} />
      </LineChart>
    </div>
  )
}

export default App