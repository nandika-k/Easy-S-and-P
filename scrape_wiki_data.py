import os
import pandas as pd
from sqlalchemy import create_engine
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import certifi
import json
import ssl

#Code from Financial Modeling Prep
def get_jsonparsed_data(url):
    context = ssl.create_default_context(cafile=certifi.where())

    # Add User-Agent header to mimic a browser
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = Request(url, headers=headers)

    try:
        response = urlopen(req, context=context)
        data = response.read().decode("utf-8")
    except HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}")
    except URLError as e:
        print(f"URL Error: {e.reason}")
    except Exception as e:
        print(f"General error: {e}")
    return None

if __name__ == "__main__":
    #get data from Financial Modeling Prep and store into json_data
    FMP_api_key = os.getenv("FMP_API_KEY")
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