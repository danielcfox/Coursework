#!/usr/bin/env python
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[2]:


import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[3]:


get_ipython().run_line_magic('matplotlib', 'notebook')

def buildval(df, colname):
    df = df[df['Data_Value'] == df[colname]]
    df.reset_index(inplace=True)
    df.drop_duplicates(subset='MonthDay', inplace=True)
    df[colname] = df['Data_Value']*0.1
    df['Date'] = df['Date'].map(lambda x: x.replace(year=2015))  
    cols_to_keep = ['MonthDay', 'Date', colname]
    df = df[cols_to_keep]
    return(df)

rawdf = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
rawdf['DateText'] = rawdf['Date']
rawdf['Date'] = pd.to_datetime(rawdf['Date'])

rawdf['Year'] = rawdf.Date.dt.year
rawdf['Month'] = rawdf.Date.dt.month
rawdf['Day'] = rawdf.Date.dt.day
rawdf['MonthDay'] = rawdf['DateText'].map(lambda x: x[5:])
rawdf = rawdf[rawdf.MonthDay != '02-29']
rawdf = rawdf.sort_values(by=['MonthDay', 'Year'])

df_feb20 = rawdf[rawdf.MonthDay == '02-20']

df_04_14 = rawdf[rawdf.Year != 2015]
df_04_14_max = df_04_14[df_04_14.Element == 'TMAX']
df_04_14_min = df_04_14[df_04_14.Element == 'TMIN']

df_15 = rawdf[rawdf.Year == 2015]
df_15_max = df_15[df_15.Element == 'TMAX']
df_15_min = df_15[df_15.Element == 'TMIN']

df_15_h = df_15_max.set_index('MonthDay')
df_15_h['High2015'] = df_15_h.groupby(df_15_h.index, sort=True)['Data_Value'].max()
df_15_h = buildval(df_15_h, 'High2015')

df_15_l = df_15_min.set_index('MonthDay')
df_15_l['Low2015'] = df_15_l.groupby(df_15_l.index, sort=True)['Data_Value'].min()
df_15_l = buildval(df_15_l, 'Low2015')

df_04_14_rh = df_04_14_max.set_index('MonthDay')
df_04_14_rh['RecordHigh'] = df_04_14_rh.groupby(df_04_14_rh.index, sort=True)['Data_Value'].max()
df_04_14_rh = buildval(df_04_14_rh, 'RecordHigh')

df_04_14_rl = df_04_14_min.set_index('MonthDay')
df_04_14_rl['RecordLow'] = df_04_14_rl.groupby(df_04_14_rl.index, sort=True)['Data_Value'].min()
df_04_14_rl = buildval(df_04_14_rl, 'RecordLow')

df_all = df_15_h.merge(df_15_l)
df_all = df_all.merge(df_04_14_rh)
df_all = df_all.merge(df_04_14_rl)

plt.figure()
rhlist = df_all['RecordHigh'].tolist()
rllist = df_all['RecordLow'].tolist()
datelist = df_all['Date'].tolist()


plt.plot(datelist, rhlist, '-g', label='Record High (2005-2014)')
plt.plot(datelist, rllist, '-c', label='Record Low (2005-2014)')

plt.gca().fill_between(datelist, rhlist, rllist, facecolor='gray', alpha=0.25)

loc, labs = plt.xticks()

plt.xticks([loc[0], loc[0]+31, loc[0]+59, loc[0]+90, loc[0]+120, loc[0]+151, 
            loc[0]+181, loc[0]+212, loc[0]+243, loc[0]+273, loc[0]+304, loc[0]+334, loc[0]+365],
        ['       Jan', '       Feb', '       Mar', '       Apr', '       May', '       Jun', 
         '       Jul', '       Aug', '       Sep', '       Oct', '       Nov', '       Dec', ''])

df_15rh = df_all[df_all['RecordHigh'] < df_all['High2015']]
df_15rl = df_all[df_all['RecordLow'] > df_all['Low2015']]

rh15list = df_15rh['High2015'].tolist()
rhdatelist = df_15rh['Date'].tolist()
rl15list = df_15rl['Low2015'].tolist()
rldatelist = df_15rl['Date'].tolist()

plt.scatter(rhdatelist, rh15list, s=10, c='r', label='2015 Record High')
plt.scatter(rldatelist, rl15list, s=10, c='b', label='2015 Record Low')

plt.title("Record High and Low Temperatures Near Ann Arbor, MI Area")

plt.legend(loc='best')

# Farenheit axis
ax = plt.subplot(111)
ax2 = ax.twinx()
ax.set_ylabel('Temperature (Celsius)')
ax2.set_ylabel('Temperature (Farenheit)')
T_f = lambda T_c: T_c*1.8 + 32.0

ymin, ymax = ax.get_ylim()
ax2.set_ylim((T_f(ymin),T_f(ymax)))
ax2.plot([],[])



# In[ ]:




