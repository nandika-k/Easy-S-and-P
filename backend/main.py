from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#start FastAPI app
app = FastAPI()

class WIKI_DATA(Base):
    __tablename__ = 's_and_p_stocks'
    Ticker = Column(String(100), primary_key=True)
    Security = Column(String(255), nullable=True)
    Sector = Column(String(100), nullable=True)
    Sub_Industry = Column(String(100), nullable=True)
    HQ_Location = Column(String(100), nullable=True)
    Date_Added = Column(Date, nullable=True)
    CIK = Column(Integer)
    Founded = Column(Date, nullable=True)

class YAHOO_FIN_DATA(Base):
    __tablename__ = 'yfin_ticker_info'
    Ticker = Column(String(100), primary_key=True)
    bBeta = Column(Float)
    Recommendation_Score = Column(Integer, nullable=True)