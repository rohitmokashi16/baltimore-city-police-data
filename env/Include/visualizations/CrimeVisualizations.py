import matplotlib.pyplot as plt
import seaborn as sns
import io
from Include.sample.Preprocessing import Preprocessing
import base64


class CrimeVisualizations:

	def __init__(self, prepros_obj):
		"""Initializes a few variables that are used multiple times across different functions."""

		self.day_of_the_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
		self.months_of_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		self.lower_year = 1950
		self.upper_year = 2021
		self.dataset_obj = prepros_obj

	def dataset_updater(self, lower, upper):
		"""Checks if the lower and upper years of the visualization are the same as the existing dataset filters.
		If not, then it updates the dataset by running a new SQL query on the database.
		lower: integer, lower bound of year
		upper: integer, upper bound of year
		"""
		if self.year_bound_checker(lower, upper):
			self.dataset_obj.dataset_read(self.lower_year, self.upper_year)
			self.dataset_obj.dataset_all_updations()
			print("Dataset updated.")
	
	def year_bound_checker(self, lower, upper):
		"""Checks if the year range is the same as the existing range or not.
		If not, then updates the class variables.
		lower: integer, lower bound of year
		upper: integer, upper bound of year		
		"""

		flag = False
		if self.lower_year != lower or self.upper_year != upper:
			self.lower_year, self.upper_year = lower, upper
			flag = True
		
		return flag

	def seaborn_plot_settings(self):
		"""Default seaborn plot settings."""

		sns.set_style()
		sns.set_context("notebook")
		# sns.set(rc={'figure.figsize':(30, 10)})
		sns.set(font_scale = 1.25)

	def day_of_the_week_boxplot(self, groupby = "Year", lower_year = 2016, upper_year = 2020, is_swarm = False, *neighborhood_name):
		"""Generates boxplots for total incidents across different days of the week.
		dataset: pandas DataFrame object
		groupby: column name to group the dataset by (Year (default) or Month_Name)
		lower_year: lower bound for year filter
		upper_year: upper bound for year filter
		is_swarm: flag to enable or disable swarmplot (Boolean)
		*neighborhood_name: contains name of ONE neighborhood (string as first and only element of tuple)"""

		if groupby is None:
			groupby = "Year"

		# Activate figure and update settings
		fig = plt.figure(figsize=(20, 10))
		self.seaborn_plot_settings()

		# Update dataset based on year filters
		self.dataset_updater(lower_year, upper_year)
		dataset = self.dataset_obj.final_dataset[['Year', 'Month_Name', 'Total_Incidents', 'Day', 'Neighborhood']]

		# Check for Neighborhood filter and filter dataset and set title accordingly
		neighborhood_title_string = ''
		if len(neighborhood_name) > 0:
			dataset = dataset[dataset['Neighborhood'] == neighborhood_name[0].upper()]
			neighborhood_title_string = f" for neighborhood {neighborhood_name[0]}"
		title = "Incidents by Day of the Week grouped by " + ("month" if groupby.lower() == 'month_name' else "year") + neighborhood_title_string

		# Group by Day
		tp = dataset.groupby(by = ["Day", groupby]).count().reset_index()

		# Check if Swarmplot is enabled
		if is_swarm:
			# Check for month or year grouping and set hue and title accordingly
			if groupby.lower() == "month_name":
				sns.swarmplot(x = "Total_Incidents", y = "Day", data = tp, hue = groupby, order = self.day_of_the_week, size = 7, hue_order = self.months_of_year)
			else:
				sns.swarmplot(x = "Total_Incidents", y = "Day", data = tp, hue = groupby, order = self.day_of_the_week, size = 7)
			title = title + " with swarmplot of " + ("month" if groupby.lower() == 'month_name' else "year")
		
		# Generate boxplot and set labels
		bx_plt = sns.boxplot(x = "Total_Incidents", y = "Day", data = tp, order = self.day_of_the_week)
		bx_plt.set_ylabel("Day of the week", fontsize = 15)
		bx_plt.set_xlabel("Total Incidents", fontsize = 15)
		bx_plt.set_title(title)
		string_bytes = io.BytesIO()
		plt.savefig(string_bytes, format='jpg')
		string_bytes.seek(0)
		plot_base64data = base64.b64encode(string_bytes.read())
		return plot_base64data

	def district_wise_boxplot(self, groupby = "Year", lower_year = 2016, upper_year = 2020, is_swarm = False):
		"""Generates boxplots for total incidents across different districts.
		dataset: pandas DataFrame object
		groupby: column name to group the dataset by (Year (default) or Month_Name)
		lower_year: lower bound for year filter
		upper_year: upper bound for year filter
		is_swarm: flag to enable or disable swarmplot (Boolean)"""

		# Activate figure and update settings
		fig = plt.figure(figsize=(20, 10))
		self.seaborn_plot_settings()

		# Update dataset based on year filters, group the dataset, and create title string
		self.dataset_updater(lower_year, upper_year)
		dataset = self.dataset_obj.final_dataset[['Year', 'Month_Name', 'Total_Incidents', 'District']]
		grouping = "Month" if groupby.lower() == 'month_name' else 'year'
		title = f"Incidents by District grouped by {grouping}"

		# Group by District
		tp = dataset.groupby(by = ["District", groupby]).count().reset_index()

		# Check if Swarmplot is enabled
		if is_swarm:
			# Check for month or year grouping and set hue and title accordingly
			if groupby.lower() == "month_name":
				sns.swarmplot(x = "Total_Incidents", y = "District", data = tp, hue = groupby, size = 7, hue_order = self.months_of_year)
			else:
				sns.swarmplot(x = "Total_Incidents", y = "District", data = tp, hue = groupby, size = 7)
			title = title + " with swarmplot of " + grouping
		
		# Generate boxplot and set labels
		bx_plt = sns.boxplot(x = "Total_Incidents", y = "District", data = tp)
		bx_plt.set_ylabel("District", fontsize = 15)
		bx_plt.set_xlabel("Total Incidents", fontsize = 15)
		bx_plt.set_title(title)
		string_bytes = io.BytesIO()
		plt.savefig(string_bytes, format='jpg')
		string_bytes.seek(0)
		plot_base64data = base64.b64encode(string_bytes.read())
		return plot_base64data

	def indoor_outdoor_crimes_trends(self, groupby = "Year", lower_year = 2016, upper_year = 2020, *neighborhood_name):
		"""Generates line graphs for inside/outside crimes for different time groupings.
		dataset: pandas DataFrame object
		groupby: column name to group the dataset by (Year (default) or Month_Name)
		lower_year: lower bound for year filter
		upper_year: upper bound for year filter
		*neighborhood_name: contains name of ONE neighborhood (string as first and only element of tuple)"""
		if groupby.lower() == 'month_name': 
			groupby = 'month_number'
		# Activate figure and update settings
		fig = plt.figure(figsize=(30, 10))
		self.seaborn_plot_settings()
		# Update dataset based on year filters
		self.dataset_updater(lower_year, upper_year)
		dataset = self.dataset_obj.final_dataset[['Year', 'Month_Number','WeekNumber', 'Total_Incidents', 'Inside_Outside', 'Neighborhood']]

		# Check for Neighborhood filter and filter dataset and set title accordingly
		neighborhood_title_string = ''
		if len(neighborhood_name) > 0:
			# print(neighborhood_name[0])
			dataset = dataset[dataset['Neighborhood'] == neighborhood_name[0].upper()]
			neighborhood_title_string = f" for neighborhood {neighborhood_name[0]}"
		# print(dataset.head())

		# Group by Inside_Outside
		tp = dataset.groupby(by = [groupby, 'Inside_Outside']).count().reset_index()
		
		# Generate lineplot
		ax = sns.lineplot(x = groupby, y='Total_Incidents', data = tp, hue = "Inside_Outside", sort = False)
		fontsz = 15

		# Check grouping to set labels
		if groupby.lower() == 'year':
			# Year grouping
			ax.set_xlabel("Year", fontsize = 15)
			grouping = 'year'
			plt.xticks([i for i in range(lower_year, upper_year + 1)])
			# ax.set_xticks(range(0, upper_year - lower_year + 0))
			# ax.set_xticklabels([i for i in range(lower_year, upper_year + 1)], size = fontsz)
		else:
			if groupby.lower() == 'month_number':
				# Month grouping
				upper, labels, grouping = 13, self.months_of_year, "Month"
			else:
				# Week number grouping
				upper, labels, grouping, fontsz = 54, [i for i in range(1, 54)], "Week Number", 10
			# Set the number of ticks and labels
			ax.set_xticks(range(1, upper))
			ax.set_xticklabels(labels, size = fontsz)
			ax.set_xlabel(grouping, fontsize = 15)
		
		# Updating y-axis settings
		ax.set_ylim([tp['Total_Incidents'].min()//2, tp['Total_Incidents'].max()*1.25])
		ax.set_ylabel("Total Incidents", fontsize = 15)
		ax.set_title(f"Trends of Indoors and Outdoors Crimes by {grouping}{neighborhood_title_string}")
		string_bytes = io.BytesIO()
		plt.savefig(string_bytes, format='jpg')
		string_bytes.seek(0)
		plot_base64data = base64.b64encode(string_bytes.read())
		return plot_base64data

	def district_crime_bar_charts(self, lower_year = 2016, upper_year = 2020, inside_outside_flag = False):
		"""Generates bar charts and stacked bar charts for crimewise incident totals.
		dataset: pandas DataFrame object
		lower_year: lower bound for year filter
		upper_year: upper bound for year filter
		inside_outside_flag: if True, generates a stacked bar chart instead of a normal horizontal chart"""

		# Activate figure and update settings
		fig = plt.figure(figsize=(20, 10))
		self.seaborn_plot_settings()

		# Update dataset based on year filters
		self.dataset_updater(lower_year, upper_year)
		dataset = self.dataset_obj.final_dataset[['District', 'Total_Incidents', 'Inside_Outside', 'Year']]

		# Check if inside and outside data needs to be presented
		if not inside_outside_flag:
			# Generates non-stacked horizontal bar chart
			tp = dataset.groupby(by = ["District"]).count().reset_index()
			ax = sns.barplot(data = tp, x = "Total_Incidents", y = 'District', order = tp.sort_values("Total_Incidents", ascending = True).District)
			ax.set_ylabel("District", fontsize = 15)
			ax.set_xlabel("Incident Count", fontsize = 15)
			ax.set_title("Bar Chart of Incident Count by Districts")
		else:
			# Generates horizontal stacked bar chart
			tp = dataset.groupby(by = ["District", "Inside_Outside"]).count().reset_index()
			tp1 = tp.groupby(['District']).sum().sort_values(['Total_Incidents'], ascending = False).reset_index()
			sort_order = {i: 0 for i in tp1['District'].unique()}
			val = 0
			for i in sort_order.keys():
				sort_order[i] = val
				val += 1
			tp = tp.assign(sort = lambda tp: tp['District'].map(sort_order)).sort_values('sort').drop('sort', axis = 1)
			b1 = plt.barh(tp['District'].unique(), tp.loc[tp['Inside_Outside'] == 'Outside', 'Total_Incidents'])
			b2 = plt.barh(tp['District'].unique(), tp.loc[tp['Inside_Outside'] == 'Inside', 'Total_Incidents'], left = tp.loc[tp['Inside_Outside'] == 'Outside', 'Total_Incidents'])
			plt.legend([b1, b2], ["Outside", "Inside"], title = "Crime Setting", loc= "upper right")
			plt.xlabel("District")
			plt.ylabel("Incident Count")
			plt.title("Stacked Bar Chart of Incident Count by Districts broken into Indoors and Outdoors Incidents")
		string_bytes = io.BytesIO()
		plt.savefig(string_bytes, format='jpg')
		string_bytes.seek(0)
		plot_base64data = base64.b64encode(string_bytes.read())
		return plot_base64data


def test():

	print("All the graphs will be generated for the range [lower, upper].")
	lower, upper = map(int, input("Enter the lower year bound and the upper year bound (separated by a space): ").split())
	# prepros_obj.dataset_path = "E:\Courses\CMSC 636 - Data Visualization\Dataset\Baltimore City\Part1_Crime_data.csv"
	# prepros_obj.dataset_read('csv')
	# print(prepros_obj.final_dataset)
	# prepros_obj = Preprocessing(lower, upper)
	# prepros_obj.dataset_all_updations()
	# print(prepros_obj.final_dataset)

	crime_viz = CrimeVisualizations()

	# Visualizations WITH neighborhood filter
	# dotw_year_noswr = crime_viz.day_of_the_week_boxplot("Year", lower, upper, False, 'Downtown')
	# dotw_year_swarm = crime_viz.day_of_the_week_boxplot("Year", lower, upper, True, 'Downtown')
	# in_ou_trends_year = crime_viz.indoor_outdoor_crimes_trends("Year", lower, upper, 'Downtown')
	# in_ou_trends_mnth = crime_viz.indoor_outdoor_crimes_trends("Month_Number", lower, upper, 'Downtown')
	# in_ou_trends_week = crime_viz.indoor_outdoor_crimes_trends("WeekNumber", lower, upper, 'Downtown')

	# Visualizations WITHOUT neighborhood filter
	# dotw_year_noswr = crime_viz.day_of_the_week_boxplot("Year", lower, upper, False)
	# dotw_year_swarm = crime_viz.day_of_the_week_boxplot("Year", lower, upper, True)
	# dotw_mnth_noswr = crime_viz.day_of_the_week_boxplot("Month_Name", lower, upper, False)
	# dotw_mnth_swarm = crime_viz.day_of_the_week_boxplot("Month_Name", lower, upper, True)

	# district_year_noswr = crime_viz.district_wise_boxplot("Year", lower, upper, False)
	# district_year_swarm = crime_viz.district_wise_boxplot("Year", lower, upper, True)
	# district_mnth_noswr = crime_viz.district_wise_boxplot("Month_Name", lower, upper, False)
	# district_mnth_swarm = crime_viz.district_wise_boxplot("Month_Name", lower, upper, True)

	# in_ou_trends_year = crime_viz.indoor_outdoor_crimes_trends("Year", lower, upper)
	# in_ou_trends_mnth = crime_viz.indoor_outdoor_crimes_trends("Month_Number", lower, upper)
	# in_ou_trends_week = crime_viz.indoor_outdoor_crimes_trends("WeekNumber", lower, upper)

	# bar_chart_unstckd = crime_viz.district_crime_bar_charts(lower, upper, False)
	# bar_chart_stacked = crime_viz.district_crime_bar_charts(lower, upper, True)