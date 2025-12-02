from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import Depends, FastAPI, HTTPException
from typing import Annotated, Any
import uuid
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import create_engine, Integer, Column, String, Float
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class nasabah(Base):
    __tablename__ = "nasabah"

    nasabah_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, # <-- Fungsi ini dipanggil saat objek dibuat
        unique=True,
        nullable=False
    )
    age = Column(Integer, nullable=False)
    job = Column(String(100), nullable=False)
    marital = Column(String(100), nullable=False)
    education = Column(String(100), nullable=False)
    default = Column(String(100), nullable=False)
    balance = Column(Integer, nullable=False)
    housing = Column(String(100), nullable=False)
    loan = Column(String(100), nullable=False)
    contact = Column(String(100), nullable=False)
    day = Column(String(100), nullable=False)
    month = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)
    campaign = Column(Integer, nullable=False)
    pdays = Column(Integer, nullable=False)
    previous = Column(Integer, nullable=False)
    poutcome = Column(String(100), nullable=False)
    emp_var_rate = Column(Float, nullable=False)
    cons_price_idx = Column(Float, nullable=False)
    cons_conf_idx = Column(Float, nullable=False)
    euribor3m = Column(Float, nullable=False)
    nr_employed = Column(Float, nullable=False)
    predicted = Column(Float, nullable=False)

Base.metadata.create_all(engine)



class NasabahCreate(BaseModel):
    age: int
    job: str
    marital: str
    education: str
    default: str
    balance: int
    housing: str
    loan: str
    contact: str
    day: str
    month: str
    duration: int
    campaign: int
    pdays: int
    previous: int
    poutcome: str
    emp_var_rate: float
    cons_price_idx: float
    cons_conf_idx: float
    euribor3m: float
    nr_employed: float

class NasabahResponse(BaseModel):
    nasabah_id: uuid.UUID
    age: int
    job: str
    marital: str
    education: str
    default: str
    balance: int
    housing: str
    loan: str
    contact: str
    day: str
    month: str
    duration: int
    campaign: int
    pdays: int
    previous: int
    poutcome: str
    emp_var_rate: float
    cons_price_idx: float
    cons_conf_idx: float
    euribor3m: float
    nr_employed: float
    predicted: float
    
    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Rest API")

@app.get("/")
def root():
    return {"message": "Sever is Ok"}

@app.post("/nasabah/", response_model=NasabahResponse)
def create_nasabah(nasabah: NasabahCreate, db: Session = Depends(get_db)):


    db_nasabah = nasabah(**nasabah.dict())
    db.add(db_nasabah)
    db.commit()
    db.refresh(db_nasabah)
    return db_nasabah
