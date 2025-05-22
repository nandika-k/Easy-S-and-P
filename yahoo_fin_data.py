import yfinance as yf
import scrape_wiki_data
import pandas as pd
import time
import random
 

cols = ['Ticker', 'Industry', 'Sub-Sector', 'Beta', 'Recommendation Score']
data_lists = []

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
            sector = company_info.get('sector', 'N/A')
            industry = company_info.get('industry', 'N/A')
            recommendations = tkr.recommendations;
            
            if recommendations is not None and not recommendations.empty:
                latest = recommendations.iloc[-1]
                grade = latest.get('To Grade', None)
                recommendation_score = recommendation_score_map.get(grade, 0)
                #print(recommendations)
                #recommendation_score = recommendations.iloc[-1]['To Grade']
                #recommendation_score = recommendation_score_map.get(recommendation_score, 0)
            else:
                recommendation_score = 0

            #add data to list
            data_lists.append([ticker, industry, sector, beta, recommendation_score])
        except:
            print("Error retrieving data for ticker: ", ticker)

        time.sleep(random.uniform(6, 10))

start = 0
end = 5
full_list = scrape_wiki_data.get_tickers()
print(full_list)
load(full_list, start, end)

# while end <= 500:
    
#     start += 10
#     end += 10
#     time.sleep(random.uniform(1, 3))

stock_data = pd.DataFrame(columns=cols, data=data_lists)
print(stock_data.head())

