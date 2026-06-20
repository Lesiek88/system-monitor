import psutil
import time

def pobierz_cpu():
    return {
        "Zużycie_procenty": psutil.cpu_percent(interval=1),
        "rdzenie": psutil.cpu_count(logical=False),
        "wątki": psutil.cpu_count(logical=True),
    }

def pobierz_ram():
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return{
        "ram": {
            "procenty": ram.percent,
            "zużycie_gb": round(ram.used / 1024 ** 3, 2),
            "wolne_gb": round(ram.available / 1024 ** 3, 2),
            "suma_gb": round(ram.total / 1024 ** 3,2),
        },
        "swap": {
            "procenty": swap.percent,
            "zużycie_gb": round(swap.used / 1024 ** 3,2),
            "wolne_gb": round(swap.free / 1024 ** 3, 2),
            "suma_gb": round(swap.total / 1024 ** 3, 2),
        }
    }

def pobierz_zużycie_dysku():
    wynik = []
    for dysk in psutil.disk_partitions():
        try:
            uzycie = psutil.disk_usage(dysk.mountpoint)
            wynik.append({
                "urządzenie": dysk.device,
                "mountpoint": dysk.mountpoint,
                "procenty": uzycie.percent,
                "użyte_gb": round(uzycie.used / 1024 ** 3,2),
                "suma_gb": round(uzycie.total / 1024 ** 3,2),
                "alert": uzycie.percent >= 70,
            })
        except PermissionError:
            pass
    return wynik
    

def pobierz_szybkosc_dysku(interval=1):
    przed = psutil.disk_io_counters()
    time.sleep(interval)
    po = psutil.disk_io_counters()
    return{
        "przeczytane_ms_s": round((po.read_bytes - przed.read_bytes) / 1024 ** 2, 2),
        "napisane_ms_s": round((po.write_bytes - przed.write_bytes) / 1024 ** 2,2),
    }


def pobierz_sieć(interval=1):
    przed = psutil.net_io_counters()
    time.sleep(interval)
    po = psutil.net_io_counters()
    return {
        "pobrane_kb_s": round((po.bytes_recv - przed.bytes_recv) / 1024,1),
        "wysłane_kb_s": round((po.bytes_sent - przed.bytes_sent) / 1024,1)
    }


def pobierz_dlugosc_dzialania():
    teraz = time.time()
    online = int(teraz-psutil.boot_time())
    return {
        "dni": online // 86400,
        "godziny": (online % 86400) // 3600,
        "minuty": (online % 3600) // 60,
        "sekundy": online % 60,
        "suma_sekund": online

    }

def pobierz_użytkowników():
    return[
        {"Użytkownik": u.name, "terminal": u.terminal, "host": u.host}
        for u in psutil.users()
    ]

def pobierz_najwiekszy_proces(n=10):
    procesy = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procesy.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return sorted(procesy, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:n] 

def zbierz_dane():
    return {
        "timestamp": time.time(),
        "cpu": pobierz_cpu(),
        "ram": pobierz_ram(),
        "zużycie_dysku": pobierz_zużycie_dysku(),
        "szybkość_dysku": pobierz_szybkosc_dysku(),
        "sieć": pobierz_sieć(),
        "online": pobierz_dlugosc_dzialania(),
        "użytkownicy": pobierz_użytkowników(),
        "najwyższy_proces": pobierz_najwiekszy_proces(),
    }


if __name__ == "__main__":
    import json
    dane = zbierz_dane()
    print(json.dumps(dane, indent=2, ensure_ascii=False))