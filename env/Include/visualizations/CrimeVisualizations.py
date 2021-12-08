import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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

	def day_of_the_week_boxplot(self, groupby = "Year", lower_year = 2016, upper_year = 2020, is_swarm = False, neighborhood_name = None, crime_type = None):
		"""Generates boxplots for total incidents across different days of the week.
		dataset: pandas DataFrame object
		groupby: column name to group the dataset by (Year (default) or Month_Name)
		lower_year: lower bound for year filter
		upper_year: upper bound for year filter
		is_swarm: flag to enable or disable swarmplot (Boolean)
		*neighborhood_name: contains name of ONE neighborhood (string as first and only element of tuple)"""
		
		if groupby is None: 
			groupby = "Year"
		elif groupby.lower() == 'month_name':
			groupby = "Month_Name"
		if lower_year is None:
    			lower_year = 2016
		else:
    			lower_year = int(lower_year)
		if upper_year is None:
    			upper_year = 2020
		else:
    			upper_year = int(upper_year)
		
		# Activate figure and update settings
		fig = plt.figure(figsize=(20, 10))
		self.seaborn_plot_settings()

		# Update dataset based on year filters
		self.dataset_updater(lower_year, upper_year)
		dataset = self.dataset_obj.final_dataset[['Year', 'Month_Name', 'Total_Incidents', 'Day', 'Neighborhood', 'Description']]

		# Check for Neighborhood filter and filter dataset and set title accordingly
		neighborhood_title_string = ''
		if neighborhood_name is not None:
			dataset = dataset[dataset['Neighborhood'] == neighborhood_name.upper()]
			neighborhood_title_string = f" for neighborhood {neighborhood_name}"

		crime_type_title_string = ""
		if crime_type is not None:
			dataset = dataset[dataset['Description'] == crime_type.upper()]
			crime_type_title_string = f"{crime_type} "
		
		title = crime_type_title_string + " Incidents by Day of the Week grouped by " + ("month" if groupby.lower() == 'month_name' else "year") + neighborhood_title_string

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
		
		if groupby is None: 
			groupby = "Year"
		elif groupby.lower() == 'month_name':
			groupby = "Month_Name"
		if lower_year is None:
    			lower_year = 2016
		else:
    			lower_year = int(lower_year)
		if upper_year is None:
    			upper_year = 2020
		else:
    			upper_year = int(upper_year)

			

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
			if groupby is not None and groupby.lower() == 'month_name': 
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

	def indoor_outdoor_crimes_trends(self, groupby = "Year", lower_year = 2016, upper_year = 2020, neighborhood_name = None, crime_type = None):
		"""Generates line graphs for inside/outside crimes for different time groupings.
		dataset: pandas DataFrame object
		groupby: column name to group the dataset by (Year (default) or Month_Name)
		lower_year: lower bound for year filter
		upper_year: upper bound for year filter
		*neighborhood_name: contains name of ONE neighborhood (string as first and only element of tuple)"""
		if groupby is not None and groupby.lower() == 'month_name': 
			groupby = 'month_number'
		# Activate figure and update settings

		if groupby is None: 
			groupby = "Year"
		elif groupby.lower() == 'month_name':
			groupby = "Month_Name"
		
		if lower_year is None:
			lower_year = 2016
		else:
			lower_year = int(lower_year)
	
		if upper_year is None:
			upper_year = 2020
		else:
			upper_year = int(upper_year)

		fig = plt.figure(figsize=(30, 10))
		self.seaborn_plot_settings()
		# Update dataset based on year filters
		self.dataset_updater(lower_year, upper_year)
		dataset = self.dataset_obj.final_dataset[['Year', 'Month_Number','WeekNumber', 'Total_Incidents', 'Inside_Outside', 'Neighborhood', 'Description']]

				# Check for Neighborhood filter and filter dataset and set title accordingly
		neighborhood_title_string = ''
		if neighborhood_name is not None:
			# print(neighborhood_name)
			dataset = dataset[dataset['Neighborhood'] == neighborhood_name.upper()]
			neighborhood_title_string = f" for neighborhood {neighborhood_name}"

		# Check for crime type filter and filter dataset and set title accordingly
		crime_type_title_string = ''
		if crime_type is not None:
			dataset = dataset[dataset['Description'] == crime_type.upper()]
			crime_type_title_string = f" of {crime_type} incidents"

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
		ax.set_title(f"Trends of Indoors and Outdoors Crimes by {grouping}{neighborhood_title_string}{crime_type_title_string}")
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

		if inside_outside_flag is None:
			inside_outside_flag = False
		if lower_year is None:
			lower_year = 2016

		if upper_year is None:
			upper_year = 2020
	
		# Activate figure and update settings
		plt.figure(figsize=(20, 10))
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
			tp = dataset.groupby(by = ["District", "Inside\\_Outside"]).count().reset_index()
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
	
	def hours_of_day_table(self, lower_year, upper_year, neighborhood, crime_type):
		df = self.dataset_obj.df_all_params(lower_year, upper_year, neighborhood, crime_type)

		df['Hours'] = df['CrimeDateTime'].astype(str).str.slice(11, 13)
		df['Hours'] = pd.to_numeric(df['Hours'], downcast='integer')
		
		pd.options.display.float_format = '{:,.0f}'.format

        #print (df[100:1200])
		df_grouped = df.groupby(
			['Hours', 'Description']).size().reset_index(name='Counts')
		data = df_grouped.pivot_table(
			'Counts', ['Hours'], 'Description').reset_index()
		#print (data)
		data["Hours"] = data["Hours"].astype(int)
		data["Hours"] = data["Hours"].astype(str)
		# data["Test"] = data["Counts"]-250

		return self.crimes_per_hour_viz(df_grouped, data, crime_type is None)

	def crimes_per_hour_viz(self, data, grouped, static):
        # Update dataset based on year filters
		fig = go.Figure()
		categories = []
		rgb_colors = ["rgb(15,76,129)", "rgb(92,144,144)", "rgb(165,178,181)", "rgb(191,208,202)",
                      "rgb(237,202,190)", "rgb(245,177,156)", "rgb(255,162,157)", "rgb(145,88,88)"]
		radius = 0
		if static is True:
			categories = ["Theft, Larceny & Robbery", "Assault, Homicide & Rape", "Arson & Shooting"]
			grouped["Assault, Homicide & Rape"] = grouped["AGG. ASSAULT"] + grouped["COMMON ASSAULT"] + grouped["RAPE"]
			grouped["Arson & Shooting"] = grouped["SHOOTING"] + grouped["ARSON"]
			grouped["Theft, Larceny & Robbery"] = grouped["AUTO THEFT"] + grouped["BURGLARY"] + grouped["LARCENY"] + grouped["LARCENY FROM AUTO"] + grouped["ROBBERY - CARJACKING"] + grouped["ROBBERY - COMMERCIAL"] + grouped["ROBBERY - RESIDENCE"] + grouped["ROBBERY - STREET"]
			# Choose the best 8 categories
			for i in range(0, len(categories)):
				radius += max(grouped[categories[i]])
				if i < len(rgb_colors):
					fig.add_trace(go.Barpolar(
	                   		r=grouped[categories[i]],
	                   		name=categories[i],
	                   		marker_color=rgb_colors[i],
	                   		theta=grouped['Hours']
					))
			fig.update_traces(text=grouped['Hours'].tolist())
			fig.update_layout(title='Crimes per Hour of Day', title_x=0.5, font_size=22,
          		legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.75),
            	legend_font_size=18,
            	template='plotly_dark',
            	polar=dict(
                	radialaxis=dict(range=[0, radius + 4]),
                	angularaxis=dict(showticklabels=True, showgrid=True, showline=True,
					rotation=90, direction="clockwise", tickfont_size=16)
            ),
            bargroupgap=0
            # showgrid=False
        )
		else:
			radius = max(data["Counts"])

			fig.add_trace(go.Barpolar(
				r=data["Counts"],
				name=data["Description"][0],
				marker_color=rgb_colors[0],
				theta=grouped['Hours']
				))
			fig.update_traces(text=grouped['Hours'].tolist())
			fig.update_layout(
				title='Crimes per Hour of Day',
            	title_x=0.5,
            	font_size=22,
            	legend=dict(
                	yanchor="top",
                	y=0.99,
               		xanchor="left",
                	x=0.75
            	),
            	legend_font_size=18,
            	template='plotly_dark',
            	polar=dict(
                	radialaxis=dict(range=[0, radius + 4]),
                	angularaxis=dict(showticklabels=True, showgrid=True, showline=True,
                                 rotation=90, direction="clockwise", tickfont_size=16)
            	),
            	bargroupgap=0
        	)
		fig_bytes = fig.to_image(format="jpg")
		buf = io.BytesIO(fig_bytes)
		plot_base64data = base64.b64encode(buf.read())
		return plot_base64data

def test():

	print("All the graphs will be generated for the range [lower, upper].")
