from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Füge Orchestrator zum Python-Pfad hinzu
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from orchestrator.semantic_engine import SemanticOrchestrator

app = FastAPI(title="ORDO.CONNECTORIS API Gateway")

# CORS konfigurieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Produktion einschränken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Orchestrator-Instanz
orchestrator = SemanticOrchestrator()

@app.post("/api/semantic/trigger/CONNECT:ALL")
async def trigger_connect_all():
    try:
        orchestrator.connect_all()
        return {"status": "success", "message": "Alle Datenbanken verbunden"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/connect/{database}")
async def connect_database(database: str):
    try:
        if database not in orchestrator.connections:
            orchestrator.connect_all()  # Verbinde spezifische Datenbank
        return {
            "status": "connected",
            "database": database,
            "type": type(orchestrator.connections[database]).__name__
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def get_cluster_status():
    try:
        status = {}
        for db_name, conn in orchestrator.connections.items():
            status[db_name] = "connected" if conn else "disconnected"
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query")
async def execute_sparql_query(query: str):
    try:
        results = orchestrator.query_semantic(query)
        return {"results": [dict(row) for row in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)