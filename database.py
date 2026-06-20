import mysql.connector as mc
from dotenv import load_dotenv
import os

load_dotenv(
    
)
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}

def polaczenie():
    try:
        return mc.connect(**db_config)
    except mc.Error as err:
        print("Błąd podczas łączenia z bazą danych:", err)
        return None
    
def zapisz_dane(dane):
    conn = polaczenie()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO dane 
                   (timestamp, cpu_procent, ram_procent, ram_uzyte_gb, swap_procent, dysk_procent, dysk_odczyt_mb, dysk_zapis_mb, siec_pobrane_kb, siec_wyslane_kb, uptime_sekundy)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   """, (
                        dane['timestamp'],
                        dane['cpu']['Zużycie_procenty'],
                        dane['ram']['ram']['procenty'],
                        dane['ram']['ram']['zużycie_gb'],
                        dane['ram']['swap']['procenty'],
                        dane['zużycie_dysku'][0]['procenty'],
                        dane['szybkość_dysku']['przeczytane_ms_s'],
                        dane['szybkość_dysku']['napisane_ms_s'],
                        dane['sieć']['pobrane_kb_s'],
                        dane['sieć']['wysłane_kb_s'],
                        dane['online']['suma_sekund'],
                   ))
        conn.commit()
    except mc.Error as err:
        print("Błąd podczas zapisu do bazy:", err)
        conn.rollback()
    finally:
        conn.close()

def pobierz_historie():
    conn = polaczenie()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM dane ORDER BY timestamp DESC LIMIT 60")
        wynik = cursor.fetchall()
        conn.close()
        return wynik
    except mc.Error as err:
        print("Nastąpił błąd podczas pobierania histori:", err)
        return []
    finally:
        conn.close()

    