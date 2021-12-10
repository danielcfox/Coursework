#!/usr/bin/env python
# coding: utf-8

# # Assignment 4
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# This assignment requires that you to find **at least** two datasets on the web which are related, and that you visualize these datasets to answer a question with the broad topic of **economic activity or measures** (see below) for the region of **Ann Arbor, Michigan, United States**, or **United States** more broadly.
# 
# You can merge these datasets with data from different regions if you like! For instance, you might want to compare **Ann Arbor, Michigan, United States** to Ann Arbor, USA. In that case at least one source file must be about **Ann Arbor, Michigan, United States**.
# 
# You are welcome to choose datasets at your discretion, but keep in mind **they will be shared with your peers**, so choose appropriate datasets. Sensitive, confidential, illicit, and proprietary materials are not good choices for datasets for this assignment. You are welcome to upload datasets of your own as well, and link to them using a third party repository such as github, bitbucket, pastebin, etc. Please be aware of the Coursera terms of service with respect to intellectual property.
# 
# Also, you are welcome to preserve data in its original language, but for the purposes of grading you should provide english translations. You are welcome to provide multiple visuals in different languages if you would like!
# 
# As this assignment is for the whole course, you must incorporate principles discussed in the first week, such as having as high data-ink ratio (Tufte) and aligning with Cairo’s principles of truth, beauty, function, and insight.
# 
# Here are the assignment instructions:
# 
#  * State the region and the domain category that your data sets are about (e.g., **Ann Arbor, Michigan, United States** and **economic activity or measures**).
#  * You must state a question about the domain category and region that you identified as being interesting.
#  * You must provide at least two links to available datasets. These could be links to files such as CSV or Excel files, or links to websites which might have data in tabular form, such as Wikipedia pages.
#  * You must upload an image which addresses the research question you stated. In addition to addressing the question, this visual should follow Cairo's principles of truthfulness, functionality, beauty, and insightfulness.
#  * You must contribute a short (1-2 paragraph) written justification of how your visualization addresses your stated research question.
# 
# What do we mean by **economic activity or measures**?  For this category you might look at the inputs or outputs to the given economy, or major changes in the economy compared to other regions.
# 
# ## Tips
# * Wikipedia is an excellent source of data, and I strongly encourage you to explore it for new data sources.
# * Many governments run open data initiatives at the city, region, and country levels, and these are wonderful resources for localized data sources.
# * Several international agencies, such as the [United Nations](http://data.un.org/), the [World Bank](http://data.worldbank.org/), the [Global Open Data Index](http://index.okfn.org/place/) are other great places to look for data.
# * This assignment requires you to convert and clean datafiles. Check out the discussion forums for tips on how to do this from various sources, and share your successes with your fellow students!
# 
# ## Example
# Looking for an example? Here's what our course assistant put together for the **Ann Arbor, MI, USA** area using **sports and athletics** as the topic. [Example Solution File](./readonly/Assignment4_example.pdf)

# In[95]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import zipfile

get_ipython().run_line_magic('matplotlib', 'notebook')

#upload "https://www.bls.gov/lpc/special_requests/nonfarm_business.zip" as "nonfarm_business.zip" into Notebook
#upload "https://www.bls.gov/lpc/special_requests/manufacturing.zip" as "manufacturing.zip" into Notebook

with zipfile.ZipFile("nonfarm_business.zip") as z:    
    with z.open("nonfarm_business-annual-series.xlsx") as f:
        nfdf = pd.read_excel(f, sheetname="NFBUS, All persons (Index)", skiprows=6)
nfdf = nfdf[nfdf['Year'] >= 1947]
nfdf['Non-farm business labor productivity'] = nfdf['Labor productivity'] * 100 / nfdf['Labor productivity'].iloc[0]
nfdf['Non-farm business labor hourly compensation (inflation-adjusted)'] = nfdf['Real hourly compensation'] * 100 / nfdf['Real hourly compensation'].iloc[0]

with zipfile.ZipFile("manufacturing.zip") as z:    
    with z.open("manufacturing-annual-series.xlsx") as f:
        mdf = pd.read_excel(f, sheetname="MFG, All persons (Index)", skiprows=6)
mdf = mdf[mdf['Year'] >= 1987]
mdf['Manufacturing labor productivity'] = mdf['Labor productivity'] * nfdf['Non-farm business labor hourly compensation (inflation-adjusted)'].iloc[1987 - 1947] / mdf['Labor productivity'].iloc[0]
mdf['Manufacturing labor hourly compensation (inflation-adjusted)'] = mdf['Real hourly compensation'] * nfdf['Non-farm business labor hourly compensation (inflation-adjusted)'].iloc[1987 - 1947] / mdf['Real hourly compensation'].iloc[0]

nfdf = nfdf[['Year', 'Non-farm business labor productivity', 'Non-farm business labor hourly compensation (inflation-adjusted)']]
nfdf['Year'] = nfdf['Year'].astype(int)
nfdf.set_index(['Year'], inplace=True)

mdf = mdf[['Year', 'Manufacturing labor productivity', 'Manufacturing labor hourly compensation (inflation-adjusted)']]
mdf['Year'] = mdf['Year'].astype(int)
mdf.set_index(['Year'], inplace=True)

df = mdf.join(nfdf, how='outer')

ax = df.plot(title='Productivity vs. Compensation, Manufacturing and Non-farm business sectors (1947 - 2016)',
            figsize = (10, 5.625), style = ['-', '--', '-', '--'], color='bbrr');
ax.set_ylabel("Index\n(Non-farm business labor 1947 = 100)\n(Manufacturing labor 1987 = {:f})".format(df['Non-farm business labor hourly compensation (inflation-adjusted)'].iloc[1987 - 1947]))

# see http://www.epi.org/publication/understanding-the-historic-divergence-between-productivity-and-a-typical-workers-pay-why-it-matters-and-why-its-real/
# for further analysis


# In[ ]:




