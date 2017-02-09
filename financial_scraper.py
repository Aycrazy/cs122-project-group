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
import datetime as dt

def get_historical_stock(start_date, end_date, ticker):
	'''
	Takes stock/index ticker and returns dictionary of dates with adjusted closing prices.

	Inputs:
		start_date, end_date (string): "YYYY-MM-DD"
		ticker (string): Ticker string i.e. "AAPL", "^SP500"

	Output:
		close_dict (dict): dict of dates mapped to adjusted closing prices
	'''
	stock = Share(ticker)
	lst = stock.get_historical(start_date, end_date)

	close_dict = {}
	for dic in lst:
		close_dict[dic["Date"]] = dic["Adj_Close"]

	return close_dict

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
	for i in range(len(date_range)):
		val = get_exchange_rate(date_range[i], home, foreign)
		if val:
			historical_dict[date_range[i]] = float(val)

	return historical_dict

def dict_to_csv(in_dict, filename):
	'''
	Given a dictionary and output filename, write the dictionary into a csv file.

    Inputs:
        in_dict (dictionary)
        filename (string)

    Output:
        CSV file
	'''
	with open(filename, 'w') as csv_file:
		writer = csv.writer(csv_file, delimiter = ",")
		for key, val in sorted(in_dict.items()):
			writer.writerow([key, val])






