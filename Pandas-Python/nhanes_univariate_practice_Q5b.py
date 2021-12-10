#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 10:11:17 2021

@author: dfox
"""

"""
Construct a frequency table of household sizes for people within each 
educational attainment category (the relevant variable is DMDEDUC2).
Convert the frequencies to proportions.
Restrict the sample to people between 30 and 40 years of age. Then calculate
the median household size for women and men within each level of educational 
attainment.
"""

import pandas as pd

da = pd.read_csv("nhanes_2015_2016.csv")

edudict = {1 : "<9",
           2 : "9-11",
           3 : "HS/GED",
           4 : "Some College/AA",
           5 : "College",
           7 : "Refused",
           9: "Don't Know"}

sexdict = {1 : "men", 2 : "women"}

da = da[da.DMDEDUC2 != 7]
da = da[da.DMDEDUC2 != 9]
da = da[da.RIDAGEYR >= 30]
da = da[da.RIDAGEYR < 40]

for sex in range(1, 3):
    dasex = da[da['RIAGENDR']==sex]
    for edu in range(1, 6):
        dae = dasex[dasex["DMDEDUC2"]==edu]
        das = dae["DMDHHSIZ"].value_counts(sort=False)
#        print(das)
        total = das.sum()
        med_loc_lower = (total / 2)
        if total % 2 == 0:
            med_loc_higher = med_loc_lower + 1
        else:
            med_loc_higher = med_loc_lower
        sum = 0
        for hhsize in range(1, 8):
            if hhsize in das:
                sum += das[hhsize]
            if sum >= med_loc_lower:
                if sum >= med_loc_higher:
                    median = float(hhsize)
                else:
                    median = hhsize+0.5
                break
                
        print("median household size for {} education level {} is {}"\
              .format(sexdict[sex], edudict[edu], median))
