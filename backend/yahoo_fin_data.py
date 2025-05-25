import yfinance as yf
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import declarative_base, sessionmaker
import backend.scrape_wiki_data as scrape_wiki_data
import pandas as pd
import time
import random
import traceback
import os


cols = ['Ticker', 'Industry', 'Sub-Sector', 'Beta', 'Recommendation Score']
data_lists = []

password = os.getenv("DB_PASSWORD")
engine = create_engine('mysql+mysqlconnector://root:{password}@127.0.0.1/easy_s_and_p')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class StockData(Base):
    __tablename__ = 'stock_data'
    id = Column(Integer, primary_key=True)
    ticker = Column(String(10))
    industry = Column(String(255), nullable=True)
    sub_sector = Column(String(255), nullable=True)
    beta = Column(String(50))
    recommendation_score = Column(Integer)


Base.metadata.create_all(engine)

recommendation_score_map = {
    "Strong Buy": 4,
    "Buy": 2,
    "Hold": 1,
    "Sell": -2,
    "Strong Sell": -4
}

def load (lst, start, end):
    for ticker in lst[start:end]:
        if (index:=ticker.find('.')) != -1:
            ticker = ticker[:index] + '-' + ticker[index+1:]
        #get the data
        try:
            tkr = yf.Ticker(ticker)
            company_info = tkr.info
            beta = company_info.get('beta', 'N/A')
            recommendations = tkr.recommendations;
            
            if recommendations is not None and not recommendations.empty:
                latest = recommendations.iloc[-1]
                grade = latest.get('To Grade', None)
                recommendation_score = recommendation_score_map.get(grade, 0)
                print(recommendations)

            #add data to list
            data_lists.append([ticker, beta, recommendation_score])
        except:
            print("Error retrieving data for ticker: ", ticker)

        try:
            stock_row = StockData(
                ticker=ticker,
                beta=beta,
                recommendation_score=recommendation_score,
                industry=None,
                sub_sector=None
            )
            session.add(stock_row)
            session.commit()
            print("Data added to SQL")
        except Exception as e:
            session.rollback()
            print(f"Error occurred: {e}")
            traceback.print_exc()
        time.sleep(random.uniform(6, 10))

start = 5
end = 7
full_list = scrape_wiki_data.get_tickers()
#print(full_list)
load(full_list, start, end)


# while end <= 500:
    
#     start += 10
#     end += 10
#     time.sleep(random.uniform(1, 3))

stock_data = pd.DataFrame(columns=cols, data=data_lists)
print(stock_data.head())

