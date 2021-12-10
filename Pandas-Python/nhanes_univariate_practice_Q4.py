#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 10:11:17 2021

@author: dfox
"""

"""
Make a boxplot showing the distribution of within-subject differences between
the first and second systolic blood pressure measurents (BPXSY1 and BPXSY2).
"""

import seaborn as sns
import pandas as pd

da = pd.read_csv("nhanes_2015_2016.csv")

da["BPXSYdiff"] = da.BPXSY2 - da.BPXSY1

da["BPXSYdiff"].dropna()

print(da.BPXSYdiff.describe())

print("")
print("Boxplot for change in systolic blood pressure from second to first"
      + " measurement")
sns.boxplot(data=da.BPXSYdiff)
