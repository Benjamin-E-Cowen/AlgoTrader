from thousand_tickers import thousand_tickers as td
import yfinance as yf
from AlgoGrapher import AlgoGrapher as AG


import requests

algo_grapher = AG()

def get_hot_tickers():
	r = requests.get("https://www.tradingview.com/markets/stocks-usa/market-movers-active/")
	a = r.text.split("tv-data-table__tbody")[1].split("data-symbol")
	return [s.split(":")[1].split('"')[0] for s in a[1:]]




def volume(ticker):
	print(ticker)
	s = yf.Ticker(ticker)
	if 'averageVolume' in s.info:
		return s.info['averageVolume']
	return -1

#l = sorted(td, key=lambda sn: volume(sn))


for ticker in get_hot_tickers():
	print(ticker)
	algo_grapher.plot_specified_stock_simple_with_best_single_cross_over_sma_and_bollinger_bands(ticker,'1y')

