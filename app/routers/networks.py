from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from fastapi import Query
from shapely import wkt #can convert WKT (from DB) into coordinates for GeoJSON
from datetime import datetime

import json


router = APIRouter(prefix="/networks", tags=["Road Networks"])

@router.post("/upload")
async def upload_network(
    file: UploadFile = File(...),
    name: str = Form(...),
    customer_id: str = Form(...),
    db: Session = Depends(get_db)
):
    print("Uploading network...")

    if not file.filename.endswith(".geojson"):
        raise HTTPException(status_code=400, detail="Only .geojson files are accepted")
    content = await file.read()
    geojson_data = json.loads(content)

    network = models.RoadNetwork(name= name, customer_id=customer_id)
    db.add(network)
    db.commit()
    db.refresh(network) # to use a the id field that was set by the database

    features = geojson_data.get("features", [])
    for feature in features:
        geometry = feature.get("geometry")
        if geometry["type"] == "LineString":
            coords = geometry["coordinates"]
            well_known_text = f"LINESTRING({', '.join(f'{x[0]} {x[1]}' for x in coords)})"
            edge = models.Edge(
                network_id=network.id,
                geometry=well_known_text,
                is_current=True
            )
            db.add(edge)
    db.commit()
    return {"message": f"Uploaded road network '{name}' with {len(features)} features."}


@router.post("/update")
async def update_network(
    file: UploadFile = File(...),
    name: str = Form(...),
    customer_id: str = Form(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".geojson"):
        raise HTTPException(status_code=400, detail="Only .geojson files are accepted")

    content = await file.read()
    geojson_data = json.loads(content)
    network = db.query(models.RoadNetwork).filter_by(name=name, customer_id=customer_id).first()
    if not network:
        raise HTTPException(status_code=404, detail="Road network not found")
    
    db.query(models.Edge).filter_by(network_id=network.id, is_current=True).update({"is_current": False})
    db.commit()


    features = geojson_data.get("features",[])
    for feature in features:
        geometry = feature.get("geometry")
        if geometry["type"] == "LineString":
            coords = geometry["coordinates"]
            well_known_text = f"LINESTRING({', '.join(f'{x[0]} {x[1]}' for x in coords)})"
            new_edge = models.Edge(
                network_id=network.id,
                geometry=well_known_text,
                is_current=True
            )
            db.add(new_edge)
    db.commit()
    return {
        "message": f"Updated road network '{name}'. "
                   f"Old edges marked as outdated. {len(features)} new edges added."
    }






@router.get("/{network_id}/edges")
def get_edges(
    network_id: int,
    customer_id: str = Query(...),
    timestamp: datetime = Query(None),
    db: Session = Depends(get_db)
):
    network = db.query(models.RoadNetwork).filter_by(id=network_id, customer_id=customer_id).first()
    if not network:
        raise HTTPException(status_code=404, detail="Network not found for this customer")

    edges_query = db.query(models.Edge).filter_by(network_id=network.id)

    if timestamp:
        edges_query = edges_query.filter(models.Edge.created_at <= timestamp)
    if not timestamp:
        edges_query = edges_query.filter_by(is_current=True)

    edges = edges_query.all()

    features = []
    for edge in edges:
        line = wkt.loads(db.scalar(edge.geometry.ST_AsText()))  # Convert WKT to LineString object
        coords = list(line.coords)
        geojson_feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            },
            "properties": {
                "id": edge.id,
                "is_current": edge.is_current
            }
        }
        features.append(geojson_feature)

    return {
        "type": "FeatureCollection",
        "features": features
    }
