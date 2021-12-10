#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 10:11:17 2021

@author: dfox
"""

"""
Restricting to the female population, stratify the subjects into age bands 
no wider than ten years, and construct the distribution of marital status 
within each age band. Within each age band, present the distribution in terms 
of proportions that must sum to 1.
"""

import pandas as pd

da = pd.read_csv("nhanes_2015_2016.csv")

da["DMDMARTLx"] = da.DMDMARTL.replace({1 : "Married", 2 : "Widowed", 
                                       3 : "Divorced", 4 : "Separated",
                                       5 : "Never Married", 
                                       6 : "Living with partner", 
                                       77 : "Refused",
                                       99 : "Don't Know"}).dropna()
da["RIAGENDRx"] = da.RIAGENDR.replace({1 : "Male", 2 : "Female"})

da = da[da.RIAGENDRx == "Female"]
da = da[da.DMDMARTLx != "Don't Know"]

da["agegrp"] = pd.cut(da.RIDAGEYR, list(range(10, 81, 10)))
da = da.groupby("agegrp")["DMDMARTLx"]
da = da.value_counts()
da = da.unstack()
da = da.apply(lambda x: x/x.sum(), axis=1)
da = da.fillna(0)
print(da)

da = pd.read_csv("nhanes_2015_2016.csv")

da["DMDMARTLx"] = da.DMDMARTL.replace({1 : "Married", 2 : "Widowed", 
                                       3 : "Divorced", 4 : "Separated",
                                       5 : "Never Married", 
                                       6 : "Living with partner", 
                                       77 : "Refused",
                                       99 : "Don't Know"}).dropna()
da["RIAGENDRx"] = da.RIAGENDR.replace({1 : "Male", 2 : "Female"})

da = da[da.RIAGENDRx == "Male"]
da = da[da.DMDMARTLx != "Don't Know"]

da["agegrp"] = pd.cut(da.RIDAGEYR, list(range(10, 81, 10)))
da = da.groupby("agegrp")["DMDMARTLx"]
da = da.value_counts()
da = da.unstack()
da = da.apply(lambda x: x/x.sum(), axis=1)
da = da.fillna(0)
print(da)

