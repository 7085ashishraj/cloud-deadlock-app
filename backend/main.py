from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
import os

from services.deadlock_service import DeadlockDetector
from services.s3_service import generate_and_upload_graph
from database import get_db, engine
import models

# Create all tables in the engine (This will create SQLite or MySQL schema)
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Cloud Deadlock App API")

# Setup CORS to allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folder for fallback image hosting
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Deadlock Detector
detector = DeadlockDetector()

# Dependency to populate graph from DB on load
def load_graph_from_db(db: Session):
    detector.clear()
    nodes = db.query(models.NodeModel).all()
    for n in nodes:
        if n.type == models.NodeType.process:
            detector.add_process(n.id)
        else:
            detector.add_resource(n.id)
    
    edges = db.query(models.EdgeModel).all()
    for e in edges:
        if e.type == models.EdgeType.request:
            detector.request_resource(e.source_id, e.target_id)
        else:
            detector.allocate_resource(e.target_id, e.source_id) # Resource -> Process

@app.on_event("startup")
def startup_event():
    with next(get_db()) as db:
        load_graph_from_db(db)
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
def add_process(data: NodeRequest, db: Session = Depends(get_db)):
    if db.query(models.NodeModel).filter(models.NodeModel.id == data.id).first():
        raise HTTPException(status_code=400, detail="Process already exists")
    
    db_node = models.NodeModel(id=data.id, type=models.NodeType.process)
    db.add(db_node)
    db.commit()
    
    detector.add_process(data.id)
    return {"status": "success", "message": f"Process {data.id} added."}

@app.post("/api/resource")
def add_resource(data: NodeRequest, db: Session = Depends(get_db)):
    if db.query(models.NodeModel).filter(models.NodeModel.id == data.id).first():
        raise HTTPException(status_code=400, detail="Resource already exists")

    db_node = models.NodeModel(id=data.id, type=models.NodeType.resource)
    db.add(db_node)
    db.commit()

    detector.add_resource(data.id)
    return {"status": "success", "message": f"Resource {data.id} added."}

@app.post("/api/request")
def request_resource(data: EdgeRequest, db: Session = Depends(get_db)):
    if not detector.graph.has_node(data.process_id) or not detector.graph.has_node(data.resource_id):
        raise HTTPException(status_code=400, detail="Process or Resource not found")

    db_edge = models.EdgeModel(source_id=data.process_id, target_id=data.resource_id, type=models.EdgeType.request)
    db.add(db_edge)
    db.commit()

    detector.request_resource(data.process_id, data.resource_id)
    return {"status": "success", "message": f"Process {data.process_id} requested Resource {data.resource_id}."}

@app.post("/api/allocate")
def allocate_resource(data: EdgeRequest, db: Session = Depends(get_db)):
    if not detector.graph.has_node(data.process_id) or not detector.graph.has_node(data.resource_id):
        raise HTTPException(status_code=400, detail="Process or Resource not found")

    # Allocation edge goes from resource to process in DB
    db_edge = models.EdgeModel(source_id=data.resource_id, target_id=data.process_id, type=models.EdgeType.allocate)
    db.add(db_edge)
    db.commit()

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

@app.get("/api/visualize")
def visualize_graph():
    """Generates an image via matplotlib, uploads to S3, and returns the public URL"""
    try:
        url = generate_and_upload_graph(detector.graph)
        return {"status": "success", "url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reset")
def reset_graph(db: Session = Depends(get_db)):
    detector.clear()
    db.query(models.EdgeModel).delete()
    db.query(models.NodeModel).delete()
    db.commit()
    return {"status": "success", "message": "Graph states cleared"}
