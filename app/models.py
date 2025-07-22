from sqlalchemy import Column, Integer, String
from app.database import Base, engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from datetime import datetime


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)



class Edge(Base):
    __tablename__ = "edges"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    geometry = Column(Geometry(geometry_type='LINESTRING', srid=4326), nullable=False)
    is_current = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    network_id = Column(Integer, ForeignKey("road_network.id"), nullable=False)

    network = relationship("RoadNetwork", back_populates="edges")

class RoadNetwork(Base):
    __tablename__ = "road_network"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    customer_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    edges = relationship("Edge", back_populates="network")







