
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[14]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[3]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[15]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    df = pd.DataFrame([[np.nan, np.nan]], columns=["State", "RegionName"])
    regiondata = pd.read_csv('university_towns.txt', sep="\n", header=None)
    regiondata.columns=['RegionName']
    for x in regiondata.RegionName:
        if "edit" in x:
            state = x[:x.find('[')]
        else:
            region = x[:x.find(' (')]
            newdf = pd.DataFrame([[state, region]], columns=["State", "RegionName"])
            df = df.append(newdf, ignore_index=True)

    df = df.dropna()
    df.reset_index(drop=True, inplace=True)
    return df

get_list_of_university_towns()


# In[16]:

def get_recession_start():
    xl = pd.ExcelFile("gdplev.xls")
    gdp = xl.parse(xl.sheet_names[0], skiprows = 7, parse_cols="E,G")
    gdp.columns=['Quarter', 'GDP']
    gdp = gdp.drop(gdp[gdp.Quarter.str[0] == "1"].index)
    gdp.reset_index(drop=True, inplace=True)
    gdp['RecessionStart'] = ((gdp['GDP'].shift(1) > gdp['GDP']) & (gdp['GDP'] > gdp['GDP'].shift(-1)))
    gdpRecStart = gdp.drop(gdp[gdp.RecessionStart == False].index)
    gdpRecStart.reset_index(drop=True, inplace=True)
    
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    return gdpRecStart.Quarter[0]

get_recession_start()


# In[17]:

def get_recession_end():
    recstart = get_recession_start()
    xl = pd.ExcelFile("gdplev.xls")
    gdp = xl.parse(xl.sheet_names[0], skiprows = 7, parse_cols="E,G")
    gdp.columns=['Quarter', 'GDP']
    gdp = gdp.drop(gdp[gdp.Quarter.str[0] == "1"].index)
    gdp.reset_index(drop=True, inplace=True)
    startidx = gdp[gdp.Quarter == recstart].index[0]
    gdp['Growth'] = (gdp['GDP'] >= gdp['GDP'].shift(1))
    gdp['RecessionEnd'] = ((gdp['Growth']) & (gdp['Growth'].shift(1)))
    gdp = gdp.iloc[startidx:]
    gdpRecEnd = gdp.drop(gdp[gdp.RecessionEnd == False].index)
    gdpRecEnd.reset_index(drop=True, inplace=True)
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
       
    return gdpRecEnd.Quarter[0]

get_recession_end()


# In[18]:

def get_recession_bottom():
    recstart = get_recession_start()
    recend = get_recession_end()
    xl = pd.ExcelFile("gdplev.xls")
    gdp = xl.parse(xl.sheet_names[0], skiprows = 7, parse_cols="E,G")
    gdp.columns=['Quarter', 'GDP']
    gdp = gdp.drop(gdp[gdp.Quarter.str[0] == "1"].index)
    gdp.reset_index(drop=True, inplace=True)
    startidx = gdp[gdp.Quarter == recstart].index[0]
    endidx = gdp[gdp.Quarter == recend].index[0]
    gdp = gdp.iloc[startidx:endidx+1]
    gdp.reset_index(drop=True, inplace=True)
    minidx = gdp[gdp.GDP == min(gdp.GDP)].index[0]
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    return gdp.Quarter[minidx]

get_recession_bottom()


# In[19]:

def convert_housing_data_to_quarters():
    xl = pd.ExcelFile("gdplev.xls")
    gdp = xl.parse(xl.sheet_names[0], skiprows = 7, parse_cols="E,G")
    gdp.columns=['Quarter', 'GDP']
    gdp = gdp.drop(gdp[gdp.Quarter.str[0] == "1"].index)
    gdp.reset_index(drop=True, inplace=True)
    df = pd.read_csv("City_Zhvi_AllHomes.csv")
    df = df.replace({"State": states})
    cols = [c for c in df.columns if c[:2] != "19"]
    df = df[cols]
    df.drop('RegionID', axis=1, inplace=True)
    df.drop('Metro', axis=1, inplace=True)
    df.drop('CountyName', axis=1, inplace=True)
    df.drop('SizeRank', axis=1, inplace=True)
    df.set_index(['State', 'RegionName'], inplace=True)
    df.sort_index(inplace=True)
    for q in gdp.Quarter:
        df[q] = df.iloc[:,:3].mean(axis=1)
        cols = [0,1,2]
        df.drop(df.columns[cols],axis=1,inplace=True)
    df['2016q3'] = df.iloc[:,:2].mean(axis=1)
    cols = [0,1]
    df.drop(df.columns[cols],axis=1,inplace=True)

    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    return df

convert_housing_data_to_quarters()


# In[21]:

def run_ttest():
    ul = get_list_of_university_towns()
    hd = convert_housing_data_to_quarters()
    hd['PriceRatio'] = hd['2008q2'].div(hd['2009q2'])
    hd = hd[['PriceRatio']]
    dfut = pd.merge(ul, hd, left_on=['State', 'RegionName'], right_index=True, how='inner')
    nu_idx = hd.index - dfut.index
    dfnut = hd.ix[nu_idx]
    dfut.dropna(axis=0,inplace=True)
    dfnut.dropna(axis=0,inplace=True)
    dfut.set_index(['State', 'RegionName'], inplace=True)
    utmean = dfut['PriceRatio'].mean()
    nutmean = dfnut['PriceRatio'].mean()
    stat=ttest_ind(dfut['PriceRatio'], dfnut['PriceRatio'])
    ut_better = (utmean < nutmean)
    different = (stat.pvalue < 0.01 and ut_better)
    if (ut_better):
        better = "university town"
    else:
        better = "non-university town"
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    return (different, stat.pvalue, better)

run_ttest()


# In[ ]:




# In[ ]:



