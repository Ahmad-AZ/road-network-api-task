from fastapi import FastAPI
from app.routers import networks


from app.models import Base
from app.database import engine


app = FastAPI()
app.include_router(networks.router)
Base.metadata.create_all(bind=engine)
print("Creating tables...")
print("Tables to create:", Base.metadata.tables.keys())