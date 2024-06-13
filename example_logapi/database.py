from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///./logs.db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()
