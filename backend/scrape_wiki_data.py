import os
import pandas as pd
from sqlalchemy import create_engine

if __name__ == "__main__":
    #get data from wikipedia and store it into a df
    tables = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks')
    df = tables[0]

    # Create SQLAlchemy engine, get password from env var DB_PASSWORD
    password = os.getenv("DB_PASSWORD")
    engine = create_engine(f'mysql+mysqlconnector://root:{password}@localhost/easy_s_and_p')

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