# Install the following packages:
# pymysql
# sqlalchemy

# Install the packages using the following commands:

# pip install pymysql
# pip install sqlalchemy


# Make sure that the Preprocessing.py file is in the same folder as this code

from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from Preprocessing import Preprocessing

# Uncomment the following line and insert the CSV file path in the double quotes
dataset = pd.read_csv("./tData.csv")
prepros_obj = Preprocessing()
prepros_obj.final_dataset = dataset
prepros_obj.dataset_all_updations()


# Replace "username" with your MySQL username, "database_name" with the name of the database
sqlEngine = create_engine('mysql+pymysql://root:iNsq4A4ECHNwfn0C@34.134.10.145/crime_data', pool_recycle=10000)
connection = sqlEngine.connect()
print(connection)
# Replace "crime_dataset_test" with the name of the table
prepros_obj.final_dataset.to_sql('crime_data', con=connection, index=False, if_exists='append')
print("Data inserted.")