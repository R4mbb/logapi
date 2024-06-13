from sqlalchemy import Table, Column, Integer, String, DateTime
from database import metadata

logs = Table(
    "logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", DateTime),
    Column("level", String(50)),
    Column("message", String(255)),
    Column("source", String(100)),
)
