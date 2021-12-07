import matplotlib.pyplot as plt
import pandas as pd
import july
from july.utils import date_range
from datetime import datetime, timedelta
import io
import base64

class CrimeCalendar:
    def __init__(self, prepros_obj):
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
        flag = False
        if self.lower_year != lower or self.upper_year != upper:
            self.lower_year, self.upper_year = lower, upper
            flag = True
        return flag
 
    def dataIncidentFromParams(self, lower_year = 2016, upper_year = 2020, neighborhood_name = None, crime_type = None):
        self.dataset_updater(lower_year, upper_year)
        dataset = self.dataset_obj.final_dataset[['Year', 'annoying', 'Date', 'Month_Number', 'CrimeDateTime', 'Month_Name', 'Total_Incidents', 'Day', 'Neighborhood', 'Description', 'DayNumber']]
        
        if neighborhood_name is not None:
            dataset = dataset[dataset['Neighborhood'] == neighborhood_name.upper()]

        if crime_type is not None:
            dataset = dataset[dataset['Description'] == crime_type.upper()]

        return dataset

    def yearCalendar(self, lower, upper, neighborhood, crime_type):
        data = self.dataIncidentFromParams(lower, upper, neighborhood, crime_type)

        # plot whole year calendar
        start = lower + "-01-01"
        end = upper + "-12-31"
        dates = date_range(start,end) # datetime
        if neighborhood is None:
            neighborhood = 'all neighborhoods'
        if crime_type is None:
            crime_type = 'All crimes'
        crime_array = data.groupby(['annoying']).count().reset_index().to_numpy()
        finalArray = [0] * len(dates)
        for i in crime_array:
            index = (i[0] - dates[0]).days
            finalArray[index] = i[1]

        july.calendar_plot(dates, finalArray)
        # new byte stream
        string_bytes = io.BytesIO()
        # write matplotlib object as jpeg to the byte stream
        plt.savefig(string_bytes, format='jpg')
        # move the byte stream cursor back to the beginning 
        string_bytes.seek(0)
        #encode in base 64
        return base64.b64encode(string_bytes.read())   
