#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 10:11:17 2021

@author: dfox
"""

"""
Construct a histogram of the distribution of heights using the BMXHT variable 
in the NHANES sample.
"""

import seaborn as sns
import pandas as pd

da = pd.read_csv("nhanes_2015_2016.csv")

sns.distplot(da.BMXHT.dropna(), kde=False)

