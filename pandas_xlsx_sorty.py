__author__ = 'julia'

import pandas as pd
import numpy as np
import math


df = pd.read_excel("shotlog_shhg_2018_single_sorted.xlsx")

dfs = df.replace(np.nan, True, regex=True)

# exceptional shots // like BP, cal, error
PM_only = dfs['comment1'] == True

# Prepulse out
PP_out = dfs['PP'] == "out"


# Pre pulse in
PP_in = dfs['PP'] == "in"

# GVD at 0
GVD_0 = dfs['GVD from 38200 fs^2'] == 0

# GVD at = 300 fs^2
GVD_p300 = dfs['GVD from 38200 fs^2'] == 300

# GVD at = - 300 fs^2
GVD_m300 = dfs['GVD from 38200 fs^2'] == -300

selection = dfs[PP_out & PM_only & GVD_0][['Date', "shotno", 'EL','Tz relative' ]]
selection2 = dfs[PP_out & PM_only & GVD_p300][['Date', "shotno", 'EL','Tz relative', 'GVD from 38200 fs^2']]
print(selection)

#dwPP = dfs[dfs['PP'] == "out"]
#print(dz0)

selection.to_csv('PP_out_GVD0.txt', header=None, index=None, sep=' ', mode='a')
selection2.to_csv('PP_out_GVD_p300.txt', header=None, index=None, sep=' ', mode='a')