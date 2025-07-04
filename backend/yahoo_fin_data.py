import yfinance as yf
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import traceback
import os


password = os.getenv("DB_PASSWORD")
engine = create_engine(f'mysql+mysqlconnector://root:{password}@localhost/easy_s_and_p')

def get_tickers():
    #read tickers from sql table created by scrape_wiki_data
    df = pd.read_sql('SELECT Ticker FROM WIKI_DATA', con=engine)
    return df['Ticker'].to_list()

def calc_rec_score(recommendations):
    latest = recommendations.iloc[-1]

    strong_buy = latest.get("strongBuy", 0)
    buy = latest.get("buy", 0)
    hold = latest.get("hold", 0)
    sell = latest.get("sell", 0)
    strong_sell = latest.get("strongSell", 0)

    total_analysts = strong_buy + buy + hold + sell + strong_sell;

    recommendation_score = (
        2 * strong_buy
        + 1 * buy
        + 0 * hold
        - 1 * sell
        - 2 * strong_sell
    ) / total_analysts

    #log ensures more popular companies aren't unfairly given high scores
    #dividing by 3 ensures the confidence level isn't too high for a few number
    #of analysts
    confidence = min(1, np.log1p(total_analysts) / 3)

    score = confidence * recommendation_score * 100
    print(score)
    return score

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
            recommendation_score = calc_rec_score(recommendations)
        else:
            recommendation_score = None

        #return a dictionary of the ticker, beta, and recommendation score
        return {
            "Ticker": ticker,
            "Beta" : beta,
            "Recommendation_Score": recommendation_score
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
    for ticker in tickers[0:503]:
        data = fetch_data(ticker)

        if data:
            all_data.append(data)
            print("Fetched data for ticker", ticker)

    #load into pandas dataframe
    df = pd.DataFrame(all_data, columns=["Ticker", "Beta", "Recommendation_Score"])

    #clean up data types
    df["Ticker"] = df["Ticker"].astype(str)
    df["Beta"] = pd.to_numeric(df['Beta'], errors='coerce').astype(float)
    df["Recommendation_Score"] = pd.to_numeric(df['Recommendation_Score'], errors='coerce').fillna(0).astype(int)

    try:
        #load dataframe into an sql table called y_fin_data
        df.to_sql('yahoo_fin_data', con=engine, if_exists='append', index=False)
        print("Data written successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        engine.dispose()

main()