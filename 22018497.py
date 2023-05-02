# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 12:22:18 2023

@author: aaron
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# setiing seaborn theme
sns.set_theme()

# reading from csv
df = pd.read_csv('Electricity_Production_By_Source.csv')

# filling na values
df = df.fillna(0)
# dropping columns that are not needed
df.drop("Code", axis=1, inplace=True)
# using lambda functions to rename columns
df = df.rename(columns=lambda x: x.replace('Electricity from ', ''))
df = df.rename(columns=lambda x: x.replace(' (TWh)', ''))
# capitalising column names
df.columns = df.columns.str.capitalize()
# ordering
order = [0, 1, 2, 3, 7, 4, 9, 6, 8, 5]
df = df[[df.columns[i] for i in order]]


# plot 1

# selecting world data only
df_wrld = df[df['Entity'] == "World"]
# dropping columns that are not needed
df_wrld.drop("Entity", axis=1, inplace=True)
# setting index
df_wrld.set_index("Year", inplace=True)
# coverting data to percentage
df_wrld_percent = df_wrld.apply(lambda x: round((x/sum(x)*100), 2), axis=1)

# plotting area plot
df_wrld_percent.plot(kind='area', colormap='RdYlBu')
plt.show()

# plot 2

# plotting pie chart
df_wrld.loc[2020].plot(kind='pie', autopct='%1.0f%%', colormap='RdYlBu')
plt.show()

# plot 3

# plotting line plot
df_wrld_percent.plot()
plt.show()

# plot 4

# selecting Year 2020 only
df_2020 = df[df['Year'] == 2020]
# dropping columns that are not needed
df_2020.drop("Year", axis=1, inplace=True)
# setting index
df_2020.set_index("Entity", inplace=True)
# adding Total column
df_2020['Total'] = df_2020.sum(axis=1)
# sorting in descending order
df_2020 = df_2020.sort_values('Total', ascending=False)
# selecting top 15
df_2020_sample = df_2020[:15]
# dropping rows and columns that are not needed
df_2020_sample.drop(['World', 'EU27+1', 'EU-27'], inplace=True)
df_2020_sample.drop('Total', axis=1, inplace=True)

# plotting horizontal bar plot
df_2020_sample[::-1].plot(kind='barh', stacked=True, colormap='RdYlBu')
plt.show()
