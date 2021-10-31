
import numpy as np

class AlgoTrader:
	trade_data = 0
	domain = 0
	balances = []


	def __init__(self, trade_data):
		self.trade_data = trade_data
		self.domain = len(trade_data) 

	def double_crossover_profits(self, smaller_moving_average_list, larger_moving_average_list, smaller_moving_average_degree, larger_moving_average_degree):
		balance = 0
		self.balances = [0 for _ in range(larger_moving_average_degree)]
		self.actions = [0 for _ in range(larger_moving_average_degree)]
		purchased = False
		starting_day = larger_moving_average_degree
		
		today_buy_signal, yesterday_buy_signal= False, False
		for day in range(starting_day+1,len(larger_moving_average_list)):
			self.actions.append(0)
			yesterday_buy_signal = today_buy_signal;
			today_buy_signal = smaller_moving_average_list[day-1] > larger_moving_average_list[day-1] 
			if today_buy_signal != yesterday_buy_signal:
				if (today_buy_signal):
					balance -= self.trade_data[day]
					purchased = True
					self.actions[-1] = 1
				elif purchased:
					balance += self.trade_data[day]
					purchased = False
					self.actions[-1] = -1
			if purchased:
				self.balances.append(balance + self.trade_data[day])	
			else:
				self.balances.append(balance)	
		if purchased:
			#print(balance+ self.trade_data[-1])
			return balance + self.trade_data[-1]
		#print(balance)
		return balance

	def triple_crossover_profits(self, small_moving_average_list, medium_moving_average_list, large_moving_average_list,small_moving_average_degree,medium_moving_average_degree,large_moving_average_degree):
		balance = 0
		self.balances = [0 for _ in range(large_moving_average_degree)]
		self.actions = [0 for _ in range(large_moving_average_degree)]
		starting_day = large_moving_average_degree
		purchased = False

		for day in range(starting_day+1,len(large_moving_average_list)):
			self.actions.append(0)
			#buy signal
			if not purchased and small_moving_average_list[day-1] > large_moving_average_list[day-1] and small_moving_average_list[day-1] > medium_moving_average_list[day-1]:
				purchased = True
				balance -= self.trade_data[day]
				self.actions[-1] = 1
			if purchased and small_moving_average_list[day-1] < large_moving_average_list[day-1] and small_moving_average_list[day-1] < medium_moving_average_list[day-1]:
				balance += self.trade_data[day]
				purchased = False	
				self.actions[-1] = -1
			if purchased:
				self.balances.append(balance + self.trade_data[day-1])	
			else:
				self.balances.append(balance)	
		if purchased:
			#print(balance+ self.trade_data[-1])
			return balance + self.trade_data[-1]
		#print(balance)
		return balance

	def get_maximum_single_crossover_with_simple_moving_averages(self, minimum_moving_average_degree, maximum_moving_average_degree):
		return max(range(minimum_moving_average_degree,maximum_moving_average_degree), key=lambda moving_average_degree: self.get_single_crossover_with_simple_moving_averages_profits(moving_average_degree))


	def bollinger_bands_simple_moving_averages_profits(self, moving_average_list,moving_average_degree, d):
		balance = 0
		self.balances = [0 for _ in range(moving_average_degree)]
		self.actions = [0 for _ in range(moving_average_degree)]
		starting_day = moving_average_degree
		purchased = False
		lower_band = self.get_nth_day_lower_bolinger_band_list(moving_average_degree,d)
		upper_band = self.get_nth_day_upper_bolinger_band_list(moving_average_degree,d)

		lower_band_trigger = False
		center_band_trigger = False
		upper_band_trigger = False
		was_greater_than_lower_band = True
		was_greater_than_center_band = False
		was_greater_than_upper_band = False


		for day in range(starting_day+1,len(moving_average_list)):
			self.actions.append(0)
			if not was_greater_than_lower_band:
				lower_band_trigger = self.trade_data[day-1] > lower_band[day-1]
			if not was_greater_than_center_band:
				center_band_trigger = self.trade_data[day-1] > moving_average_list[day-1]
			if was_greater_than_upper_band:
				upper_band_trigger = self.trade_data[day-1] < upper_band[day-1]




			if center_band_trigger and lower_band_trigger and not purchased:
				self.actions[-1] = 1
				purchased = True
				center_band_trigger = False
				lower_band_trigger = False
				upper_band_trigger = False
				balance -= self.trade_data[day]
			if  upper_band_trigger and purchased:
				self.actions[-1] = -1
				purchased = False
				upper_band_trigger = False
				balance += self.trade_data[day]

			was_greater_than_lower_band = self.trade_data[day-1] > lower_band[day-1]
			was_greater_than_center_band = self.trade_data[day-1] > moving_average_list[day-1]
			was_greater_than_upper_band = self.trade_data[day-1] > upper_band[day-1]
			#buy signal
			
			if purchased:
				self.balances.append(balance + self.trade_data[day])	
			else:
				self.balances.append(balance)	
		if purchased:
			#print(balance+ self.trade_data[-1])
			return balance + self.trade_data[-1]
		#print(balance)
		return balance



	def get_rsi(self, days):
		rsi_values = [0 for _ in range(days)]
		daily_gains = [self.trade_data[i] - self.trade_data[i-1] if self.trade_data[i] - self.trade_data[i-1] > 0 else 0 for i in range(1,self.domain) ]
		avg_gains = [sum(daily_gains[0:days])/days]
		for e in daily_gains[days:]:
			avg_gains.append(((days-1) * avg_gains[-1] + e)/(days))
		daily_losses = [abs(self.trade_data[i] - self.trade_data[i-1]) if self.trade_data[i] - self.trade_data[i-1] < 0 else 0 for i in range(1,self.domain)]
		avg_losses = [sum(daily_losses[0:days])/days]
		for e in daily_losses[days:]:
			avg_losses.append(((days-1) * avg_losses[-1] + e)/(days))
		return rsi_values + [100 - 100/(1 + a_g / a_l) if a_l else 0 for a_g, a_l in zip(avg_gains,avg_losses)]



	def get_single_crossover_with_simple_moving_averages_profits(self,moving_average_degree):
		return self.double_crossover_profits(self.trade_data, self.get_nth_day_moving_average_list(moving_average_degree),0,moving_average_degree)

	def get_double_crossover_with_simple_moving_averages_profits(self, smaller_moving_average_degree, larger_moving_average_degree):
		return self.double_crossover_profits(self.get_nth_day_moving_average_list(smaller_moving_average_degree), self.get_nth_day_moving_average_list(larger_moving_average_degree), smaller_moving_average_degree, larger_moving_average_degree)


	def get_triple_crossover_with_simple_moving_averages_profits(self, small_moving_average_degree, medium_moving_average_degree,large_moving_average_degree):
		return self.triple_crossover_profits(self.get_nth_day_moving_average_list(small_moving_average_degree),self.get_nth_day_moving_average_list(medium_moving_average_degree) ,self.get_nth_day_moving_average_list(large_moving_average_degree), small_moving_average_degree, medium_moving_average_degree, large_moving_average_degree)


	def get_maximum_double_crossover_with_simple_moving_averages(self, minimum_smaller_moving_average_degree, maximum_smaller_moving_average_degree, minimum_larger_moving_average_degree, maximum_larger_moving_average_degree):
		moving_average_combinations = []
		for larger_moving_average_degree in range(minimum_larger_moving_average_degree, maximum_larger_moving_average_degree + 1):
			for smaller_moving_average_degree in range(minimum_smaller_moving_average_degree, min(maximum_smaller_moving_average_degree + 1,larger_moving_average_degree)):
				moving_average_combinations.append([smaller_moving_average_degree,larger_moving_average_degree])
		#print(moving_average_combinations)
		return max(moving_average_combinations, key=lambda moving_average_combination: self.get_double_crossover_with_simple_moving_averages_profits(moving_average_combination[0],moving_average_combination[1]))
	
	def get_nth_day_moving_average_list(self,n):
		return [0 for _ in range(n)] + [sum(self.trade_data[i-n:i])/n for i in range(n,len(self.trade_data))]

	def get_nth_day_standard_deviations_list(self,n):
		return [0 for _ in range(n)] + [np.std(self.trade_data[i-n:i]) for i in range(n,len(self.trade_data))]

	def get_nth_day_lower_bolinger_band_list(self,n,d):
			deviation_list = self.get_nth_day_standard_deviations_list(n)
			simple_moving_average = self.get_nth_day_moving_average_list(n)
			return [mean - d * std for mean,std in zip(simple_moving_average,deviation_list)]
	def get_nth_day_upper_bolinger_band_list(self,n,d):
			deviation_list = self.get_nth_day_standard_deviations_list(n)
			simple_moving_average = self.get_nth_day_moving_average_list(n)
			return [mean + d * std for mean,std in zip(simple_moving_average,deviation_list)]


	def get_bollinger_bands_simple_moving_averages_profits(self,moving_average_degree,d):
		return self.bollinger_bands_simple_moving_averages_profits(self.get_nth_day_moving_average_list(moving_average_degree), moving_average_degree,d)
	def get_maximum_triple_crossover_with_simple_moving_averages(self, minimum_smaller_moving_average_degree, maximum_smaller_moving_average_degree, minimum_medium_moving_average_degree, maximum_medium_moving_average_degree, minimum_larger_moving_average_degree, maximum_larger_moving_average_degree):
		moving_average_combinations = []
		for larger_moving_average_degree in range(minimum_larger_moving_average_degree, maximum_larger_moving_average_degree + 1):
			for medium_moving_average_degree in range(minimum_medium_moving_average_degree, min(maximum_medium_moving_average_degree + 1, larger_moving_average_degree)):
				for smaller_moving_average_degree in range(minimum_smaller_moving_average_degree, min(maximum_smaller_moving_average_degree + 1,medium_moving_average_degree)):
					moving_average_combinations.append([smaller_moving_average_degree,medium_moving_average_degree,larger_moving_average_degree])
		#print(moving_average_combinations)
		return max(moving_average_combinations, key=lambda moving_average_combination: self.triple_crossover_profits(self.get_nth_day_moving_average_list(moving_average_combination[0]),self.get_nth_day_moving_average_list(moving_average_combination[1]) ,self.get_nth_day_moving_average_list(moving_average_combination[2]), moving_average_combination[0], moving_average_combination[1], moving_average_combination[2]))


	def get_maximum_bollinger_bands_simple_moving_averages_profits(self,minimum_moving_average_degree, maximum_moving_average_degree, minimum_standard_deviation, maximum_standard_deviation, standard_deviation_inc):
		bollinger_bands_combinations = []
		for moving_average_degree in range(minimum_moving_average_degree,maximum_moving_average_degree+1):
			for std in np.arange(minimum_standard_deviation, maximum_standard_deviation, standard_deviation_inc):
					bollinger_bands_combinations.append([moving_average_degree, std])
		return max(bollinger_bands_combinations, key=lambda c: self.bollinger_bands_simple_moving_averages_profits(self.get_nth_day_moving_average_list(c[0]), c[0], c[1]))

	def get_balances(self):
		return self.balances

	def get_actions(self):
		return self.actions




