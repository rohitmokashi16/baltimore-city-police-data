import numpy as np
import pandas as pd
import calendar
import json
from sqlalchemy import create_engine


class Preprocessing:
	
	def __init__(self):
		"""Initializes some variables used multiple times through the class."""

		self.final_dataset = None
		# Replace root, IP address, and dv_testdb with your respective credentials
		sqlEngine = create_engine('mysql+pymysql://root:iNsq4A4ECHNwfn0C@34.134.10.145/crime_data', pool_recycle=3600)
		self.connection = sqlEngine.connect()

	def dataset_read(self, year1, year2):
		"""Read dataset from MySQL for the specific year range.
		year1: integer, lower bound of year
		year2: integer, upper bound of year
		Dataset filtered for the range [year1, year2]"""

		sql_query = f'select * from crime_data where year(CrimeDateTime) between {year1} and {year2}'
		self.final_dataset = pd.read_sql(sql_query, con = self.connection)
		print(f"Records between years {year1} and {year2} fetched.")
		
	def dataset_read_all_params(self, year1, year2, neighborhood, crime_type):	
		sql_query = ''
		if neighborhood is not None and crime_type is not None:
			sql_query = f'select * from crime_data where (year(CrimeDateTime) between {year1} and {year2}) and Description = "{crime_type}" and Neighborhood = "{neighborhood}"'
		elif crime_type is not None:
			sql_query = f'select * from crime_data where (year(CrimeDateTime) between {year1} and {year2}) and Description = "{crime_type}"'
		elif neighborhood is not None: 
			sql_query = f'select * from crime_data where (year(CrimeDateTime) between {year1} and {year2}) and Neighborhood = "{neighborhood}"'
		else:
			sql_query = f'select * from crime_data where (year(CrimeDateTime) between {year1} and {year2}) LIMIT 500'
		
		df = pd.read_sql(sql_query, con = self.connection)
		return df.to_dict(orient="index")

	def df_all_params(self, year1, year2, neighborhood, crime_type):
		sql_query = ''
		if neighborhood is not None and crime_type is not None:
			sql_query = f'select * from crime_data where (year(CrimeDateTime) between {year1} and {year2}) and Description = "{crime_type}" and Neighborhood = "{neighborhood}" AND Latitude > 39.18 AND Latitude < 39.38 AND Longitude < -76.52 AND Longitude > -76.72'
		elif crime_type is not None:
			sql_query = f'select * from crime_data where (year(CrimeDateTime) between {year1} and {year2}) and Description = "{crime_type}" AND Latitude > 39.18 AND Latitude < 39.38 AND Longitude < -76.52 AND Longitude > -76.72'
		elif neighborhood is not None: 
			sql_query = f'select * from crime_data where (year(CrimeDateTime) between {year1} and {year2}) and Neighborhood = "{neighborhood}" AND Latitude > 39.18 AND Latitude < 39.38 AND Longitude < -76.52 AND Longitude > -76.72'
		else:
			sql_query = f'select *, SELECT COUNT(DISTINCT Date) as numInci from crime_data where (year(CrimeDateTime) between {year1} and {year2}) and Latitude > 39.18 AND Latitude < 39.38 AND Longitude < -76.52 AND Longitude > -76.72 LIMIT 500'
		
		return pd.read_sql(sql_query, con = self.connection)
		
	def dataset_add_year(self, dataset, column_name):
		"""Extract year from the given datetime column and add a new column with that data.
		dataset: pandas DataFrame object
		column_name: name of the datetime column in dataset"""

		dataset['Year'] = pd.DatetimeIndex(dataset[column_name]).year
		return dataset
	
	def dataset_add_month_details(self, dataset, column_name):
		"""Extract month number and month name from datetime column and store data in new columns.
		dataset: pandas DataFrame object
		column_name: name of the datetime column in dataset"""

		dataset['Month_Number'] = pd.DatetimeIndex(dataset[column_name]).month
		dataset['Month_Name'] = dataset['Month_Number'].apply(lambda x: calendar.month_name[x])
		return dataset
	
	def dataset_add_day_week_details(self, dataset, column_name):
		"""Extract day name, date, and week number from datetime column and store data in new columns.
		dataset: pandas DataFrame object
		column_name: name of the datetime column in dataset"""
		dataset['annoying'] = dataset['CrimeDateTime'].dt.date
		dataset['DayNumber'] = dataset['CrimeDateTime'].dt.day_of_year
		dataset['DayOfTheWeek'] = dataset['CrimeDateTime'].dt.dayofweek
		dataset['Day'] = dataset['CrimeDateTime'].dt.day_name()
		dataset['WeekNumber'] = dataset['CrimeDateTime'].dt.isocalendar().week
		return dataset

	def dataset_add_time_details(self):
		"""Perform all datetime related updations on the dataset."""

		self.final_dataset = self.final_dataset.dropna(axis = 0, subset = ['CrimeDateTime'])
		self.final_dataset['CrimeDateTime'] = pd.to_datetime(self.final_dataset['CrimeDateTime'])
		self.final_dataset = self.dataset_add_year(self.final_dataset, 'CrimeDateTime')
		self.final_dataset = self.dataset_add_month_details(self.final_dataset, 'CrimeDateTime')
		self.final_dataset = self.dataset_add_day_week_details(self.final_dataset, 'CrimeDateTime')
		print("Dataset updated with time details.")

	def dataset_clean_inside_outside(self):
		"""Replace I with Inside and O with Outside in the dataset."""

		self.final_dataset['Inside_Outside'].replace(to_replace = ['O', 'I'], value = ['Outside', 'Inside'], inplace = True)
		print("Inside/Outside details updated.")
	
	def dataset_all_updations(self):
		"""Perform all possible updations through one single function call."""

		self.dataset_add_time_details()
		self.dataset_clean_inside_outside()