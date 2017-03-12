# CS 122 A News Ment
# 
# Currency and Stock scraper
#
# resrar-jarroyom-ayaspan

from yahoo_finance import Currency, Share
import bs4
import urllib3
import csv
import pandas as pd

def get_historical_stock(start_date, end_date, ticker):
	'''
	Takes stock/index ticker and returns dictionary of dates with adjusted closing prices.

	Inputs:
		start_date, end_date (string): "YYYY-MM-DD"
		ticker (string): Ticker string i.e. "AAPL", "^SP500"

	Output:
		close_dict (dict): dict of dates mapped to adjusted closing prices
	'''
	date_series = pd.date_range(start_date, end_date, freq="D")
	date_range = pd.Series(date_series.format())

	stock = Share(ticker)
	value_list = stock.get_historical(start_date, end_date)

	historical_dict = {}
	for day in date_range:
		historical_dict[day] = 0
	for value in value_list:
		historical_dict[value["Date"]] = value["Adj_Close"]

	df = pd.DataFrame.from_dict(historical_dict, orient = "index")
	df = df[0].replace(to_replace = 0, method = "ffill")
	
	dict_for_sql = {}
	for k, v in df.to_dict().items():
		dict_for_sql[k] = (v, ticker)

	return dict_for_sql

def get_exchange_rate(date, home, foreign):
	'''
	Takes string of date formatted "YYYY-MM-DD" and returns USD to currency exchange rate.

	Inputs:
		date (string): "YYYY-MM-DD"
		home (string): reference currency i.e. USD, EUR, etc
		foreign (string): exchange currency i.e. MXN, AUS, etc
	
	Output:
		t.text (string): exchange rate for given day
	'''
	pm = urllib3.PoolManager()
	url = "http://www.x-rates.com/historical/?from=USD&amount=1&date=" + date
	html = pm.urlopen(url=url, method="GET").data
	soup = bs4.BeautifulSoup(html, "html5lib")
	tags = soup.find_all("td", "a", class_="rtRates")

	for t in tags:
		if t.a["href"] == "/graph/?from=" + home + "&to=" + foreign:
			return t.text

def get_historical_currency(start_date, end_date, home, foreign):
	'''
	Gets a historical dictionary that maps dates to exchange rate for two currencies.

	Inputs:
		start_date, end_date (string): "YYYY-MM-DD"
		home (string): reference currency i.e. USD, EUR, etc
		foreign (string): exchange currency i.e. MXN, AUS, etc

	Output: 
		historical_dict (dict): dict of dates mapped to closing exchange rates 
	'''
	date_series = pd.date_range(start_date, end_date, freq="D")
	date_range = pd.Series(date_series.format())

	historical_dict = {}
	for day in date_range:
		historical_dict[day] = 0
	for i in range(len(date_range)):
		val = get_exchange_rate(date_range[i], home, foreign)
		if val:
			historical_dict[date_range[i]] = float(val)

	df = pd.DataFrame.from_dict(historical_dict, orient = "index")
	df = df[0].replace(to_replace = 0, method = "ffill")
	
	dict_for_sql = {}
	for k, v in df.to_dict().items():
		dict_for_sql[k] = (v, foreign)

	return dict_for_sql
	
def stock_dict_to_csv(in_dict, filename):
	'''
	Given a dictionary and output filename, write the dictionary into a csv file.

    Inputs:
        in_dict (dictionary)
        filename (string)

    Output:
        CSV file
	'''
	with open(filename, 'w') as csv_file:
		fieldnames = ["date", "adj_close_price", "ticker"]
		writer = csv.writer(csv_file)
		writer.writerow(fieldnames)
		for key, value in sorted(in_dict.items()):
			writer.writerow([key, value[0], value[1]])

def currency_dict_to_csv(in_dict, filename):
	'''
	Given a dictionary and output filename, write the dictionary into a csv file.

    Inputs:
        in_dict (dictionary)
        filename (string)

    Output:
        CSV file
    '''
	with open(filename, 'w') as csv_file:
		fieldnames = ["date", "exchange_rate", "peso"]
		writer = csv.writer(csv_file)
		writer.writerow(fieldnames)
		for key, value in sorted(in_dict.items()):
			writer.writerow([key, value[0], value[1]])

if __name__ == "__main__":
	
	start_date = "2008-04-01"
	end_date = "2013-04-01"

	tickers = ["^IXIC", "F", "BA", "^MXX"]
	files = ["nasdaq_ticker.csv", "ford_ticker.csv", "boeing_ticker.csv", "ipc_ticker.csv"]

	for i in range(len(tickers)):
		d = get_historical_stock(start_date, end_date, tickers[i])
		stock_dict_to_csv(d, files[i])

