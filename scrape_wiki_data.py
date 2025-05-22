import pandas as pd
from sqlalchemy import create_engine
#had to download lxml module for read_html

#read all the tables from the page and store the first one in df
tables = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks')
df = tables[0]

#testing shows it reads it correctly
#print(df['Symbol'].tolist())

# Create SQLAlchemy engine
engine = create_engine('mysql+mysqlconnector://root:Database23!@127.0.0.1/fin_data_project')

try:
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
    return df['Symbol'].tolist()

def get_details():
    return df[['Symbol', 'GICS Sector', 'GICS Sub-Industry']].tolist()