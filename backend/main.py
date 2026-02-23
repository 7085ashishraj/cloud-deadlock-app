from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from services.deadlock_service import DeadlockDetector

app = FastAPI(title="Cloud Deadlock App API")

# Setup CORS to allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Deadlock Detector
detector = DeadlockDetector()

# Pydantic Models for requests
class NodeRequest(BaseModel):
    id: str

class EdgeRequest(BaseModel):
    process_id: str
    resource_id: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cloud Deadlock App API"}

@app.post("/api/process")
def add_process(data: NodeRequest):
    detector.add_process(data.id)
    return {"status": "success", "message": f"Process {data.id} added."}

@app.post("/api/resource")
def add_resource(data: NodeRequest):
    detector.add_resource(data.id)
    return {"status": "success", "message": f"Resource {data.id} added."}

@app.post("/api/request")
def request_resource(data: EdgeRequest):
    if not detector.graph.has_node(data.process_id) or not detector.graph.has_node(data.resource_id):
        raise HTTPException(status_code=400, detail="Process or Resource not found")
    detector.request_resource(data.process_id, data.resource_id)
    return {"status": "success", "message": f"Process {data.process_id} requested Resource {data.resource_id}."}

@app.post("/api/allocate")
def allocate_resource(data: EdgeRequest):
    if not detector.graph.has_node(data.process_id) or not detector.graph.has_node(data.resource_id):
        raise HTTPException(status_code=400, detail="Process or Resource not found")
    detector.allocate_resource(data.process_id, data.resource_id)
    return {"status": "success", "message": f"Resource {data.resource_id} allocated to Process {data.process_id}."}

@app.get("/api/detect")
def detect_deadlock():
    result = detector.detect_deadlock()
    return result

@app.get("/api/graph")
def get_graph():
    """Returns the current graph structure for frontend visualization."""
    nodes = [{"id": n, "type": detector.graph.nodes[n].get("type", "unknown")} for n in detector.graph.nodes()]
    edges = [{"source": u, "target": v} for u, v in detector.graph.edges()]
    return {"nodes": nodes, "edges": edges}

@app.post("/api/reset")
def reset_graph():
    detector.clear()
    return {"status": "success", "message": "Graph states cleared"}
