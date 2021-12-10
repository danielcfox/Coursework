#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 10:11:17 2021

@author: dfox
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statsmodels.api as sm
import numpy as np

da = pd.read_csv("nhanes_2015_2016.csv")

da["DMDMARTLx"] = da.DMDMARTL.replace({1 : "Married", 2 : "Widowed", 3 : "Divorced", 4 : "Separated",
                                       5 : "Never Married", 6 : "Living with partner", 77 : "Refused",
                                      99 : "Don't Know"}).dropna()

dafreqall = da.DMDMARTLx.value_counts()
print("frequency of marital status for all:")
print(dafreqall)
print(dafreqall / dafreqall.sum())

dawomen = da[da.RIAGENDR == 2] # Women are 2
dafreqwomen = dawomen.DMDMARTLx.value_counts()
print("")
print("frequency of marital status for women:")
print(dafreqwomen)
print(dafreqwomen / dafreqwomen.sum())

damen = da[da.RIAGENDR == 1] # Men are 1
dafreqmen = damen.DMDMARTLx.value_counts()
print("")
print("frequency of marital status for men:")
print(dafreqmen)
print(dafreqmen / dafreqmen.sum())

da30_40 = da[(da.RIDAGEYR >= 30) & (da.RIDAGEYR <= 40)]
dafreqall30_40 = da30_40.DMDMARTLx.value_counts()
print("frequency of marital status for all aged 30-40:")
print(dafreqall30_40)
print(dafreqall30_40 / dafreqall30_40.sum())

dawomen30_40 = dawomen[(dawomen.RIDAGEYR >= 30) & (dawomen.RIDAGEYR <= 40)]
dafreqwomen30_40 = dawomen30_40.DMDMARTLx.value_counts()
print("")
print("frequency of marital status for women aged 30-40:")
print(dafreqwomen30_40)
print(dafreqwomen30_40 / dafreqwomen30_40.sum())

damen30_40 = damen[(damen.RIDAGEYR >= 30) & (damen.RIDAGEYR <= 40)]
dafreqmen30_40 = damen30_40.DMDMARTLx.value_counts()
print("")
print("frequency of marital status for men aged 30-40:")
print(dafreqmen30_40)
print(dafreqmen30_40 / dafreqmen30_40.sum())

# filter out don't know
daws = dawomen[dawomen.DMDMARTL != 99]

daws["agegrp"] = pd.cut(da.RIDAGEYR, list(range(0, 81, 10)))
daws = daws.groupby("agegrp")['DMDMARTLx']
daws = daws.value_counts()
daws = daws.unstack()
daws = daws.apply(lambda x: x/x.sum(), axis=1)
print(daws.to_string(float_format="%.3f"))
