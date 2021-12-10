
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-text-mining/resources/d9pwm) course resource._
# 
# ---

# # Assignment 1
# 
# In this assignment, you'll be working with messy medical data and using regex to extract relevant infromation from the data. 
# 
# Each line of the `dates.txt` file corresponds to a medical note. Each note has a date that needs to be extracted, but each date is encoded in one of many formats.
# 
# The goal of this assignment is to correctly identify all of the different date variants encoded in this dataset and to properly normalize and sort the dates. 
# 
# Here is a list of some of the variants you might encounter in this dataset:
# * 04/20/2009; 04/20/09; 4/20/09; 4/3/09
# * Mar-20-2009; Mar 20, 2009; March 20, 2009;  Mar. 20, 2009; Mar 20 2009;
# * 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
# * Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
# * Feb 2009; Sep 2009; Oct 2010
# * 6/2008; 12/2009
# * 2009; 2010
# 
# Once you have extracted these date patterns from the text, the next step is to sort them in ascending chronological order accoring to the following rules:
# * Assume all dates in xx/xx/xx format are mm/dd/yy
# * Assume all dates where year is encoded in only two digits are years from the 1900's (e.g. 1/5/89 is January 5th, 1989)
# * If the day is missing (e.g. 9/2009), assume it is the first day of the month (e.g. September 1, 2009).
# * If the month is missing (e.g. 2010), assume it is the first of January of that year (e.g. January 1, 2010).
# * Watch out for potential typos as this is a raw, real-life derived dataset.
# 
# With these rules in mind, find the correct date in each note and return a pandas Series in chronological order of the original Series' indices.
# 
# For example if the original series was this:
# 
#     0    1999
#     1    2010
#     2    1978
#     3    2015
#     4    1985
# 
# Your function should return this:
# 
#     0    2
#     1    4
#     2    0
#     3    1
#     4    3
# 
# Your score will be calculated using [Kendall's tau](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient), a correlation measure for ordinal data.
# 
# *This function should return a Series of length 500 and dtype int.*

# In[2]:

import pandas as pd

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
df


# In[85]:

def date_sorter():
    import re
    
    months = {'Jan' : 1, 'Feb' : 2, 'Mar': 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6, 'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12}
    
    # Your code here
    ddf = df.to_frame()
    ddf.columns = ['note']
    
    for index, row in ddf.iterrows():
        # first find those with named months
        datestrlist = re.findall(r'(?:\d{1,2} )?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.,]* (?:\d{1,2})(?:\w{,2}[., ]+)?\d{2,4}', ddf.at[index, 'note'])
        if (len(datestrlist)):
#            print(index, datestrlist[0])
            ddf.at[index, 'date'] = datestrlist[0]
            daylist = re.findall(r'(\d{1,2} )?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.,]* (?:\d{1,2})(?:\w{,2}[., ]+)?\d{2,4}', datestrlist[0])
            if (len(daylist[0])):
                ddf.at[index, 'day'] = int(daylist[0])
            else:
                daylist = re.findall(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.,]* (\d{1,2})(?:\w{,2}[., ]+)?\d{2,4}', datestrlist[0])
                if (len(daylist) and len(daylist[0])):
                    ddf.at[index, 'day'] = int(daylist[0])
                else:
                    ddf.at[index, 'day'] = 1
            monthlist = re.findall(r'(?:\d{1,2} )?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.,]* (?:\d{1,2})(?:\w{,2}[., ]+)?\d{2,4}', datestrlist[0])
#            print(monthlist)
            ddf.at[index, 'month'] = int(months[monthlist[0][0:3]])
#            ddf['month'].astype(int)
            yearlist = re.findall(r'(?:\d{1,2} )?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.,]* (?:\d{,2}\w{,2}[., ]+)?(\d{4})', datestrlist[0])
            ddf.at[index, 'year'] = int(yearlist[0])
        else:
            # next find those with m(m)(/d(d))/yy(yy)
            datestrlist = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', ddf.at[index, 'note'])
            if (len(datestrlist)):
#                print(index, datestrlist[0])
                ddf.at[index, 'date'] = datestrlist[0]
                yearlist = re.findall(r'\d{1,2}[/-]\d{1,2}[/-](\d{2,4})', datestrlist[0])
                ddf.at[index, 'year'] = int(yearlist[0])
                monthlist = re.findall(r'(\d{1,2})[/-]\d{1,2}[/-]\d{2,4}', datestrlist[0])
                ddf.at[index, 'month'] = int(monthlist[0])
                daylist = re.findall(r'\d{1,2}[/-](\d{1,2})[/-]\d{2,4}', datestrlist[0])
                ddf.at[index, 'day'] = int(daylist[0])
            else:
                # next find those with m(m)/yy(yy)
                datestrlist = re.findall(r'\d{1,2}[/-]\d{2,4}', ddf.at[index, 'note'])
                if (len(datestrlist)):
#                    print(index, datestrlist[0])
                    ddf.at[index, 'date'] = datestrlist[0]
                    yearlist = re.findall(r'\d{1,2}[/-](\d{2,4})', datestrlist[0])
                    year = int(yearlist[0])
                    ddf.at[index, 'year'] = int(yearlist[0])
                    monthlist = re.findall(r'(\d{1,2})[/-]\d{2,4}', datestrlist[0])
                    ddf.at[index, 'month'] = int(monthlist[0])
                    ddf.at[index, 'day'] = 1
                else:
                    # next find those with yyyy
                    yearlist = re.findall(r'\d{4}', ddf.at[index, 'note'])
                    if (len(yearlist)):
#                        print(index, yearlist[0])
                        ddf.at[index, 'date'] = yearlist[0]
                        ddf.at[index, 'year'] = int(yearlist[0])
                        ddf.at[index, 'month'] = 1
                        ddf.at[index, 'day'] = 1
                    else:
                        # should not get here
                        print(index, ddf.at[index, 'note'])
        if (ddf.at[index, 'year'] <= 100):
            ddf.at[index, 'year'] = ddf.at[index, 'year'] + 1900
#        print(ddf.at[index, 'year'])
#        print(ddf.at[index, 'month'])
#        print(ddf.at[index, 'day'])

    ddf.sort_values(['year', 'month', 'day'], inplace=True)
    ddf['orig_index'] = ddf.index
    return ddf['orig_index'] # Your answer here

# date_sorter()


# In[ ]:



