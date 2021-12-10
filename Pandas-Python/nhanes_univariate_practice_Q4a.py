#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 10:11:17 2021

@author: dfox
"""

"""
What proportion of the subjects have a lower SBP on the second reading 
compared to the first?
"""

import pandas as pd

da = pd.read_csv("nhanes_2015_2016.csv")

da["BPXSYdiff"] = da.BPXSY2 - da.BPXSY1
da["BPXSYdiff"].dropna()
dal = da[da.BPXSYdiff < 0]

prop_lower = dal.BPXSYdiff.count()/da.BPXSYdiff.count()
print("proportion of lower SBP on second reading is {}".format(prop_lower))

