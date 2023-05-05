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

# cleaning

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
gs = plt.GridSpec(2, 3, figure=fig, width_ratios=[1, 1, 0.75])


# seting theme
rc = {'axes.facecolor': '#1221a6', 'text.color': 'black', 'axes.labelcolor':
      '.85', 'xtick.color': '.75', 'ytick.color': '.75', 'axes.edgecolor':
      'black', 'grid.color': '.7'}
sns.set_theme(font='Georgia', font_scale=0.8, rc=rc)


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
titl = 'Cummilative Percentage of Electricity\nProduced from Sources Worldwide'
ax1.set_title(titl, color='white')

# plot 2

# plotting pie chart
ax2 = fig.add_subplot(gs[0, 1])
explode = [0.2 for i in range(len(df_wrld.loc[2020]))]

df_wrld.loc[2020].plot.pie(autopct='%1.0f%%',
                           shadow=True,
                           labels=None,
                           pctdistance=0.65,
                           figsize=(7, 7),
                           ax=ax2,
                           explode=explode,
                           textprops={'fontsize': 7, 'fontweight': 'bold'},
                           wedgeprops={'edgecolor': '0.85', 'linewidth': 0.5},
                           **kwargs)

# changing to donut chart
my_circle = plt.Circle((0, 0), 0.45, color='#000038')
p = plt.gcf()
p.gca().add_artist(my_circle)

# changing label
ax2.set_ylabel(None)
ax2.set_xlabel('2020')
# title
titl2 = 'Percentage of Electricity Produced\nfrom Sources Worldwide in 2020'
ax2.set_title(titl2, color='white')

# plot 3

# plotting line plot
ax3 = fig.add_subplot(gs[1, 0])

df_wrld_percent.loc[1990:].plot(style='>-',
                                lw=1.5,
                                markersize=2.5,
                                figsize=(8, 5),
                                ax=ax3,
                                **kwargs)

ax3.set_ylabel('Electicity Produced (%)')
ax3.set_xticks(range(2000, 2021, 4))
ax3.set_xlim(2000, 2020)
titl3 = 'Percentage of Electricity Produced\nfrom Sources Worldwide'
ax3.set_title(titl3, color='white')

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

df_2020_sample[::-1].plot.barh(stacked=True,
                               figsize=(8, 5),
                               ax=ax4,
                               edgecolor='None',
                               **kwargs)

ax4.set_xlabel('Electicity Produced (TWh)')
ax4.set_ylabel('Countries')
ax4.set_xticks(range(0, 8000, 1500))
ax4.set_xlim(0, 7750)
titl4 = 'Electricity Produced from\nSources in 2020'
ax4.set_title(titl4, color='white')

# textbox

# creating blank subplot
ax5 = fig.add_subplot(gs[:, 2])
ax5.axis('off')

txt = 'BRIEF DESCRIPTION:\n\nThe source of electricity that powers our\n\
devices and vehicles is important to consider\nas we move towards a more \
electronic\nsociety.\n\nAccording to the area chart, coal, gas, and oil\nhave \
been the main sources of electricity\nproduction for the past 20 years, \
accounting\nmore than 60%.The pie chart shows that coal\nand gas were the most\
 used sources in 2020,\nwhile renewable sources still contributed very\n\
little. The line plot displays the time trend of\neach source over two \
decades, we see coal\ndecreasing but still dominating and the\nrenewable \
sources show some growth and\ngives hope for the environment. The bar plot\n\
shows that China produces more electricity\nfrom coal alone than any other \
country.\n\nThis Infographics visualization emphasizes\nthe importance of \
transitioning to sustainable\nsources of electricity production to reduce\n\
the environmental impact of electricity\nproduction, especially as we \
increasingly\nrely on electronic devices and vehicles.'
props = dict(boxstyle='round', facecolor='wheat', edgecolor='black')
ax5.text(0, -0.02, txt, fontsize=8.5, bbox=props)

# shorthand explain box
sh = '% = Percentage\nTWh = Terawatt hour'
fig.text(0.87, 0.01, sh, fontsize=7.5, color='.65')

# title, name and student id
title = 'Is Electricity Production Eco-Friendly?'
fig.suptitle(title, fontsize=25, color='white', weight='bold')

namenid = 'Name          : Aaron Modiyil Joseph\nStudent ID : 22018497'
props = dict(boxstyle='round4', facecolor='wheat', edgecolor='black')
fig.text(0.73, 0.85, namenid, fontsize=9, bbox=props)

# customising legen5
handles, labels = ax1.get_legend_handles_labels()
legend = fig.legend(handles, labels,
                    loc='upper center',
                    title='Source',
                    fancybox=True,
                    shadow=True,
                    borderpad=0.5,
                    fontsize=8,
                    framealpha=0.1,
                    bbox_to_anchor=(-0.111, -0.21, 1, 1),
                    labelcolor='linecolor')
plt.setp(legend.get_title(), color='.85')

# saving figure
fig.savefig('22018497.png', dpi=300, bbox_inches="tight")

# show the plot
plt.show()
