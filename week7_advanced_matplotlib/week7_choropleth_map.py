#!/usr/bin/env python
# coding: utf-8

"""
Title: Matplotlib Adcanced Data Visualizations
Author: Keaton Turner
Date: 10/9/2021
Description: This script creates 2 plots of choropleth visuals
for France covid data (separated by department)
"""
#%%
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import colors


#%% VIZ # 1: Hospitalizations by department
# shape and data file path locations
france_shapefile = "C:/Users/keatu/Regis/DataVisualization/Week7_Advanced-Matplotlib/fra.shp"
france_cov19_file = "C:/Users/keatu/Regis/DataVisualization/Week7_Advanced-Matplotlib/france_trends_by_department.csv"

# create dataframes (geopandas and pandas) and merge on France Department name
map_df = gpd.read_file(france_shapefile)
covid_df =  pd.read_csv(france_cov19_file)
cmapdf = map_df.merge(covid_df, how='left', left_on="ADMIN_NAME", right_on="Department")

# Use total hospitalizations
use_col = "total_hospitalizations"
fig  = plt.figure(figsize = (17,6))
ax = fig.add_subplot(1, 2, 1)
ax.axis("off")

# set parameters for color bar/map
sm = plt.cm.ScalarMappable(cmap='Reds',
                           norm = plt.Normalize(vmin=cmapdf[use_col].min(),
                                               vmax=cmapdf[use_col].max()))
sm.set_array([])
scale_factor = 10**3
fmt = mpl.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_factor))
cb = fig.colorbar(sm)
cb.ax.tick_params(labelsize = 10)
cb.ax.yaxis.set_major_formatter(fmt)
cb.set_label('x10^3', rotation=270, size = 15, labelpad = 20)

# generate the map
cmapdf.plot(column = use_col, cmap = 'Reds', linewidth = 0.8,
            ax = ax, edgecolor = '0.8')

# add a title
ax.set_title('Total Hospitalizations', fontdict={'fontsize': '25', 'fontweight' : '3'})

# Add second map
ax2 = fig.add_subplot(1, 2, 2)
use_col = "per_100k"
ax2.axis("off")

# set parameters for color bar/map
sm2 = plt.cm.ScalarMappable(cmap='Reds',
                           norm = plt.Normalize(vmin=cmapdf[use_col].min(),
                                               vmax=cmapdf[use_col].max()))
sm2.set_array([])
cb2 = fig.colorbar(sm2)
cb2.ax.tick_params(labelsize = 10)
cb2.ax.yaxis.set_major_formatter(fmt)
cb2.set_label('x10^3', rotation=270, size = 15, labelpad = 20)

# generate the 2nd map
cmapdf.plot(column = use_col, cmap = 'Reds', linewidth = 0.8,
            ax = ax2, edgecolor = '0.8')

# add a title and annotation
ax2.set_title('Hospitalizations (per 100k)', fontdict={'fontsize': '25', 'fontweight' : '3'})
ax.annotate('Source: https://www.nytimes.com/interactive/2021/world/france-covid-cases.html', xy=(0.35, .05), xycoords='figure fraction', fontsize=15, color='grey')
plt.savefig("hospitalizations.png")


#%% VIZ # 2 Hospitalizations 14 day change


france_cov19_file_recent = "C:/Users/keatu/Regis/DataVisualization/Week7_Advanced-Matplotlib/france_trends_by_department_recent.csv"

covid_df2 =  pd.read_csv(france_cov19_file_recent)
cmapdf2 = map_df.merge(covid_df2, how='left', left_on="ADMIN_NAME", right_on="Department")

use_col = "14_day_change"
fig, ax = plt.subplots(figsize = (30,15))
ax.axis("off")


# set parameters for color map
sm = plt.cm.ScalarMappable(cmap="bwr",
                           norm = colors.TwoSlopeNorm(vmin=cmapdf2[use_col].min(),
                                               vmax=cmapdf2[use_col].max(), vcenter = 0))

sm.set_array([])
cb = fig.colorbar(sm)
cb.set_label('Percentage', rotation=270, size = 20, labelpad = 20)
cb.ax.tick_params(labelsize = 20)
cmapdf2.plot(column = use_col, cmap = "bwr", linewidth = 0.8,
            ax = ax, edgecolor = '0.8')

# Add data labels
cmapdf2['coords'] = cmapdf2['geometry'].apply(lambda x: x.representative_point().coords[:])
cmapdf2['coords'] = [coords[0] for coords in cmapdf2['coords']]
top2 = cmapdf2.sort_values(by=use_col, ascending=False).head(2)
for idx, row in top2.iterrows():
    ax.annotate(s=row['Department'], xy=row['coords'],horizontalalignment='center',size=15)


# add a title and annotation
ax.set_title('14 Day Change', fontdict={'fontsize': '25', 'fontweight' : '3'})
ax.annotate('Source: https://www.nytimes.com/interactive/2021/world/france-covid-cases.html', xy=(0.24, .05), xycoords='figure fraction', fontsize=25, color='grey')
plt.savefig("14daychange.png")


# In[ ]:




