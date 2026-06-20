export interface CpuData{
    Zużycie_procenty: number
    rdzenie: number
    wątki: number
}

export interface RamSzczegoly{
    procenty: number
    zużycie_gb: number
    wolne_gb: number
    suma_gb: number
}

export interface DiskData{
    urządzenie: string
    mountpoint: string
    procenty: number
    użyte_gb: number
    suma_gb: number
    alert: boolean
}

export interface StatusResponse{
    timestamp: number
    cpu: CpuData
    ram: {
        ram: RamSzczegoly
        swap: RamSzczegoly
    }
    zużycie_dysku: DiskData[]
}

export interface HistoryRow{
    timestamp: number
    cpu_procent: number
    ram_procent: number
    ram_uzyte_gb: number
    swap_procent: number
    dysk_procent: number
    dysk_odczyt_mb: number
    dysk_zapis_mb: number
    siec_pobrane_kb: number
    siec_wyslane_kb: number
    uptime_sekundy: number
}

export type PoziomAlertu = "ostrzeżenie" | "krytyczny"

export interface AlertItem{
    typ: string
    wartosc: number
    poziom: PoziomAlertu
}

export interface AlertsResponse{
    alerty: AlertItem[]
    liczba: number
}

export interface HistoryPoint{
    time: string
    cpu: number
    ram: number
}