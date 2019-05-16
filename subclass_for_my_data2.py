__author__ = 'julia'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

############### that is not working, pandas subclassing has to generate a
######### instance (table, that is accessible) otherwise only reference to
# object will be called, to much stucked Object(object) problem.

original_df = pd.read_excel("fundamentalshifts8_selection.xlsx")

class Sort_and_Copy_Dataframe:

    def __init__(self,  database):
        self.orginal = database
        self.copy = self.orginal.copy()
        self.copy = self.copy.replace(np.nan, True, regex=True)
        self.tricks = []
        self.auswahl = []
        self.label_set = []




    def drop_unnamed_columns(self):

        self.auswahl = self.copy.columns.str.match('Unnamed')
        empty_column_index = [i for i, x in enumerate(self.auswahl) if x]

        for i in range(len(empty_column_index)):

            number = empty_column_index[i]

            delete_column = "Unnamed: "+str(number)

            self.copy.drop(labels = [delete_column], axis = 1, inplace = True)

        return self.copy


    def get_label_names(self):
        self.label_set = set(self.copy.columns)
        #print(label_set, "labels in dfs..")
        print("number:", len(self.label_set))
        print(self.label_set)
        #eturn label_set


    def drop_columns(self, trick):

        self.tricks = trick
        self.copy.drop(labels=self.tricks, axis=1, inplace = True)
        self.label_set = set(self.copy.columns)






    def get_new_df(self):

        return self.copy



mam = Sort_and_Copy_Dataframe(original_df)
mam.drop_unnamed_columns()
mam.get_label_names()
mam.drop_columns(["z steps", 'Comment 1', "side peaks", "EL (corrected)", "comment2", "GVD", "CWE central", "2w center", "central2", "divergence", 'category, x,y,z'])
mam.get_label_names()
RESULT = mam.get_new_df()

print(RESULT)

class Sorting_by_parameters:

    def __init__(self,  database):
        self.orginal = database
        self.copy = self.orginal.copy()
        self.tricks = []
        self.auswahl = []
        self.label_set = []
        self.GVD300 = self.copy['GVD in fs^2'] <= 300
        self.GVD600 = self.copy['GVD in fs^2'] <= 600
        self.GVD900 = self.copy['GVD in fs^2'] > 600

    def PP_out(self):
        is_out = self.copy["PP in out"] == "out"
       # print(self.copy["PP in out"])
        self.copy = self.copy[is_out][self.copy.columns]
        return self.copy

    def sort_by_day(self, day):

        day_sort = self.copy["day"] == day
        self.copy = self.copy[day_sort][self.copy.columns]
        return self.copy

    def divergence_vs_defocusing(self, day):


        plt.figure(1)


        self.copy.plot(x = "divergence N=25", y = 'z um', color = "r", style = '.', alpha = 0.2, label = day )
        #self.copy.plot(x = "divergence N=25", y = "z um")
        plt.xlabel("divergence [mrad]")
        plt.ylabel("defocusing [um]")
        plt.xlim(1,15)
        #plt.ylim(-1000,4000.)

        plt.show()

    def high_energy(self, energy):
        above_EL = self.copy["EL on target"] >= energy
        self.copy = self.copy[above_EL][self.copy.columns]
        return self.copy

    def low_energy(self, energy):
        below_EL = self.copy["EL on target"] <= energy
        self.copy = self.copy[below_EL][self.copy.columns]
        return self.copy

    def divergence_vs_GVD(self, day):

        plt.figure(2)
        #print(self.copy["divergence"])
        self.copy.plot(x = "GVD in fs^2", y = "z um", color = "g", style = '.', marker = 'o', alpha=0.1 , label = day )

        plt.ylabel("divergence [mrad]")
        plt.xlabel("GVD [fs^2]")
        plt.xlim(1,20)

        plt.legend()
        plt.show()

    def GVD_selection(self, day):
        self.copy = self.copy[self.GVD600 != self.GVD300][["divergence N=25", "z um"]]
        print(self.copy)


        plt.figure(2)


        self.copy.plot(x = "z um", y = "divergence N=25", color = "b", style = '.', marker = 'o', alpha=0.1 , label = day )
        plt.ylabel("divergence [mrad]")
        plt.xlabel("z [um]")
        plt.ylim(1,20)
        plt.xlim(0,4500)

        plt.legend()
        plt.show()




sorting1 = Sorting_by_parameters(RESULT)
sorting1.PP_out()
#sorting1.sort_by_day("20190130s")
#sorting1.divergence_vs_defocusing("asdfsa")
#sorting1.high_energy(2.2)
sorting1.GVD_selection('GVD 400-600fs^2 All')
#sorting1.divergence_vs_GVD("N=25, PP out, all energy, all focusing")
#sorting1.GVD_selection()



