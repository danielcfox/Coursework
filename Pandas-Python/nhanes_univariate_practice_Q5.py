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
"""

import pandas as pd

da = pd.read_csv("nhanes_2015_2016.csv")

da["DMDEDUC2x"] = da.DMDEDUC2.replace({1 : "<9",
                                       2 : "9-11",
                                       3 : "HS/GED",
                                       4 : "Some College/AA",
                                       5 : "College",
                                       7 : "Refused",
                                       9: "Don't Know"}).dropna()
# da["RIAGENDRx"] = da.RIAGENDR.replace({1 : "Male", 2 : "Female"})

#da = da[da.RIAGENDRx == "Female"]
da = da[da.DMDEDUC2x != "Refused"]
da = da[da.DMDEDUC2x != "Don't Know"]

#da["agegrp"] = pd.cut(da.RIDAGEYR, list(range(10, 81, 10)))

da = da.groupby("DMDEDUC2x")["DMDHHSIZ"]
da = da.value_counts()
da = da.unstack()
da = da.apply(lambda x: x/x.sum(), axis=1)
da = da.fillna(0)
print(da)


