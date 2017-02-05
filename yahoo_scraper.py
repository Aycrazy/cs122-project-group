# CS 122 A News Ment
# 
# Yahoo Finance Scraper
#
# resrar-jarroyom-ayaspan

from yahoo_finance import Currency, Share

def get_currency_rate(t0, t1 = None):
	'''
	'''
	t0 = t0.upper()
	if not t1:
		ticker = Currency(t0)
		return ticker.get_rate()
	else:
		t1 = t1.upper()
		ticker = Currency(t0 + t1)
		return ticker.get_rate()

def get_historical_stock(ticker, start_date, end_date):
	'''
	'''
	stock = Share(ticker)
	lst = stock.get_historical(start_date, end_date)

	close_dict = {}
	for dic in lst:
		close_dict[dic["Date"]] = dic["Adj_Close"]

	return close_dict





