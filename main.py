from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def getDB():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()

dbDependency = Annotated[Session, Depends(getDB)]





@app.get("/{searchTerm}")
def readSearch(searchTerm: str):
    return {"message": "Hello World"}

@app.pos("/")
def test():
    return 0