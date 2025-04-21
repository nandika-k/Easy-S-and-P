import pandas as pd
#had to download lxml module for read_html

#read all the tables from the page and store the first one in df
tables = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks')
df = tables[0]

#testing shows it reads it correctly
#print(df['Symbol'].tolist())

#store to csv file without indexing
#df.to_csv('data/stocks.csv', index=False)