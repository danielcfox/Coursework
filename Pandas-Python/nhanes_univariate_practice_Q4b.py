#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 10:11:17 2021

@author: dfox
"""

"""
Make side-by-side boxplots of the two systolic blood pressure variables.
"""

import seaborn as sns
import pandas as pd

da = pd.read_csv("nhanes_2015_2016.csv")

dap = da.loc[:, ["BPXSY1", "BPXSY2"]]

sns.boxplot(data=dap).set_ylabel("Blood pressure in mm/Hg")


