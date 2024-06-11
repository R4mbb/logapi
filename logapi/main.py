from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from database import engine, metadata, DATABASE_URL
from models import logs
from schemas import LogCreate, Log
from databases import Database
from contextlib import asynccontextmanager
import datetime

app = FastAPI()
database = Database(DATABASE_URL)

metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

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
    query = select(logs)  # 여기서 수정됨
    if start:
        start_date = datetime.datetime.fromisoformat(start)
        query = query.where(logs.c.timestamp >= start_date)
    if end:
        end_date = datetime.datetime.fromisoformat(end)
        query = query.where(logs.c.timestamp <= end_date)
    if level:
        query = query.where(logs.c.level == level)
    results = await database.fetch_all(query)
    return [dict(result) for result in results]

@app.delete("/api/logs", status_code=204)
async def delete_logs(before: str = None):
    if before:
        before_date = datetime.datetime.fromisoformat(before)
        query = logs.delete().where(logs.c.timestamp < before_date)
        await database.execute(query)
    return

