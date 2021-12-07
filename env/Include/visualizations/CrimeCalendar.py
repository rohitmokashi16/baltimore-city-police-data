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
        dataset = self.dataset_obj.final_dataset[['Year', 'Month_Number', 'Month_Name', 'Total_Incidents', 'Day', 'Neighborhood', 'Description', 'DayNumber']]
       	# Check for Neighborhood filter and filter dataset and set title accordingly
        neighborhood_title_string = ''
        
        if neighborhood_name is not None:
            dataset = dataset[dataset['Neighborhood'] == neighborhood_name.upper()]
            neighborhood_title_string = f" for neighborhood {neighborhood_name}"

        crime_type_title_string = ""
        if crime_type is not None:
            dataset = dataset[dataset['Description'] == crime_type.upper()]
            crime_type_title_string = f"{crime_type} "
		
        title = crime_type_title_string + " Incidents by Day of the Week " + neighborhood_title_string

        # THIS LINE RIGHT HERE::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        return dataset.groupby(by = ["DayNumber", "Year"]).count().reset_index().to_numpy().T[2]


    def yearCalendar(self, lower, upper, neighborhood, crime_type):
        data = self.dataIncidentFromParams(lower, upper, neighborhood, crime_type)
        start = lower + "-01-01"
        end = upper + "-12-31"
        dates = date_range(start,end) # datetime
        # plot whole year calendar
        july.calendar_plot(dates, data)
        # new byte stream
        string_bytes = io.BytesIO()
        # write matplotlib object as jpeg to the byte stream
        plt.savefig(string_bytes, format='jpg')
        # move the byte stream cursor back to the beginning 
        string_bytes.seek(0)
        #encode in base 64
        return base64.b64encode(string_bytes.read())   

    # def monthCalendar(self, year, mth,num):
    #     start = year + "-01-01"
    #     end = year + "-12-31"
    #     dates = date_range(start,end) # datetime
    #     # plot one year calendar
    #     july.month_plot(dates, inci, month=int(mth), colorbar=True)
    #     # new byte stream
    #     string_bytes = io.BytesIO()
    #     # write matplotlib object as jpeg to the byte stream
    #     plt.savefig(string_bytes, format='jpg')
    #     # move the byte stream cursor back to the beginning 
    #     string_bytes.seek(0)
    #     #encode in base 64
    #     return base64.b64encode(string_bytes.read())
