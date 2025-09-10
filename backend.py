from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn

# Inizializza l'applicazione FastAPI
app = FastAPI(title="Stratega API")

# Definizione del modello per lo Stratega
class Strategist(BaseModel):
    name: str
    description: str

# Database in memoria (lista di strateghi)
database: List[Dict[str, Any]] = []

# Rotta di base
@app.get("/")
def read_root():
    return {"message": "Benvenuto alla Stratega API!"}

# Rotta per ottenere tutti gli strateghi
@app.get("/strategists/")
def get_strategists():
    return {"strategists": database}

# Rotta per creare un nuovo stratega
@app.post("/strategists/", response_model=Strategist)
def create_strategist(strategist: Strategist):
    database.append(strategist.dict())
    return strategist

# Rotta per aggiornare uno stratega
@app.put("/strategists/{strategist_id}", response_model=Strategist)
def update_strategist(strategist_id: int, strategist: Strategist):
    if strategist_id >= len(database) or strategist_id < 0:
        raise HTTPException(status_code=404, detail="Stratega non trovato")
    database[strategist_id] = strategist.dict()
    return strategist

# Rotta per eliminare uno stratega
@app.delete("/strategists/{strategist_id}")
def delete_strategist(strategist_id: int):
    if strategist_id >= len(database) or strategist_id < 0:
        raise HTTPException(status_code=404, detail="Stratega non trovato")
    del database[strategist_id]
    return {"message": "Stratega eliminato con successo"}

# Se il file viene eseguito direttamente, lancia il server Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)