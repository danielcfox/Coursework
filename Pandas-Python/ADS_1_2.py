
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.2** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[19]:

import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df


# ### Question 0 (Example)
# 
# What is the first country in df?
# 
# *This function should return a Series.*

# In[2]:

# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 


# ### Question 1
# Which country has won the most gold medals in summer games?
# 
# *This function should return a single string value.*

# In[13]:

def answer_one():
    max_gold = df.where(df['Gold'] == max(df['Gold']))
    max_gold = max_gold.dropna()
    return max_gold.index[0]

answer_one()


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# In[32]:

def answer_two():
    max_num = max(abs(df['Gold']-df['Gold.1']))
    max_diff = df.where(abs(df['Gold']-df['Gold.1']) == max_num)
    max_diff = max_diff.dropna()
    return max_diff.index[0]

answer_two()


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

# In[270]:

def answer_three():
    osw = df.where((df['Gold'] > 0) & (df['Gold.1'] > 0))
    osw = osw.dropna()
    max_ratio_num = max(abs((osw['Gold']-osw['Gold.1']) / (osw['Gold.2'])))
    max_ratio = osw.where(abs((osw['Gold']-osw['Gold.1']) / (osw['Gold.2'])) == max_ratio_num)
    max_ratio = max_ratio.dropna()
    return max_ratio.index[0]

answer_three()


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created.
# 
# *This function should return a Series named `Points` of length 146*

# In[271]:

def answer_four():
    points_num = df['Gold.2'] * 3 + df['Silver.2'] * 2 + df['Bronze.2']
    Points = pd.Series(points_num)
    return Points

answer_four()


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov/popest/data/counties/totals/2015/CO-EST2015-alldata.html). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](http://www.census.gov/popest/data/counties/totals/2015/files/CO-EST2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*

# In[80]:

census_df = pd.read_csv('census.csv')
census_df.head()


# In[120]:

def answer_five():
    max = 0
    maxcostatename = ''
    # create series of states
    sts = census_df.where(census_df["SUMLEV"] == 40)
    sts = sts.dropna()
    for stname in sts["STNAME"]:
        st = census_df.where(census_df["STNAME"] == stname)
        st = st.dropna()
        nr = st["STNAME"].count()
        co = st.where(st["SUMLEV"] == 50)
        co = co.dropna()
        nc = co["SUMLEV"].count()
        if (nc > max):
            max = nc
            maxcostatename = stname
    return maxcostatename
        
answer_five()


# ### Question 6
# Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
# 
# *This function should return a list of string values.*

# In[269]:

def answer_six():
    maxcostatename = ['', '', '']
    sts = census_df.where(census_df["SUMLEV"] == 40)
    sts = sts.dropna()
    stpopdict = {}
    stpops = pd.Series(stpopdict)
    for stname in sts["STNAME"]:
        cos = census_df.where((census_df["STNAME"] == stname) & (census_df["SUMLEV"] == 50))
        cos = cos.dropna()
        cos = cos.sort("CENSUS2010POP", ascending=False)
        cos = cos.reset_index()
        # state population only looks at 3 largest counties
        stpop = cos["CENSUS2010POP"][0]
        if (cos["CENSUS2010POP"].count() > 1):
            stpop += cos["CENSUS2010POP"][1]
        if (cos["CENSUS2010POP"].count() > 2):
            stpop += cos["CENSUS2010POP"][2]
        stpopdict[stname] = stpop
        
    # each state pop goes into dictionary, take max then delete, take max again, then delete, tax max again
    maxpop = max(stpopdict, key=stpopdict.get)
    maxcostatename[0] = maxpop
    del stpopdict[maxpop]
    maxpop = max(stpopdict, key=stpopdict.get)
    maxcostatename[1] = maxpop
    del stpopdict[maxpop]
    maxpop = max(stpopdict, key=stpopdict.get)
    maxcostatename[2] = maxpop
    return maxcostatename

answer_six()


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 
# *This function should return a single string value.*

# In[267]:

def answer_seven():
    cos = census_df.where(census_df["SUMLEV"] == 50)
    cos = cos.dropna()
    cos = cos.reset_index()
    i = 0
    max_diff = 0
    max_diff_index = 0
    while i < len(cos):
        poplist = [cos["POPESTIMATE2010"][i], 
                   cos["POPESTIMATE2011"][i],
                   cos["POPESTIMATE2012"][i],
                   cos["POPESTIMATE2013"][i],
                   cos["POPESTIMATE2014"][i],
                   cos["POPESTIMATE2015"][i]]
        pop_diff = max(poplist)-min(poplist)
        if (pop_diff > max_diff):
            max_diff = pop_diff
            max_diff_index = i
            max_poplist = poplist
        i += 1
    return cos["CTYNAME"][max_diff_index]
        
answer_seven()


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[266]:

def answer_eight():
    reg = census_df.where((census_df.CTYNAME.str.find("Washington") == 0) &
                          ((census_df["REGION"] == 1) | (census_df["REGION"] == 2)) &
                          (census_df["POPESTIMATE2015"] > census_df["POPESTIMATE2014"]))
    reg = reg.dropna()
    reg = reg[["STNAME", "CTYNAME"]]
    return reg

answer_eight()


# In[ ]:



