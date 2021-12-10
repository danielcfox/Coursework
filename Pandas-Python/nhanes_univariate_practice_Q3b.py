#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 10:11:17 2021

@author: dfox
"""

"""
Make separate histograms for the heights of women and men, then make a
side-by-side boxplot showing the heights of women and men.
"""

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

da = pd.read_csv("nhanes_2015_2016.csv")

da["RIAGENDRx"] = da.RIAGENDR.replace({1 : "Male", 2 : "Female"})

daf = da[da.RIAGENDRx == "Female"]
dam = da[da.RIAGENDRx == "Male"]

print("Histogram of heights for women")
sns.distplot(daf.BMXHT.dropna(), kde=False)
plt.show()

print("")
print("Histogram of heights for men")
sns.distplot(dam.BMXHT.dropna(), kde=False)
plt.show()

print("")
print("Boxplots for Men and Women")
sns.boxplot(x="RIAGENDRx", y="BMXHT", data=da)
