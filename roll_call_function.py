# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 21:20:42 2021

@author: tuf91019
"""


import geopandas as gpd
import geopandas
import pandas as pd
from shapely.geometry import Point
import os
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)
import shapely.speedups
shapely.speedups.enable()
from adjustText import adjust_text
import time



class rollcallfunction:
    def __init__(self, csv, direct, output):
        self.direct = direct
        self.csv = csv
        self.output = output
        
        
    def shapefile(self):
        self.df = pd.read_csv(self.csv)
        geometry = [Point(xy) for xy in zip(self.df.Longitude, self.df.Latitude)]
        crs = {'init':'epsg:4326'}
        geo_df = gpd.GeoDataFrame(self.df, crs=crs, geometry=geometry)
        geo_df.to_file(self.output + '\\' + 'roll_call_locations.shp', driver='ESRI Shapefile')

        '''
        The above function takes the csv and turns it into a shapefile that is placed into the directory of 
        the user's choice. This csv is turned into a shapefile using a dataframe function from pandas,
        given a crs of WGS84, and converted into a geodataframe where it is given the crs specified.
        The geo_df.to_file will output the shapefile to the directory specified.
        '''    
        
        
    def rc_map(self):
        start = time.time()
        print("Time elapsed on working...")
        df = geopandas.read_file(self.output + '\\' + 'roll_call_locations.shp')
        roll_call = df
        maj_roads = geopandas.read_file('C:/Users/tuf91019/Desktop/Spring 2021/Capstone/major_roads.gpkg')
        us = geopandas.read_file('C:/Users/tuf91019/Desktop/Spring 2021/Capstone/us_counties.gpkg')  
        plt.figure(figsize=(60,60), facecolor='w', edgecolor='k')
        ax1 = plt.axes()
        maj_roads.plot(ax=ax1, alpha=0.25, color='black', facecolor='white')
        us.plot(ax=ax1, alpha=0.1, edgecolor='grey', facecolor='white')
        roll_call.plot(ax=ax1, alpha=0.50, color='green', facecolor='green')
        bar = AnchoredSizeBar(ax1.transData, 1, '50 miles', 4)
        ax1.add_artist(bar)
        ax1.set_title('Roll Call Locations', fontweight = 'bold')
        ax1.margins(2,2)
        xlim = ([roll_call.total_bounds[0],  roll_call.total_bounds[2]])
        ylim = ([roll_call.total_bounds[1],  roll_call.total_bounds[3]])
        ax1.set_ylim(ylim)
        ax1.set_xlim(xlim)
        texts = []
        for i, txt in enumerate(roll_call['Licensee N']):
            texts.append(plt.annotate(txt, (roll_call['Longitude'][i], roll_call['Latitude'][i])))
        adjust_text(texts)
        end = time.time()
        print("Time consumed in working: ",end - start)
        plt.savefig(self.output + '\\' +'roll_call.png')
       
        '''
        The rc_map function up above reads in the shapefile and turns it into a dataframe. It then
        plots the file, adds a basemap through the ctx (the contextily package), and adds a scalebar
        as well as title. The figure is then placed in the output directory and renamed as roll_call_locations.
        '''

        
      
    def rc_textfile(self):
        self.df = geopandas.read_file(self.output + "\\" + 'roll_call_locations.shp')
        roll_call_text_file = pd.DataFrame(self.df, columns =['Frequency', 'Call Sign', 'Service Co', 'Phone Numb',  'Licensee N', 'Power ERP', 'Licensee P', 'Latitude', 'Longitude'])
        base_filename = 'roll_call_text_file.txt'
        with open(os.path.join(self.output + '\\' + base_filename),'w') as outfile:
            roll_call_text_file.to_string(outfile)
            
        '''
        This final function turns the shapefile into a text file by converting it into a pandas dataframe with the columns
        specified from the shapefile. This can pare down the number of columns needed.
        It then joins the file's destination with the basename, usese 'w' to write the file and sends it out
        as a string. This can later be viewed in the output directory.
        '''


           
    def runrc(self):
        self.shapefile()
        self.rc_map()
        self.rc_textfile()
        
        '''
        This final function up here runs through each of the functions and is later
        utilized in the GUI file.
        '''

        
        