#!/usr/bin/env python
# coding: utf-8

"""
Title: Matplotlib Data Visualizations
Author: Keaton Turner
Date: 10/2/2021
Description: This script creates four plots (3 total visualizations) looking
a dataset of annual customer spending totals (I think in Euros) for a wholesale
distributor.
"""

#%% Imports and data


import matplotlib.pyplot as plt
import matplotlib as mpl
from pandas import read_csv

# read the data
customerdf = read_csv("C:\\Users\\keatu\\Regis\\DataVisualization\\Week5and6_Matplotlib\\wholesale_customers_data.csv")

# define colors and defaults
mpl.style.use("seaborn-notebook")
colors = [(174,199,232),(255,187,120),(152,223,138),(255,152,150),(197,176,213),(168,120,110)]
colors = [[(i[0]/255.0),(i[1]/255.0),(i[2]/255.0)] for i in colors]

#%% Visualization 1:  Multiple boxplots for all numeric variables
#                      in the dataset, sorted by increasing mean value

# narrow down to only numeric variables and divide by 1000
numdf = customerdf[["fresh","milk","grocery","frozen","detergent","delicatessen"]] / 1000.0

# get dictionary of items sorted by increasing mean value
items_sorted_by_mean = {i[0]:list(numdf[i[0]]) for i in sorted(numdf.mean().reset_index().values, key = lambda x:x[1])}

# generate the figure
fig, ax = plt.subplots(figsize = (12,10))
bplot = ax.boxplot(items_sorted_by_mean.values(), patch_artist=True)
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
ax.set_xticklabels(items_sorted_by_mean.keys(), fontsize = 20, rotation=45)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.yticks(size = 20)
ax.set_title("Annual Wholesale Spending",fontsize = 25)
ax.set_ylabel("Euros (in thousands)", fontsize = 20)
plt.savefig("wholesale_spending_boxplots.png")


#%% Visualization 2 Part 1: Stacked barplots for each variable
#                           separating color based on retail channel


# group spending by channel
channel_groups = customerdf.drop("region",axis=1).groupby("channel")
channel_counts = channel_groups.aggregate("sum") / 100000
channel1 = channel_counts.iloc[0]
channel2= channel_counts.iloc[1]

# figure parameters
fig, ax = plt.subplots(figsize = (15,10))
ax.barh(list(channel_counts.columns), channel1, color=colors[3], label = "HoReCa")
ax.barh(list(channel_counts.columns), channel2, left=channel1, color=colors[4], label = "Retail")
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.xticks(size=20)
ax.tick_params(
    axis='y',         
    which='both',      
    left=False,     
    top=False,         
    labelleft=False) 
ax.set_title("Total Spending Per Channel", fontsize = 30)
ax.legend(fontsize = 20, bbox_to_anchor=(0.6,0.8))
plt.savefig("spending_per_channel.png")


#%% Visualization 2 Part 2: Stacked barplots for each variable
#                           separating color based on customer region

# group spending by region
region_groups = customerdf.drop("channel",axis=1).groupby("region")
region_counts = region_groups.aggregate("sum") / 100000
region1 = region_counts.iloc[0]
region2 = region_counts.iloc[1]
region3 = region_counts.iloc[2]

fig, ax = plt.subplots(figsize = (15,10))
ax.barh(list(channel_counts.columns), region1, color=colors[0], label = "Lisbon")
ax.barh(list(channel_counts.columns), region2, left=region1, color=colors[1], label = "Oporto")
ax.barh(list(channel_counts.columns), region3, left=region2+region1, color=colors[2], label = "Other")
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.xticks(size=20)
ax.tick_params(
    axis='y',         
    which='both',      
    left=False,     
    top=False,         
    labelleft=False) 
ax.set_title("Total Spending Per Region", fontsize = 30)
ax.legend(fontsize = 20, bbox_to_anchor=(0.6,0.8))
ax.set_xlim(56,0) # reverse the plot
plt.savefig("spending_per_region.png")


#%% Visualization # 3: Scatter plot of points for fresh vs grocery spending.
#                      Color points by region and change shape based on 
#                      channel--6 possible combinations

ch1r1 = customerdf.loc[(customerdf["channel"]==1) & (customerdf["region"]==1)]
ch1r2 = customerdf.loc[(customerdf["channel"]==1) & (customerdf["region"]==2)]
ch1r3 = customerdf.loc[(customerdf["channel"]==1) & (customerdf["region"]==3)]

ch2r1 = customerdf.loc[(customerdf["channel"]==2) & (customerdf["region"]==1)]
ch2r2 = customerdf.loc[(customerdf["channel"]==2) & (customerdf["region"]==2)]
ch2r3 = customerdf.loc[(customerdf["channel"]==2) & (customerdf["region"]==3)]

fig, ax = plt.subplots(figsize = (15,10))
markersize = 150
ax.scatter(ch1r1['fresh']/1000,ch1r1['grocery']/1000, color=colors[3], alpha=0.7, marker="o", label="HoReCa:Lisbon",s=markersize)
ax.scatter(ch1r2['fresh']/1000,ch1r2['grocery']/1000, color=colors[3], alpha=0.7, marker="^", label="HoReCa:Oporto",s=markersize)
ax.scatter(ch1r3['fresh']/1000,ch1r3['grocery']/1000, color=colors[3], alpha=0.7, marker="s", label="HoReCa:Other",s=markersize)

ax.scatter(ch2r1['fresh']/1000,ch2r1['grocery']/1000, color=colors[4], alpha=0.7, marker="o", label="Retail:Lisbon",s=markersize)
ax.scatter(ch2r2['fresh']/1000,ch2r2['grocery']/1000, color=colors[4], alpha=0.7, marker="^", label="Retail:Oporto",s=markersize)
ax.scatter(ch2r3['fresh']/1000,ch2r3['grocery']/1000, color=colors[4], alpha=0.7, marker="s", label="Retail:Other",s=markersize)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xticks(size=20)
plt.yticks(size=20)
ax.set_xlabel("fresh", fontsize=25)
ax.set_ylabel("grocery", fontsize=25)
ax.set_title("Spending Trends: Grocery vs Fresh", fontsize = 30)
#ax.text(x=15,y=40,s="Cafe",size=20, color = colors[4])
ax.legend(fontsize = 20, bbox_to_anchor=(0.6,0.8))
plt.tight_layout()
plt.savefig("fresh-vs-grocery.png")

