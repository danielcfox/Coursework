#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 10:11:17 2021

@author: dfox
"""

"""
The participants can be clustered into "maked variance units" (MVU) based on
every combination of the variables SDMVSTRA and SDMVPSU. Calculate the mean age
(RIDAGEYR), height (BMXHT), and BMI (BMXBMI) for each gender (RIAGENDR),
within each MVU, and report the ratio between the largest and smallest mean
(e.g. for height) across the MVUs.
Calculate the inter-quartile range (IQR) for age, height, and BMI for each 
gender and each MVU. Report the ratio between the largest and smalles IQR 
across the MVUs.
"""

import pandas as pd
import seaborn as sns

da = pd.read_csv("nhanes_2015_2016.csv")

#for SDMVPSU in range(1, 3):
#    for SDMVSTRA in range(119, 134):
#        damvu = da[(da.SDMVPSU == SDMVPSU) & (da.SDMVSTRA == SDMVSTRA)]

sexdict = {1 : "men", 2 : "women"}
da["RIAGENDRx"] = da.RIAGENDR.replace(sexdict)

damvuq1 = da.groupby(['RIAGENDRx', 'SDMVPSU', 'SDMVSTRA']).quantile(0.75)
damvuq1 = damvuq1[['RIDAGEYR', 'BMXHT', 'BMXBMI']]
print("")
print("First quartile:")
print("")
print(damvuq1)

damvuq3 = da.groupby(['RIAGENDRx', 'SDMVPSU', 'SDMVSTRA']).quantile(0.25)
damvuq3 = damvuq3[['RIDAGEYR', 'BMXHT', 'BMXBMI']]
print("")
print("Third quartile:")
print("")
print(damvuq3)

damvuiqrr = damvuq1 - damvuq3
print("")
print("IQR range:")
print("")
print(damvuiqrr)

damvuiqrr.reset_index(inplace=True)
dmen = damvuiqrr[damvuiqrr['RIAGENDRx'] == "men"]
dwomen = damvuiqrr[damvuiqrr['RIAGENDRx'] == "women"]

print("")
print("Ratios of largest to smallest IQR range across MVUs:")
print("")
print("For men, age range ratio is {}"\
      .format(dmen['RIDAGEYR'].max()/dmen['RIDAGEYR'].min()))
print("For men, height range ratio is {}"\
      .format(dmen['BMXHT'].max()/dmen['BMXHT'].min()))
print("For men, BMI range ratio is {}"\
      .format(dmen['BMXBMI'].max()/dmen['BMXBMI'].min()))
print("")
print("For women, age range ratio is {}"\
      .format(dwomen['RIDAGEYR'].max()/dwomen['RIDAGEYR'].min()))
print("For women, height range ratio is {}"\
      .format(dwomen['BMXHT'].max()/dwomen['BMXHT'].min()))
print("For women, BMI range ratio is {}"\
      .format(dwomen['BMXBMI'].max()/dwomen['BMXBMI'].min()))

sns.distplot(a=dmen['RIDAGEYR'])