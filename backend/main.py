from fastapi import FastAPI
from database import engine, Base
import models


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Приложение запущено"}

@app.get("/health")
def health_check():
    return {"status": "OK", "database": "connected"}