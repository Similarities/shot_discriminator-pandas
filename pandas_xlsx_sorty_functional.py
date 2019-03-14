__author__ = 'julia'

import pandas as pd
import numpy as np
import math


df = pd.read_excel("shotlog_shhg_2018_single_sorted.xlsx")

dfs = df.replace(np.nan, True, regex=True)

# exceptional shots // like BP, cal, error
PM_only = dfs['comment1'] == True


# Prepulse out
#PP_out = dfs['PP'] == 'out'


# Pre pulse in
#PP_in = PM_only['PP'] == "in"



#####################################
# Tz minus is towards OAP

# Tz 0
def Tz_range(z0, error_range):
    Tz00 = dfs['Tz relative'] >= z0-error_range
    Tz01 = dfs['Tz relative'] <= z0+error_range
    PP_out = dfs['PP'] == 'out'
    rangeTz= dfs[Tz00 & Tz01 & PM_only & PP_out][['Date', "shotno", 'EL','Tz relative','GVD from 38200 fs^2' ]]
    return rangeTz

def GVD_range(GVD, error_range, z0, error_z):
    GVD00 = dfs['GVD from 38200 fs^2'] >= GVD-error_range
    GVD01 = dfs['GVD from 38200 fs^2'] <= GVD+error_range
    PP_out = dfs['PP'] == 'out'
    Tz00 = dfs['Tz relative'] == z0


    return dfs[GVD01  & PM_only & PP_out &Tz00 ][['Date', "shotno", 'EL','Tz relative','GVD from 38200 fs^2' ]]






# range of Tz: Tz_range(z, error_range)
#selection3 = Tz_range(0, 2000)
#print(selection3)

#selection_GVD0 = GVD_range(0, 1100, 800, 0)
#print(selection_GVD0)

#selection_Tz = Tz_range(1200,200)
#print(selection_Tz)

Tz_discrimination = Tz_range(0,0)
print(Tz_discrimination)



#print to txt
#Tz_discrimination.to_csv('PP_out_GVD0_zscan.txt', header="GVD out", index=None, sep=' ', mode='a')
Tz_discrimination.to_csv('PP_out_GVDscan_at_Tz_200steps.txt', header="GVD_scan", index=None, sep=' ', mode='a')
