import os
import pandas as pd
from sqlalchemy import create_engine
from urllib.request import urlopen
import certifi
import json

#Code from Financial Modeling Prep
def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

if __name__ == "__main__":
    #get data from Financial Modeling Prep and store into json_data
    FMP_api_key = os.getenv("FMPI_API_KEY")
    url = ("https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={FMP_api_key}}")
    json_data = get_jsonparsed_data(url)

    #Store the data as a data frame
    df = pd.DataFrame(json_data)

    # Create SQLAlchemy engine, get password from env var DB_PASSWORD
    password = os.getenv("DB_PASSWORD")
    engine = create_engine('mysql+mysqlconnector://root:{password}@127.0.0.1/easy_s_and_p')

    try:
        #load dataframe into an sql table called stocks
        df.to_sql('stocks', con=engine, if_exists='replace', index=False)
        print("Data written successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        engine.dispose()


def update_stock_csv():
    #store to csv file without indexing
    df.to_csv('data/stocks.csv', index=False)

def get_tickers():
    #Returns a list of all the tickers stored
    return df['Symbol'].tolist()

def get_details():
    #returns a list of lists for each row
    return df[['Symbol', 'GICS Sector', 'GICS Sub-Industry']].values.tolist()