from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI(title="RailGuard Agents")

track_health = 100

@app.get("/")
def root():
    return {"system": "RailGuard Agents", "status": "active"}

@app.get("/health")
def health():
    return {"track_health": track_health, "status": "ok"}

@app.post("/track/detect")
def detect():
    global track_health
    if random.random() > 0.85:
        track_health -= 15
        return {"alert": "CRITICAL", "defect": "Crack detected", "health": track_health}
    return {"alert": "OK", "health": track_health}

@app.get("/maintenance/predict")
def maintenance():
    return {"predictions": [{"equipment": "Track A", "failure_risk": "HIGH"}]}

@app.post("/emergency/report")
def emergency():
    return {"incident_id": "INC_001", "response_dispatched": True}

@app.get("/traffic/status")
def traffic():
    return {"active_trains": 42, "delays": 3}

@app.get("/dashboard")
def dashboard():
    return {"track_health": track_health, "active_trains": 42}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
