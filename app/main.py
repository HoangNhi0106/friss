from fastapi import FastAPI
from app.api import person
from app.db.database import engine, Base

app = FastAPI()

app.include_router(person.router, prefix="/persons", tags=["persons"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to my FastAPI application!"}

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)