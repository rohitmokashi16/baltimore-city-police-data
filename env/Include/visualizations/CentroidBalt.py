import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
from sklearn.cluster import KMeans
import base64
import numpy as np
import io
import os


class CentroidBaltimore:

    def __init__(self, prepros_obj):
        self.day_of_the_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        self.months_of_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.lower_year = 1950
        self.upper_year = 2021
        self.queryFunc = prepros_obj 
    
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

    def getCentroidForParams(self, lower, upper, neighborhood, crime_type):
        df = self.queryFunc(lower, upper, neighborhood, crime_type)
        filename = os.path.join(os.path.dirname(__file__), "../sample/geoMap/tl_2019_24510_faces.shp")
        street_map = gpd.read_file(filename)
        fig, ax = plt.subplots(figsize=(15,15))
        crs = {'init': 'epsg:4326'}

        geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
        X = [coord for coord in zip(df["Longitude"], df["Latitude"])]
        kmeans = KMeans(n_clusters=1, random_state=0).fit(X)
        geometry_kmeans = [Point(xy) for xy in kmeans.cluster_centers_]


        geo = gpd.GeoDataFrame(df, crs = crs, geometry = geometry)
        geo_kmeans = gpd.GeoDataFrame(kmeans.cluster_centers_, crs = crs, geometry = geometry_kmeans)


        street_map.plot(ax = ax)

        geo.plot(ax = ax, markersize = 20, color = "blue", marker = "o")
        geo_kmeans.plot(ax = ax, markersize = 30, color="red", marker = "o")
        
        string_bytes = io.BytesIO()
        # write matplotlib object as jpeg to the byte stream
        plt.savefig(string_bytes, format='jpg')
        # move the byte stream cursor back to the beginning 
        string_bytes.seek(0)
        #encode in base 64
        return base64.b64encode(string_bytes.read())   