from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI(root_path="/api")
models.Base.metadata.create_all(bind=engine)

def getDB():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()

dbDependency = Annotated[Session, Depends(getDB)]





@app.get("/status")
def checkStatus():
    return {"message": "Hello World!!!"}



if __name__ == "__main__":
    uvicorn.run(app, host="https://cs2300.skrublaub.xyz/api", port=80)#not sure if this is directed to the correct point
