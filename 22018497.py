# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 12:22:18 2023

@author: aaron
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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


# plotting with GridSpec
fig = plt.figure(dpi=300, facecolor='#000038', layout='constrained')
# fig.set_size_inches(6, 12)

gs = plt.GridSpec(2, 3, figure=fig, width_ratios=[1, 1, 0.75])

# seting theme
rc = {'axes.facecolor': '#1221a6', 'text.color': 'black', 'axes.labelcolor':
      '.85', 'xtick.color': '.75', 'ytick.color': '.75',
      'grid.color': '.7'}
sns.set_theme(font_scale=0.75, rc=rc)

# some kwargs
kwargs = {'cmap': 'RdYlGn', 'legend': False}


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
ax1 = fig.add_subplot(gs[0, 0])
df_wrld_percent.loc[2000:].plot.area(ax=ax1, alpha=0.85, **kwargs)
ax1.set_ylabel('Electicity Produced (%)')
ax1.set_xticks(range(2000, 2021, 4))
ax1.set_yticks(range(0, 101, 10))
ax1.set_xlim(2000, 2021)

# plot 2

# plotting pie chart
ax2 = fig.add_subplot(gs[0, 1])
explode = [0.2 for i in range(len(df_wrld.loc[2020]))]
df_wrld.loc[2020].plot.pie(autopct='%1.0f%%', shadow=True, labels=None,
                           pctdistance=0.7, ax=ax2, explode=explode,
                           textprops={'fontsize': 8}, figsize=(7, 7), **kwargs)
# changing to donut chart
my_circle = plt.Circle((0, 0), 0.5, color='#000038')
p = plt.gcf()
p.gca().add_artist(my_circle)
# changing label
ax2.set_ylabel(None)
ax2.text(-0.23, -0.05, '2020', color='.85', fontsize=12)

# plot 3

# plotting line plot
ax3 = fig.add_subplot(gs[1, 0])
df_wrld_percent.loc[1990:].plot(ax=ax3, style='>-.', markersize=4,
                                figsize=(8, 5), **kwargs)
ax3.set_ylabel('Electicity Produced (%)')
ax3.set_xticks(range(2000, 2021, 4))
ax3.set_xlim(2000, 2020)

# plot 4

# selecting Year 2020 only
df_2020 = df[df['Year'] == 2020]
# dropping columns that are not needed
df_2020.drop('Year', axis=1, inplace=True)
# setting index
df_2020.set_index("Entity", inplace=True)
# adding Total column
df_2020['Total'] = df_2020.sum(axis=1)
# sorting in descending order
df_2020 = df_2020.sort_values('Total', ascending=False)
# selecting top 15
df_2020_sample = df_2020[:8]
# dropping rows and columns that are not needed
df_2020_sample.drop(['World', 'EU27+1', 'EU-27'], inplace=True)
df_2020_sample.drop('Total', axis=1, inplace=True)

# plotting horizontal bar plot
ax4 = fig.add_subplot(gs[1, 1])
df_2020_sample[::-1].plot.barh(stacked=True, figsize=(8, 5), ax=ax4, **kwargs)
ax4.set_ylabel('Countries')
ax4.set_xticks(range(0, 8000, 1500))
ax4.set_xlim(0, 7750)

# textbox

# creating blank subplot
ax5 = fig.add_subplot(gs[:, 2])
ax5.axis('off')

txt = 'The source of electricity that powers\nour devices and vehicles is \
important\nto consider as we move towards more\neco-friendly options.According\
 to the\narea chart, coal,gas, and oil have been\nthe main sources of \
electricity production\nfor the past 20 years, accounting more\nthan 60%\
The pie chart shows\nthat coal and gas were the most used\n\
sources in 2020, while renewable\nsources contributed very little. The line\n\
plot displays the time trend of each\nsource over two decades, with coal\n\
decreasing but still dominating.\nRenewable sources show some growth\nand \
hope for the environment. The bar\nplot shows that China produces more\n\
electricity from coal than any other\ncountry. This visualization emphasizes\n\
the importance of transitioning to\nsustainable sources of electricity\n\
production to reduce the environmental\nimpact of electricity generation,\n\
especially as we increasingly rely\non electronic devices and eco-friendly\n\
vehicles.'
props = dict(boxstyle='round', facecolor='wheat')
ax5.text(0, 0.08, txt, fontsize=9, bbox=props)

# title
fig.suptitle('Source of Electricity', fontsize=25, color='white')

# blank subplot fior legend
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')
# customising legend
handles, labels = ax1.get_legend_handles_labels()
legend = fig.legend(handles, labels, loc='upper center', title='Source',
                    fancybox=True, shadow=True, borderpad=1, fontsize=7,
                    framealpha=0.3, bbox_to_anchor=(-0.112, -0.12, 1, 1),
                    labelcolor='linecolor')
plt.setp(legend.get_title(), color='.85')

# show the plot
plt.show()
