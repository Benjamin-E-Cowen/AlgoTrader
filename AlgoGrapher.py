import yfinance as yf
import numpy as np
from matplotlib import pyplot as plt 
from scipy.signal import find_peaks
import scipy as sp
from AlgoTrader import AlgoTrader
import math
from datetime import date as date_d

class AlgoGrapher:
	def plot_rsi(self,d):
		rsi = self.algo_t.get_rsi(d)

		for i in range(d,len(rsi)):
			s  = 4/25 * abs(rsi[i] - 50) + 2
			if rsi[i] <= 30:
				self.ax.plot([i],[self.algo_t.trade_data[i]],  marker='o', markersize=s,color='green')
			elif rsi[i] >= 70:
				self.ax.plot([i],[self.algo_t.trade_data[i]],  marker='o',markersize=s, color='red')
			else:
				self.ax.plot([i],[self.algo_t.trade_data[i]],  marker='o', markersize=s, color='orange')

	def plot_options_action(self,data):
		pass


	def plot_simple_moving_average_range(self,l,d):
		for i in range(l,d):
	 		self.plot_simple_moving_average(i)


	def plot_triple_crossover(self,s,m,l):
		best_balances = self.algo_t.get_triple_crossover_with_simple_moving_averages_profits(s,m,l)
		self.ax.plot(self.algo_t.get_balances(),color='green')
		for i,e in enumerate(self.algo_t.get_actions()):
			if e == 1:
				self.ax.plot([i],[self.algo_t.get_balances()[i]],  marker='o', color='green')
			elif e == -1:
				self.ax.plot([i],[self.algo_t.get_balances()[i]],  marker='o', color='red')
	def plot_double_crossover(self,s,l):
		best_balances = self.algo_t.get_double_crossover_with_simple_moving_averages_profits(s,l)
		self.ax.plot(self.algo_t.get_balances())
		for i,e in enumerate(self.algo_t.get_actions()):
			if e == 1:
				self.ax.plot([i],[self.algo_t.get_balances()[i]],  marker='o', color='green')
			elif e == -1:
				self.ax.plot([i],[self.algo_t.get_balances()[i]],  marker='o', color='red')

	def plot_single_crossover(self,s):
		best_balances = self.algo_t.get_single_crossover_with_simple_moving_averages_profits(s)
		self.ax.plot(self.algo_t.get_balances())
		for i,e in enumerate(self.algo_t.get_actions()):
			if e == 1:
				self.ax.plot([i],[self.algo_t.get_balances()[i]],  marker='o', color='green')
			elif e == -1:
				self.ax.plot([i],[self.algo_t.get_balances()[i]],  marker='o', color='red')

	def plot_bollinger_bands(self,n,d, linewidth=1):
		lower_band = self.algo_t.get_nth_day_lower_bolinger_band_list(n,d)
		upper_band = self.algo_t.get_nth_day_upper_bolinger_band_list(n,d)
		self.ax.plot(range(n,len(lower_band)),lower_band[n:], linewidth = linewidth)
		self.ax.plot(range(n,len(upper_band)),upper_band[n:], linewidth = linewidth)


	def plot_bollinger_bands_crossover(self,n,d):
		self.algo_t.get_bollinger_bands_simple_moving_averages_profits(n,d)
		self.ax.plot(self.algo_t.get_balances())
		for i,e in enumerate(self.algo_t.get_actions()):
			if e == 1:
				self.ax.plot([i],[self.algo_t.get_balances()[i]],  marker='o', color='green')
			elif e == -1:
				self.ax.plot([i],[self.algo_t.get_balances()[i]],  marker='o', color='red')	






	def plot_simple_moving_average(self,n,alpha=0,linewidth=1):
		if not alpha:
			alpha= max((1-self.density_plot_value/(self.density_plot_value-1)) * n + self.density_plot_value/(self.density_plot_value-1),0) 
		self.ax.plot(range(n,len(self.algo_t.get_nth_day_moving_average_list(n))),self.algo_t.get_nth_day_moving_average_list(n)[n:], alpha=alpha,picker=5,linewidth=linewidth)

	def plot_specified_stock_simple(self,stock_name, stock_period):
		self.fig, self.ax = plt.subplots()
		self.stock_period = "1y"
		self.stock_interval = '1d'
		self.number_of_volumes = 5
		self.forcast_constant = 1.3
		self.number_of_peaks = 20
		self.time_frame_increment = .10
		self.density_plot_value = 200
		stock = yf.Ticker(stock_name)
		stock_history = stock.history(period=self.stock_period, interval=self.stock_interval)
		stock_average = [(a + b) / 2 for a,b in zip(stock_history['Open'],stock_history['Close'])] 
		self.algo_t = AlgoTrader(stock_average)
		domain = len(stock_average)
		print(domain)
		if domain > 14:
			self.plot_simple_moving_average_range(1,800)
			self.plot_rsi(14)
			plt.plot(stock_average, color="black", picker=5)
			plt.title(f'{stock_name}')
			plt.show()


	def plot_specified_stock_simple_with_best_single_cross_over_sma(self,stock_name, stock_period):
		self.fig, self.ax = plt.subplots()
		self.stock_period = "1y"
		self.stock_interval = '1d'
		self.number_of_volumes = 5
		self.forcast_constant = 1.3
		self.number_of_peaks = 20
		self.time_frame_increment = .10
		self.density_plot_value = 200
		stock = yf.Ticker(stock_name)
		stock_history = stock.history(period=self.stock_period, interval=self.stock_interval)
		stock_average = [(a + b) / 2 for a,b in zip(stock_history['Open'],stock_history['Close'])] 
		self.algo_t = AlgoTrader(stock_average)


		domain = len(stock_average)
		if domain > 14:
			sma1, sma2 = self.algo_t.get_maximum_double_crossover_with_simple_moving_averages(5,50,5,50)
			print(sma1,sma2)
	
			self.plot_simple_moving_average_range(1,800)
			self.plot_simple_moving_average(sma1, 1,3)
			self.plot_simple_moving_average(sma2, 1,3)

			self.plot_rsi(14)
			plt.plot(stock_average, color="black", picker=5)
			plt.title(f'{stock_name}')
			plt.show()



	def plot_specified_stock_simple_with_best_single_cross_over_sma(self,stock_name, stock_period):
		self.fig, self.ax = plt.subplots()
		self.stock_period = "1y"
		self.stock_interval = '1d'
		self.number_of_volumes = 5
		self.forcast_constant = 1.3
		self.number_of_peaks = 20
		self.time_frame_increment = .10
		self.density_plot_value = 200
		stock = yf.Ticker(stock_name)
		stock_history = stock.history(period=self.stock_period, interval=self.stock_interval)
		stock_average = [(a + b) / 2 for a,b in zip(stock_history['Open'],stock_history['Close'])] 
		self.algo_t = AlgoTrader(stock_average)


		domain = len(stock_average)
		if domain > 14:
			sma1 = self.algo_t.get_maximum_single_crossover_with_simple_moving_averages(5, 100)
			print(sma1)
	
			self.plot_simple_moving_average_range(1,800)
			self.plot_simple_moving_average(sma1, 1,3)
			self.plot_rsi(14)
			plt.plot(stock_average, color="black", picker=5)
			plt.title(f'{stock_name}')
			plt.show()




	def plot_specified_with_maximum_bollinger_bands(self,stock_name, stock_period):
		self.fig, self.ax = plt.subplots()
		self.stock_period = "1y"
		self.stock_interval = '1d'
		self.number_of_volumes = 5
		self.forcast_constant = 1.3
		self.number_of_peaks = 20
		self.time_frame_increment = .10
		self.density_plot_value = 200
		stock = yf.Ticker(stock_name)
		stock_history = stock.history(period=self.stock_period, interval=self.stock_interval)
		stock_average = [(a + b) / 2 for a,b in zip(stock_history['Open'],stock_history['Close'])] 
		self.algo_t = AlgoTrader(stock_average)


		domain = len(stock_average)
		if domain > 14:
			sma1, sd = self.algo_t.get_maximum_bollinger_bands_simple_moving_averages_profits(5, 100, 1, 5, .5)
			print(sma1)
			print(sd)
			self.plot_simple_moving_average_range(1,800)
			self.plot_simple_moving_average(sma1, 1,2)

			self.plot_bollinger_bands(sma1,sd, 1.1)
			self.plot_rsi(14)
			plt.plot(stock_average, color="black", picker=5)
			plt.title(f'{stock_name}')
			plt.show()



	def plot_specified_stock_simple_with_best_single_cross_over_sma_and_bollinger_bands(self,stock_name, stock_period):
		self.fig, self.ax = plt.subplots()
		self.stock_period = "1y"
		self.stock_interval = '1d'
		self.number_of_volumes = 5
		self.forcast_constant = 1.3
		self.number_of_peaks = 20
		self.time_frame_increment = .10
		self.density_plot_value = 200
		stock = yf.Ticker(stock_name)
		stock_history = stock.history(period=self.stock_period, interval=self.stock_interval)
		stock_average = [(a + b) / 2 for a,b in zip(stock_history['Open'],stock_history['Close'])] 
		self.algo_t = AlgoTrader(stock_average)


		domain = len(stock_average)
		if domain > 14:
			sma1 = self.algo_t.get_maximum_single_crossover_with_simple_moving_averages(5, 100)
			print(sma1)
	
			self.plot_simple_moving_average_range(1,800)
			self.plot_simple_moving_average(sma1, 1,3)
			sma1, sd = self.algo_t.get_maximum_bollinger_bands_simple_moving_averages_profits(5, 100, 1, 2, .2)
			print(sma1)
			print(sd)
			self.plot_simple_moving_average(sma1, 1,2)

			self.plot_bollinger_bands(sma1,sd, 1.1)


			self.plot_rsi(14)
			plt.plot(stock_average, color="black", picker=5)
			self.plot_future_option_activity(stock_name)
			plt.title(f'{stock_name}')
			plt.show()

	def plot_future_option_activity(self,stock_name):
		stock = yf.Ticker(stock_name)
		if len(stock.options) > 0:
			stock_history = stock.history(period=self.stock_period, interval=self.stock_interval)
			stock_average = [(a + b) / 2 for a,b in zip(stock_history['Open'],stock_history['Close'])] 
			domain = len(stock_average)
			date_i = list(map(int,stock.options[0].split("-")))
			date_i = date_d(date_i[0],date_i[1],date_i[2])

			for i, date in enumerate(stock.options):
				date_chain = stock.option_chain(date)
				date_j = list(map(int, date.split("-")))
				date_j = date_d(date_j[0],date_j[1],date_j[2])

				v = max(date_chain.calls['volume'])
				max_percent_change = max(date_chain.calls['percentChange'])
				min_percent_change = min(date_chain.calls['percentChange'])
				if ((date_j - date_i).days < 100):
					for r in [ [s,p,v] for s,p,v in zip(
														date_chain.calls['strike'],
														date_chain.calls['percentChange'],
														date_chain.calls['volume']
													 ) 
						if abs(p) > 5 and v > 100]:
						alpha = r[2]/v if r[2]/v == r[2]/v else 0
						if r[1] > 0:
							self.ax.plot([domain + (date_j - date_i).days], r[0] ,marker='o', markersize= r[1]/max_percent_change * 5, alpha= alpha, color='green')
						else: 
							self.ax.plot([domain + (date_j - date_i).days], r[0] ,marker='o', markersize= r[1]/min_percent_change * 5, alpha= alpha , color='red')
				#put stugg
				# for date in stock.options:
				# 	date_chain = stock.option_chain(date)
				# 	v = max(date_chain.puts['volume'])
				# 	max_percent_change = max(date_chain.puts['percentChange'])
				# 	min_percent_change = min(date_chain.puts['percentChange'])

				# 	for r in [ [s,p,v] for s,p,v in zip(
				# 										date_chain.puts['strike'],
				# 										date_chain.puts['percentChange'],
				# 										date_chain.puts['volume']
				# 									 ) 
				# 		if abs(p) > 5 and v > 100]:
				# 		if r[1] > 0:
				# 			self.ax.plot([date], r[0] ,marker='o', markersize= r[1]/max_percent_change * 5, alpha= r[2]/ v , color='red')
				# 		else: 
				# 			self.ax.plot([date], r[0] ,marker='o', markersize= r[1]/min_percent_change * 5, alpha= r[2]/ v , color='green')

	


