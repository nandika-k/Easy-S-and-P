import yfinance as yahoo_finance
import scrape_wiki_data as wiki_data

for ticker in wiki_data.df.columns[0]:
    company_info = yahoo_finance.Ticker(ticker)
    beta = company_info.info['beta']