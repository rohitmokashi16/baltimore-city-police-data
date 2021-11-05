import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import distutils
import io
import base64

class CrimeVisualizations:

	def __init__(self):
		"""Initializes a few variables that are used multiple times across different functions."""
		self.string_bytes = io.BytesIO()
		self.day_of_the_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
		self.months_of_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	
	def seaborn_plot_settings(self):
		"""Default seaborn plot settings."""

		sns.set_style()
		sns.set_context("notebook")
		# sns.set(rc={'figure.figsize':(30, 10)})
		sns.set(font_scale = 1.25)

	def day_of_the_week_boxplot(self, dataset, groupby = "Year", lower_year = 1950, upper_year = 2021, is_swarm = False):
		"""Generates boxplots for total incidents across different days of the week.
		dataset: pandas DataFrame object
		groupby: column name to group the dataset by (Year (default) or Month_Name)
		lower_year: lower bound for year filter
		upper_year: upper bound for year filter
		is_swarm: flag to enable or disable swarmplot (Boolean)"""
		self.string_bytes = io.BytesIO()
		
		fig = plt.figure(figsize=(20, 10))
		dataset = dataset[['Year', 'Month_Name', 'Total_Incidents', 'Day']]
		self.seaborn_plot_settings()
		title = "Incidents by Day of the Week grouped by " + ("month" if groupby.lower() == 'month_name' else "year")
		tp = dataset[(dataset['Year'] >= int(lower_year)) & (dataset['Year'] <= upper_year)].groupby(by = ["Day", groupby]).count().reset_index()
		print(is_swarm)
		print(type(is_swarm))
		if is_swarm:
			if groupby.lower() == "month_name":
				sns.swarmplot(x="Total_Incidents", y="Day", data=tp, hue=groupby, order = self.day_of_the_week, size = 7, hue_order = self.months_of_year)
			else:
				sns.swarmplot(x="Total_Incidents", y="Day", data=tp, hue=groupby, order = self.day_of_the_week, size = 7)
			title = title + " with swarmplot of " + ("month" if groupby.lower() == 'month_name' else "year")
		bx_plt = sns.boxplot(x="Total_Incidents", y="Day", data=tp, order = self.day_of_the_week)
		bx_plt.set_ylabel("Day of the week", fontsize = 15)
		bx_plt.set_xlabel("Total Incidents", fontsize = 15)
		bx_plt.set_title(title)
		plt.savefig(self.string_bytes, format='jpg')
		self.string_bytes.seek(0)
		plot_base64data = base64.b64encode(self.string_bytes.read())
		return plot_base64data
	
	def district_wise_boxplot(self, dataset, groupby= "Year", lower_year = 1950, upper_year = 2021, is_swarm = False):
		"""Generates boxplots for total incidents across different districts.
		dataset: pandas DataFrame object
		groupby: column name to group the dataset by (Year (default) or Month_Name)
		lower_year: lower bound for year filter
		upper_year: upper bound for year filter
		is_swarm: flag to enable or disable swarmplot (Boolean)"""
		self.string_bytes = io.BytesIO()

		fig = plt.figure(figsize=(20, 10))
		self.seaborn_plot_settings()
		dataset = dataset[['Year', 'Month_Name', 'Total_Incidents', 'District']]
		grouping = "Month" if groupby.lower() == 'month_name' else 'year'
		title = f"Incidents by District grouped by {grouping}"
		tp = dataset[(dataset['Year'] >= int(lower_year)) & (dataset['Year'] <= int(upper_year))].groupby(by = ["District", groupby]).count().reset_index()
		if is_swarm:
			if groupby.lower() == "month_name":
				sns.swarmplot(x="Total_Incidents", y="District", data=tp, hue=groupby, size = 7, hue_order = self.months_of_year)
			else:
				sns.swarmplot(x="Total_Incidents", y="District", data=tp, hue=groupby, size = 7)
			title = title + " with swarmplot of " + grouping
		bx_plt = sns.boxplot(x="Total_Incidents", y="District", data=tp)
		bx_plt.set_ylabel("District", fontsize = 15)
		bx_plt.set_xlabel("Total Incidents", fontsize = 15)
		bx_plt.set_title(title)
		plt.savefig(self.string_bytes, format='jpg')
		self.string_bytes.seek(0)
		plot_base64data = base64.b64encode(self.string_bytes.read())
		return plot_base64data
	
	def indoor_outdoor_crimes_trends(self, dataset, groupby = "Year", lower_year = 1950, upper_year = 2021):
		"""Generates line graphs for inside/outside crimes for different time groupings.
		dataset: pandas DataFrame object
		groupby: column name to group the dataset by (Year (default) or Month_Name)
		lower_year: lower bound for year filter
		upper_year: upper bound for year filter"""
		self.string_bytes = io.BytesIO()

		fig = plt.figure(figsize=(30, 10))
		self.seaborn_plot_settings()
		
		if groupby == 'Month_Name':
  			groupby = 'Month_Number'

		dataset = dataset[['Year', 'Month_Number','WeekNumber', 'Total_Incidents', 'Inside_Outside']]
		tp = dataset[(dataset['Year'] >= int(lower_year)) & (dataset['Year'] <= int(upper_year))].groupby(by = [groupby, 'Inside_Outside']).count().reset_index()
		ax = sns.lineplot(x = groupby, y='Total_Incidents', data = tp, hue = "Inside_Outside", sort = False)
		fontsz = 15
		if groupby.lower() == 'year':
			ax.set_xlabel("Year", fontsize = 15)
			grouping = 'year'
		else:
			if groupby.lower() == 'month_number':
				upper, labels, grouping = 13, self.months_of_year, "Month"
			else:
				upper, labels, grouping, fontsz = 54, [i for i in range(1, 54)], "Week Number", 10
			ax.set_xticks(range(1, upper))
			ax.set_xticklabels(labels, size = fontsz)
			ax.set_xlabel(grouping, fontsize = 15)
		ax.set_ylim([tp['Total_Incidents'].min()//2, tp['Total_Incidents'].max()*1.25])
		ax.set_ylabel("Total Incidents", fontsize = 15)	
		ax.set_title(f"Trends of Indoors and Outdoors Crimes by {grouping}")
		plt.savefig(self.string_bytes, format='jpg')
		self.string_bytes.seek(0)
		plot_base64data = base64.b64encode(self.string_bytes.read())
		return plot_base64data

	def district_crime_bar_charts(self, dataset, lower_year = 1950, upper_year = 2021, inside_outside_flag = False):
		"""Generates bar charts and stacked bar charts for crimewise incident totals.
		dataset: pandas DataFrame object
		lower_year: lower bound for year filter
		upper_year: upper bound for year filter
		inside_outside_flag: if True, generates a stacked bar chart instead of a normal horizontal chart"""
		self.string_bytes = io.BytesIO()

		fig = plt.figure(figsize=(20, 10))
		self.seaborn_plot_settings()
		dataset = dataset[['District', 'Total_Incidents', 'Inside_Outside', 'Year']]
		if not inside_outside_flag:
			tp = dataset[(dataset['Year'] >= int(lower_year)) & (dataset['Year'] <= int(upper_year))].groupby(by = ["District"]).count().reset_index()
			ax = sns.barplot(data = tp, x = "Total_Incidents", y = 'District', order = tp.sort_values("Total_Incidents", ascending = True).District)
			ax.set_ylabel("District", fontsize = 15)
			ax.set_xlabel("Incident Count", fontsize = 15)
			ax.set_title("Bar Chart of Incident Count by Districts")
		else:
			tp = dataset[(dataset['Year'] >= int(lower_year)) & (dataset['Year'] <= int(upper_year))].groupby(by = ["District", "Inside_Outside"]).count().reset_index()
			tp1 = tp.groupby(['District']).sum().sort_values(['Total_Incidents'], ascending = False).reset_index()
			sort_order = {i: 0 for i in tp1['District'].unique()}
			val = 0
			for i in sort_order.keys():
				sort_order[i] = val
				val += 1
			tp = tp.assign(sort = lambda tp: tp['District'].map(sort_order)).sort_values('sort').drop('sort', axis = 1)
			b1 = plt.barh(tp['District'].unique(), tp.loc[tp['Inside_Outside'] == 'Outside', 'Total_Incidents'])
			b2 = plt.barh(tp['District'].unique(), tp.loc[tp['Inside_Outside'] == 'Inside', 'Total_Incidents'], left = tp.loc[tp['Inside_Outside'] == 'Outside', 'Total_Incidents'])
			plt.legend([b1, b2], ["Outside", "Inside"], title = "Crime Setting", loc="upper right")
			plt.xlabel("District")
			plt.ylabel("Incident Count")
			plt.title("Stacked Bar Chart of Incident Count by Districts broken into Indoors and Outdoors Incidents")
		plt.savefig(self.string_bytes, format='jpg')
		self.string_bytes.seek(0)
		plot_base64data = base64.b64encode(self.string_bytes.read())
		return plot_base64data

def test():
	prepros_obj = Preprocessing()
	prepros_obj.dataset_path = "./env/Include/sample/Part1_Crime_data.csv"
	prepros_obj.dataset_read('csv')
	# print(prepros_obj.final_dataset)
	prepros_obj.dataset_all_updations()
	# print(prepros_obj.final_dataset)
	print("All the graphs will be generated for the range [lower, upper].")
	lower, upper = map(int, input("Enter the lower year bound and the upper year bound (separated by a space): ").split())

	

	crime_viz = CrimeVisualizations()
	dotw_year_noswr = crime_viz.day_of_the_week_boxplot(prepros_obj.final_dataset, "Year", lower, upper, False)
	dotw_year_swarm = crime_viz.day_of_the_week_boxplot(prepros_obj.final_dataset, "Year", lower, upper, True)
	dotw_mnth_noswr = crime_viz.day_of_the_week_boxplot(prepros_obj.final_dataset, "Month_Name", lower, upper, False)
	dotw_mnth_swarm = crime_viz.day_of_the_week_boxplot(prepros_obj.final_dataset, "Month_Name", lower, upper, True)

	district_year_noswr = crime_viz.district_wise_boxplot(prepros_obj.final_dataset, "Year", lower, upper, False)
	district_year_swarm = crime_viz.district_wise_boxplot(prepros_obj.final_dataset, "Year", lower, upper, True)
	district_mnth_noswr = crime_viz.district_wise_boxplot(prepros_obj.final_dataset, "Month_Name", lower, upper, False)
	district_mnth_swarm = crime_viz.district_wise_boxplot(prepros_obj.final_dataset, "Month_Name", lower, upper, True)

	in_ou_trends_year = crime_viz.indoor_outdoor_crimes_trends(prepros_obj.final_dataset, "Year", lower, upper)
	in_ou_trends_mnth = crime_viz.indoor_outdoor_crimes_trends(prepros_obj.final_dataset, "Month_Number", lower, upper)

	bar_chart_unstckd = crime_viz.district_crime_bar_charts(prepros_obj.final_dataset, lower, upper, False)
	bar_chart_stacked = crime_viz.district_crime_bar_charts(prepros_obj.final_dataset, lower, upper, True)

	# print(len(dotw_mnth_noswr), len(dotw_year_swarm), len(dotw_mnth_noswr), len(dotw_mnth_swarm), len(district_year_noswr), len(district_year_swarm), len(district_mnth_noswr), len(district_mnth_swarm), len(in_ou_trends_year), len(in_ou_trends_mnth), len(bar_chart_unstckd), len(bar_chart_stacked))

