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



#####################################
# Tz minus is towards OAP

# Tz 0
def Tz_range(z0, error_range, dataframe):
    Tz00 = dataframe['Tz relative'] >= z0-error_range
    Tz01 = dataframe['Tz relative'] <= z0+error_range
    rangeTz= dataframe[Tz00 & Tz01 ][['Date', "shotno", 'EL','Tz relative','GVD from 38200 fs^2' ]]
    return rangeTz

def GVD_range(GVD, error_range):
    GVD00 = dfs['GVD from 38200 fs^2'] >= GVD-error_range
    GVD01 = dfs['GVD from 38200 fs^2'] <= GVD+error_range

    return dfs[GVD00 & GVD01 & PP_out & PM_only][['Date', "shotno", 'EL','Tz relative','GVD from 38200 fs^2' ]]






# range of Tz: Tz_range(z, error_range)
#selection3 = Tz_range(0, 2000)
#print(selection3)

selection_GVD0 = GVD_range(0, 300)
#print(selection_GVD0)

Tz_discrimination = Tz_range(0,3000, selection_GVD0)
print(Tz_discrimination)



#print to txt
Tz_discrimination.to_csv('PP_out_GVD0_zscan.txt', header="GVD out", index=None, sep=' ', mode='a')
