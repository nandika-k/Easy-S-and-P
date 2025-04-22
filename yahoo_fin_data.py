import yfinance as yf
import scrape_wiki_data

cols = ['Ticker', 'Industry', 'Sub-Sector', 'Beta', 'Recommendation Score']
data_lists = []

for ticker in scrape_wiki_data.get_tickers():
    #get the data
    company_info = yf.Ticker(ticker)
    beta = company_info.info.get('beta')
    recommendations = company_info.get_recommendations();
    print(ticker,beta, "\n", recommendations)

    #add data to list
    data_lists.append([ticker, beta, rec_score])

stock_data = pd.DataFrame(columns=cols)