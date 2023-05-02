# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 12:22:18 2023

@author: aaron
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

# reading from csv
df = pd.read_csv('Electricity_Production_By_Source.csv')


# selecting world data only from 1990
df_wrld = df[(df['Entity'] == "World")]
# dropping columns that are not needed
df_wrld.drop(["Entity", "Code"], axis=1, inplace=True)
# setting index
df_wrld.set_index("Year", inplace=True)

# coverting data to percentage
df_wrld_percent = df_wrld.apply(lambda x: round((x/sum(x)*100), 2), axis=1)

# using lambda functions to rename columns
df_wrld_percent =\
    df_wrld_percent.rename(columns=lambda x: x.replace('Electricity from ',
                                                       ''))
df_wrld_percent =\
    df_wrld_percent.rename(columns=lambda x: x.replace(' (TWh)', ''))
df_wrld_percent = \
    df_wrld_percent.rename(columns=lambda x: x.replace(' (zero filled)', ''))

# renaming one more column
df_wrld_percent =\
    df_wrld_percent.rename(columns={"Other renewables excluding bioenergy":
                                    "Other renewables"})
# capitalising column names
df_wrld_percent.columns = df_wrld_percent.columns.str.capitalize()
# ordering
order = [0, 1, 5, 2, 7, 4, 6, 3]
df_wrld_percent = df_wrld_percent[[df_wrld_percent.columns[i] for i in order]]

# plotting area plot
df_wrld_percent.plot(kind='area', colormap='RdYlBu')
plt.show()
