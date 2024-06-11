from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from database import engine, metadata
from models import logs
from schemas import LogCreate, Log
from databases import Database

app = FastAPI()
database = Database(DATABASE_URL)

metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/api/logs", response_model=Log, status_code=201)
async def create_log(log: LogCreate):
    query = logs.insert().values(
        timestamp=log.timestamp,
        level=log.level,
        message=log.message,
        source=log.source
    )
    last_record_id = await database.execute(query)
    return {**log.dict(), "id": last_record_id}

@app.get("/api/logs", response_model=list[Log])
async def read_logs(start: str = None, end: str = None, level: str = None):
    query = select([logs])
    if start:
        query = query.where(logs.c.timestamp >= start)
    if end:
        query = query.where(logs.c.timestamp <= end)
    if level:
        query = query.where(logs.c.level == level)
    results = await database.fetch_all(query)
    return results

@app.delete("/api/logs", status_code=204)
async def delete_logs(before: str = None):
    if before:
        query = logs.delete().where(logs.c.timestamp < before)
        await database.execute(query)
    return

