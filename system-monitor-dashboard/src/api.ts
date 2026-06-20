import type { StatusResponse, AlertsResponse, HistoryRow } from './types'

const API_BASE = "http://127.0.0.1:8000"

export async function FetchStatus(): Promise<StatusResponse>{
    const respond = await fetch(`${API_BASE}/status`)
    if (!respond.ok){
        throw new Error(`Fetch failed: ${respond.status}`)
    }
    const data: StatusResponse = await respond.json()
    return data
}


export async function fetchAlerts(): Promise<AlertsResponse>{
    const respond = await fetch(`${API_BASE}/alerty`)
    if(!respond.ok){
        throw new Error(`Fetch Error: ${respond.status}`)
    }
    const data: AlertsResponse = await respond.json()
    return data
}

export async function fetchHistory(): Promise<HistoryRow[]>{
    const respond = await fetch(`${API_BASE}/historia`)
    if (!respond.ok){
        throw new Error(`Fetch Error: ${respond.status}`)
    }
    const data: HistoryRow[] = await respond.json()
    return data
}