import yfinance as yf
from sqlalchemy import create_engine
import pandas as pd
import time
import random
import traceback
import os


password = os.getenv("DB_PASSWORD")
engine = create_engine(f'mysql+mysqlconnector://root:{password}@localhost/easy_s_and_p')

recommendation_score_map = {
    "Strong Buy": 4,
    "Buy": 2,
    "Hold": 1,
    "Sell": -2,
    "Strong Sell": -4
}

def get_tickers():
    #read tickers from sql table created by scrape_wiki_data
    df = pd.read_sql('SELECT Symbol FROM stocks', con=engine)
    return df['Symbol'].to_list()

def fetch_data(ticker):
    #Clean up names for any tickers with dots
    if (index:=ticker.find('.')) != -1:
            ticker = ticker[:index] + '-' + ticker[index+1:]
    
    #get the data
    try:
        tkr = yf.Ticker(ticker)
        company_info = tkr.info

        #get beta
        beta = company_info.get('beta', 'N/A')

        #get recommendations
        recommendations = tkr.recommendations;
            
        #compute recommendation score based on analyst recommendations
        if recommendations is not None and not recommendations.empty:
            latest = recommendations.iloc[-1]
            grade = latest.get('To Grade', None)
            recommendation_score = recommendation_score_map.get(grade, 0)
            print(recommendations)
        else:
            recommendation_score = None

        #return a list of the ticker, beta, and recommendation score
        return {
            "Ticker": ticker,
            "Beta" : beta,
            "Recommendation Score": recommendation_score
        }
    except:
        #if there is an error, provide the details
        print("Error retrieving data for ticker: ", ticker)
        traceback.print_exc()
        return None

        

def main():
    #get list of tickers
    tickers = get_tickers()
    
    #create list to store all the data lists
    all_data = []
    
    #smaller amount for testing
    
    '''
    iterate through tickers and fetch the data on all
    if data is found, append list to all_data
    '''
    for ticker in tickers[0:5]:
        data = fetch_data(ticker)

        if data:
            all_data.append(data)
            print("Fetched data for ticker", ticker)

    #load into pandas dataframe
    df = pd.DataFrame(all_data)

    try:
        #load dataframe into an sql table called y_fin_data
        df.to_sql('y_fin_data', con=engine, if_exists='replace', index=False)
        print("Data written successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        engine.dispose()

main()