from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum

class NodeType(enum.Enum):
    process = "process"
    resource = "resource"

class EdgeType(enum.Enum):
    request = "request"
    allocate = "allocate"

class NodeModel(Base):
    __tablename__ = "nodes"
    id = Column(String(50), primary_key=True, index=True)
    type = Column(Enum(NodeType), nullable=False)

class EdgeModel(Base):
    __tablename__ = "edges"
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(50), nullable=False)
    target_id = Column(String(50), nullable=False)
    type = Column(Enum(EdgeType), nullable=False)
