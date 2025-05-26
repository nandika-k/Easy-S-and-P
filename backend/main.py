from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#start FastAPI app
app = FastAPI()

'''
CREATE TABLE s_and_p_stocks (
	Symbol VARCHAR(100) NOT NULL,
    Security VARCHAR(255) NOT NULL,
    GICS_Sector VARCHAR(255),
    GICS_Sub_Industry VARCHAR(255),
    Headquarters_Location VARCHAR(255),
    Date_Added DATE,
    CIK INT NOT NULL,
    Founded DATE,
    PRIMARY KEY (Symbol)
);

CREATE TABLE yfin_ticker_info (
	Ticker VARCHAR(100) NOT NULL,
    Beta INT NOT NULL,
    Recommendation_Score INT NOT NULL,
    PRIMARY KEY (Ticker)
);

'''

class WIKI_DATA(Base):
    __tablename__ = 's_and_p_stocks'
    symbol = Column(String(100), primary_key=True)
    security = Column(String(255), nullable=True)
    sector = Column(String(100), nullable=True)
    sub_industry = Column(String(100), nullable=True)
    hq_location = Column(String(100), nullable=True)
    date_added = Column(Date, nullable=True)
    cik = Column(Integer)
    date_founded = Column(Date, nullable=True)