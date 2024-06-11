from pydantic import BaseModel
from datetime import datetime

class LogCreate(BaseModel):
    timestamp: datetime
    level: str
    message: str
    source: str

class Log(BaseModel):
    id: int
    timestamp: datetime
    level: str
    message: str
    source: str

    class Config:
        from_attributes = True

