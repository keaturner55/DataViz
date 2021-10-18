#!/usr/bin/env python
# coding: utf-8
"""
Title: Final Project: Avanced Data Visualization in Matplotlib
Author: Keaton Turner
Date: 10/9/2021
Description: This script creates several plots using Colorado weather data
from NOAA.gov separated by county.
"""
#%%

import pandas as pd
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt
import numpy as np
from colour import Color

# Shape and weather data files
map_file = "C://Users/keatu/Regis/DataVisualization/Week8_FinalProj/Colorado_County_Boundaries.shp"
weather_file = "C://Users/keatu/Regis/DataVisualization/Week8_FinalProj/colorado_weather_history.csv"

# create primary dataframes
map_df = gpd.read_file(map_file)
weather_df = pd.read_csv(weather_file)
weather_df["DATE"] = weather_df["DATE"].str.replace('Feb-29','29-Feb')

# create a dict to map weather stations to a county via lat/long
stations = weather_df.groupby(['STATION', 'LATITUDE', 'LONGITUDE']).size().reset_index().drop(columns=[0]).values.tolist()
locator = Nominatim(user_agent="myGeocoder")
county_map = {i[0]:locator.reverse("{},{}".format(i[1],i[2])).raw["address"]["county"] for i in stations}
for i in county_map:
    county_map[i] = county_map[i].replace(" County","").upper()

# add county to weather data with map dict
weather_df["COUNTY"] = weather_df['STATION'].map(lambda x: county_map[x])

# Create dict of station count per county
density = weather_df.groupby(["COUNTY"])["STATION"].nunique()
density = density.reset_index().values.tolist()
density_map = {i[0]:i[1] for i in density} # used later in a function to change county text size on map

#%% First Viz: Weather stations
# create geodataframe of weather station locations using lat/long
locations_df = gpd.GeoDataFrame(weather_df.copy(), geometry=gpd.points_from_xy(weather_df.LONGITUDE, weather_df.LATITUDE))

fig, ax = plt.subplots(figsize = (15,12))
colors = [(174,199,232),(255,187,120),(152,223,138),(255,152,150),(197,176,213),(168,120,110)]
colors = [[(i[0]/255.0),(i[1]/255.0),(i[2]/255.0)] for i in colors]

# generate the map
map_df.plot(ax = ax, color='white', edgecolor='gray')

# add station locations
locations_df.plot(ax = ax, color=colors[2], markersize = 10, marker = "o")

# formatting
ax.set_title("Colorado Weather Stations by County", fontdict={'fontsize': '25', 'fontweight' : '3'})
ax.axis("off")
ax.annotate('Weather Station Data: https://www.ncdc.noaa.gov/cdo-web/', xy=(0.40, .14), xycoords='figure fraction', fontsize=15, color='grey')

# Add county annotations sized by # of stations in that particular county
map_df['coords'] = map_df['geometry'].apply(lambda x: x.representative_point().coords[:])
map_df['coords'] = [coords[0] for coords in map_df['coords']]
for idx, row in map_df.iterrows():
    if row["COUNTY"] in density_map:
        ax.annotate(s=row['COUNTY'], xy=row['coords'],horizontalalignment='center',size=(6+density_map[row["COUNTY"]])/1.5)
plt.savefig("weather_stations.png")


#%% Second Viz: Temperature plots

# gather temperature maximum data (aggregated using mean values)
use_col = "DLY-TMAX-NORMAL"
hottest_month = weather_df.groupby(["DATE"]).aggregate(
    {use_col:"mean"}).reset_index().sort_values([use_col], ascending=False).head(1)["DATE"].tolist()[0]
hottest_month = hottest_month.split("-")[-1]
hottest_counties = weather_df[weather_df["DATE"].str.contains(hottest_month)].groupby(
    ["COUNTY"]).aggregate({use_col:"mean"}).reset_index().sort_values([use_col], ascending=False).head(5)["COUNTY"].tolist()

# gather temperature minimum data (aggregated using mean values)
use_col = "DLY-TMIN-NORMAL"
coldest_month = weather_df.groupby(["DATE"]).aggregate(
    {use_col:"mean"}).reset_index().sort_values([use_col], ascending=True).head(1)["DATE"].tolist()[0]
coldest_month = coldest_month.split("-")[-1]
coldest_counties = weather_df[weather_df["DATE"].str.contains(coldest_month)].groupby(
    ["COUNTY"]).aggregate({use_col:"mean"}).reset_index().sort_values([use_col], ascending=False).head(5)["COUNTY"].tolist()

fig = plt.figure(figsize = (12,6))

# High Temp plot
use_col = "DLY-TMAX-NORMAL"
dark_red = Color("#8B0000")
light_red = Color("#FF7F7F")
reds = list(dark_red.range_to(light_red,5))
ax = fig.add_subplot(221)
for i,county in enumerate(hottest_counties):
    data = weather_df[(weather_df["COUNTY"]==county) & 
                      (weather_df["DATE"].str.contains(hottest_month))].groupby(
                    ["COUNTY","DATE"]).aggregate({use_col:"mean"}).reset_index()
    data["DATE"] = data["DATE"].apply(lambda x: "{}".format(x.split("-")[0].zfill(2)))
    data = data.sort_values("DATE")
    ax.scatter(data["DATE"],data[use_col], color = reds[i].rgb, label = county)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_xticklabels("")
ax.set_xticks("")
ax.set_title(hottest_month, fontsize = 20)
ax.legend(loc ='upper left',bbox_to_anchor=(-.4,1), frameon=False)


# Low Temp plot
use_col = "DLY-TMIN-NORMAL"
dark_blue = Color("#00008B")
light_blue = Color("#ADD8E6")
blues = list(light_blue.range_to(dark_blue,5))
ax2 = fig.add_subplot(223)
for i,county in enumerate(coldest_counties):
    data = weather_df[(weather_df["COUNTY"]==county) & 
                      (weather_df["DATE"].str.contains(coldest_month))].groupby(
                    ["COUNTY","DATE"]).aggregate({use_col:"mean"}).reset_index()
    data["DATE"] = data["DATE"].apply(lambda x: "{}".format(x.split("-")[0].zfill(2)))
    data = data.sort_values("DATE")
    ax2.scatter(data["DATE"],data[use_col], color = blues[i].rgb, label = county)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.set_xticklabels("")
ax2.set_xticks("")
ax2.set_title(coldest_month, fontsize = 20)
ax2.legend(loc ='upper left',bbox_to_anchor=(-.43,1), frameon=False)


# BACA county temperature swings plot
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
tmid = [weather_df[(weather_df["COUNTY"]=="BACA") & (weather_df["DATE"].str.contains(month))]["DLY-TAVG-NORMAL"].mean()
          for month in months]
tmin = [weather_df[(weather_df["COUNTY"]=="BACA") & (weather_df["DATE"].str.contains(month))]["DLY-TMIN-NORMAL"].mean()
          for month in months]
tmax = [weather_df[(weather_df["COUNTY"]=="BACA") & (weather_df["DATE"].str.contains(month))]["DLY-TMAX-NORMAL"].mean()
          for month in months]

ax3 = fig.add_subplot(122)
ax3.errorbar(months,tmid,yerr=(np.array(tmid)-np.array(tmin),(np.array(tmax)-np.array(tmid))),
             linestyle="", color = "green")
ax3.axhspan(0,32, facecolor=colors[0], alpha = 0.5)
ax3.annotate(s = "Freezing", xy=(4.5,18), color='gray', size = 12)
ax3.spines['right'].set_visible(False)
ax3.spines['top'].set_visible(False)
ax3.set_xticklabels(months,rotation=90, size = 12)
ax3.set_ylim(0,97)
ax3.set_title("Baca County Temperature Swings", fontsize = 14)
plt.savefig("Temperatures.png")


#%% Third Viz: Snow/rainfall totals graphic

# generate a plot of cumulative snow/rain counts by county per day
# individual plots used to create animation w/ ImageMagick
for i,day in enumerate(weather_df["DATE"].unique()):
    # get relevant data
    use_col = 'YTD-PRCP-NORMAL'
    daydf = weather_df.loc[(weather_df['DATE']==day) & (weather_df[use_col] > 0)].groupby(["COUNTY"]).aggregate({use_col:"mean"})
    if len(daydf) == 0:
        continue
    merged = gpd.GeoDataFrame(map_df.merge(daydf, how='left', left_on="COUNTY", right_on="COUNTY"))
    
    # set parameters for the overall figure
    fig, [[ax, ax2], [ax3, ax4]] = plt.subplots(2,2, gridspec_kw={'width_ratios': [12, 12], 'height_ratios':[10,8]}, dpi=150)
    fig.suptitle('Cumulative Totals: {}'.format(day), size = 15, y=.999)
    
    ############################### RAINFALL PLOTS
    # get relevant data
    use_col = 'YTD-PRCP-NORMAL'
    daydf = weather_df.loc[(weather_df['DATE']==day) & (weather_df[use_col] > 0)].groupby(["COUNTY"]).aggregate({use_col:"mean"})
    if len(daydf) == 0:
        continue
    merged = gpd.GeoDataFrame(map_df.merge(daydf, how='left', left_on="COUNTY", right_on="COUNTY"))
    # generate the map
    merged.plot(column = use_col, cmap = 'Blues', linewidth = 0.8,ax = ax, edgecolor = 'grey')
    ax.set_title("Precipitation (inches)", fontdict={'fontsize': '11', 'fontweight' : '3'})
    ax.axis("off")
    
    # Show top 10 locations
    top10 = merged.sort_values(by=use_col, ascending=False).head(10)
    top10['coords'] = top10['geometry'].apply(lambda x: x.representative_point().coords[:])
    top10['coords'] = [coords[0] for coords in top10['coords']]
    c = 0
    for idx, row in top10.iterrows():
        c += 1
        if row["COUNTY"] in density_map:
            ax.annotate(s=c, xy=row['coords'],horizontalalignment='center',size=(9))
    
    # Generate bar plot w/ top 10 counties    
    ax3.bar(top10["COUNTY"], top10[use_col])
    ax3.tick_params(rotation=90)
    ax3.spines['right'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3.tick_params(axis='y', labelsize= 8)
    t = [0, round(top10[use_col].max(),1)]
    ax3.set_yticklabels(t,rotation=0)
    ax3.set_yticks(t)

    ############################### SNOWFALL PLOTS
    
    # get relevant data
    use_col = 'YTD-SNOW-NORMAL'
    daydf2 = weather_df.loc[(weather_df['DATE']==day) & (weather_df[use_col] > 0)].groupby(["COUNTY"]).aggregate({use_col:"mean"})
    if len(daydf2) == 0:
        continue
    merged2 = gpd.GeoDataFrame(map_df.merge(daydf2, how='left', left_on="COUNTY", right_on="COUNTY"))

    # generate the map
    merged2.plot(column = use_col, cmap = 'Greens', linewidth = 0.8,ax = ax2, edgecolor = 'grey')
    ax2.set_title("Snowfall (inches)", fontdict={'fontsize': '11', 'fontweight' : '3'})
    ax2.axis("off")
    
    # Show top 10 locations
    top10 = merged2.sort_values(by=use_col, ascending=False).head(10)
    top10['coords'] = top10['geometry'].apply(lambda x: x.representative_point().coords[:])
    top10['coords'] = [coords[0] for coords in top10['coords']]
    c = 0
    for idx, row in top10.iterrows():
        c += 1
        if row["COUNTY"] in density_map:
            ax2.annotate(s=c, xy=row['coords'],horizontalalignment='center',size=(9))
            
    # Generate bar plot w/ top 10 counties
    ax4.bar(top10["COUNTY"], top10[use_col], color="green")
    ax4.tick_params(rotation=90)
    ax4.spines['right'].set_visible(False)
    ax4.spines['top'].set_visible(False)
    ax4.tick_params(axis='y', labelsize= 8)
    t = [0, round(top10[use_col].max(),1)]
    ax4.set_yticklabels(t,rotation=0)
    ax4.set_yticks(t)
    
    fig.tight_layout(rect=[0.05, 0.03, .9, 0.9])
    plt.savefig("C://Users/keatu/workspace/{}_precip_{}.png".format(str(i).zfill(3),day))
    plt.close()

