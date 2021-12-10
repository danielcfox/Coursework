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
"""

import pandas as pd

da = pd.read_csv("nhanes_2015_2016.csv")

#for SDMVPSU in range(1, 3):
#    for SDMVSTRA in range(119, 134):
#        damvu = da[(da.SDMVPSU == SDMVPSU) & (da.SDMVSTRA == SDMVSTRA)]

sexdict = {1 : "men", 2 : "women"}
da["RIAGENDRx"] = da.RIAGENDR.replace(sexdict)

damvucl = da.groupby(['RIAGENDRx', 'SDMVPSU', 'SDMVSTRA']).mean()
damvucl = damvucl[['RIDAGEYR', 'BMXHT', 'BMXBMI']]
print(damvucl)

damvucl.reset_index(inplace=True)
damvuclmen = damvucl[damvucl['RIAGENDRx'] == "men"]
damvuclwomen = damvucl[damvucl['RIAGENDRx'] == "women"]

print("")
print("Ratios of largest to smallest means across MVUs:")
print("")
print("For men, age ratio is {}"\
      .format(damvuclmen['RIDAGEYR'].max()/damvuclmen['RIDAGEYR'].min()))
print("For men, height ratio is {}"\
      .format(damvuclmen['BMXHT'].max()/damvuclmen['BMXHT'].min()))
print("For men, BMI ratio is {}"\
      .format(damvuclmen['BMXBMI'].max()/damvuclmen['BMXBMI'].min()))
print("")
print("For women, age ratio is {}"\
      .format(damvuclwomen['RIDAGEYR'].max()/damvuclwomen['RIDAGEYR'].min()))
print("For women, height ratio is {}"\
      .format(damvuclwomen['BMXHT'].max()/damvuclwomen['BMXHT'].min()))
print("For women, BMI ratio is {}"\
      .format(damvuclwomen['BMXBMI'].max()/damvuclwomen['BMXBMI'].min()))
