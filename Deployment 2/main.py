from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import Depends, FastAPI, HTTPException
from typing import Annotated, Any
from sqlalchemy.pool import NullPool
import uuid
from pydantic import BaseModel, Field
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import create_engine, Integer, Column, String, Float
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from utils.preprocessing import preprocessing

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")


DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"


engine = create_engine(DATABASE_URL, poolclass=NullPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DBNasabah(Base):
    __tablename__ = "nasabah"

    nasabah_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
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
    day_of_week = Column(String(100), nullable=False)
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


import uuid
from pydantic import BaseModel, Field, ConfigDict


class NasabahCreate(BaseModel):
 
    age: int
    job: str
    marital: str
    education: str
    default: str
    housing: str
    loan: str
    contact: str
    month: str
    day_of_week: str 
    duration: int
    campaign: int
    pdays: int
    previous: int
    poutcome: str
    

    emp_var_rate: float = Field(alias='emp.var.rate') 
    cons_price_idx: float = Field(alias='cons.price.idx')
    cons_conf_idx: float = Field(alias='cons.conf.idx')
    euribor3m: float
    nr_employed: float = Field(alias='nr.employed')
    
 
    balance: int 

    model_config = ConfigDict(
        populate_by_name=True, 
        extra='ignore'         
    )


class NasabahResponse(BaseModel):
    # nasabah_id: uuid.UUID 
    # age: int
    # job: str
    # marital: str
    # education: str
    # default: str
    # housing: str
    # loan: str
    # contact: str
    # month: str
    # day_of_week: str 
    # duration: int
    # campaign: int
    # pdays: int
    # previous: int
    # poutcome: str
    

    # emp_var_rate: float
    # cons_price_idx: float
    # cons_conf_idx: float
    # euribor3m: float
    # nr_employed: float
    # balance: int

    predicted: float 
    
    model_config = ConfigDict(
        from_attributes=True 
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Rest API")

@app.get("/")
async def root():
    return {"message": "Sever is Ok"}

@app.post("/nasabah/", response_model=NasabahResponse)
async def create_nasabah(
    nasabah: NasabahCreate 
):

    nasabah_data = nasabah.model_dump()
    
    predicted_proba = await preprocessing(nasabah_data)
    predicted_proba = float(predicted_proba)
    
    return {"predicted": predicted_proba}
