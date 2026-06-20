from fastapi import FastAPI
from collector import zbierz_dane
from contextlib import asynccontextmanager
import database
import asyncio
from fastapi.middleware.cors import CORSMiddleware



async def zapisuj_co_sekunde():
    while True:
        try:
            dane = zbierz_dane()
            database.zapisz_dane(dane)
        except Exception as err:
            print("Błąd podczas zapisu:", err)
        await asyncio.sleep(3)

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(zapisuj_co_sekunde())
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/status")
def status():
    return zbierz_dane()

@app.get("/historia")
def historia():
    return database.pobierz_historie()

@app.get("/alerty")
def alerty():
    dane = zbierz_dane()
    alerty = []

    if dane['cpu']['Zużycie_procenty'] >= 90:
        alerty.append({"typ": "CPU", "wartosc": dane['cpu']["Zużycie_procenty"], "poziom": "krytyczny"})
    elif dane['cpu']['Zużycie_procenty'] >= 70:
        alerty.append({"typ": "CPU", "wartosc": dane['cpu']["Zużycie_procenty"], "poziom": "ostrzeżenie"})

    if dane['ram']['ram']['procenty'] >= 90:
        alerty.append({"typ": "RAM", "wartosc": dane["ram"]["ram"]["procenty"], "poziom": "krytyczny"})
    elif dane['ram']['ram']['procenty'] >= 80:
        alerty.append({"typ": "RAM", "wartosc": dane["ram"]["ram"]["procenty"], "poziom": "ostrzeżenie"})

    if dane['ram']['swap']['procenty'] > 0:
        alerty.append({"typ": "SWAP", "wartosc": dane["ram"]["swap"]["procenty"], "poziom": "ostrzeżenie"})

    for dysk in dane["zużycie_dysku"]:
        if dysk["procenty"] >= 85:
            alerty.append({"typ": f"DYSK {dysk['urządzenie']}", "wartosc": dysk["procenty"], "poziom": "krytyczny"})
        elif dysk["procenty"] >= 70:
            alerty.append({"typ": f"DYSK {dysk['urządzenie']}", "wartosc": dysk["procenty"], "poziom": "ostrzeżenie"})
    return {"alerty": alerty, "liczba": len(alerty)}