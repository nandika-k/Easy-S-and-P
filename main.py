from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional
import os

#creating the engine
password = os.getenv("DB_PASSWORD")
DATABASE_URL = f"mysql+mysqlconnector://root:{password}@localhost/easy_s_and_p"
engine = create_engine(DATABASE_URL)

#create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#start FastAPI app
app = FastAPI()

#method to open session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#method to get stocks. takes in sector filter (optional), sort_by which defaults to ticker, and database session from method above.
@app.get("/stocks")
def get_stocks(sector: Optional[str] = None, sort_by: Optional[str] = "Ticker", db: Session = Depends(get_db)):
    #query the sql table
    query = db.query(WIKI_DATA, YAHOO_FIN_DATA)
    
    #filter by sector if needed
    try: 
        if sector is not None:
            query = query.filter(WIKI_DATA.Sector == sector)

        #join WIKI_DATA and YAHOO_FIN_DATA tables
        query = query.join(YAHOO_FIN_DATA, YAHOO_FIN_DATA.Ticker == WIKI_DATA.Ticker)
        
        #if the column doesn't exist, default to Ticker
        sort_col = getattr(YAHOO_FIN_DATA, sort_by, YAHOO_FIN_DATA.Ticker) or getattr(WIKI_DATA, sort_by, WIKI_DATA.Ticker)
        #sort data in ascending order by chosen col
        query = query.order_by(sort_col.asc())
            
        #execute and return query
        results = query.all()
        
        #exception if query goes wrong
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    #create list of dictionaries to store all returned rows
    rows = []
    for wiki, yahoo in results:
        rows.append(
            {
                "Ticker": wiki.Ticker,
                "Security": wiki.Security,
                "Sector": wiki.Sector,
                "Sub_Industry": wiki.Sub_Industry,
                "Beta": yahoo.Beta,
                "Recommendation_Score": yahoo.Recommendation_Score
            }
        )
        
    return rows

class WIKI_DATA(Base):
    __tablename__ = 'wiki_data'
    Ticker = Column(String(100), primary_key=True)
    Security = Column(String(255), nullable=True)
    Sector = Column(String(100), nullable=True)
    Sub_Industry = Column(String(100), nullable=True)
    HQ_Location = Column(String(100), nullable=True)
    Date_Added = Column(Date, nullable=True)
    CIK = Column(Integer)
    Founded = Column(Date, nullable=True)

class YAHOO_FIN_DATA(Base):
    __tablename__ = 'yahoo_fin_data'
    Ticker = Column(String(100), primary_key=True)
    Beta = Column(Float)
    Recommendation_Score = Column(Integer, nullable=True)