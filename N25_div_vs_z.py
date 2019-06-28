__author__ = 'julia'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab

############### that is not working, pandas subclassing has to generate a
######### instance (table, that is accessible) otherwise only reference to
# object will be called, to much stucked Object(object) problem.

original_df = pd.read_excel("fundamentalshifts9_selection.xlsx")

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
mam.drop_columns(["z steps", 'Comment 1', "side peaks", "EL (corrected)", "comment2", "GVD", "CWE central", "2w center", "central2", "divergence", 'category, x,y,z', 'HHG_E in uJ'])
mam.get_label_names()
RESULT = mam.get_new_df()

print(RESULT)

class Sorting_by_parameters:

    def __init__(self,  database, name):
        self.orginal = database
        self.copy = self.orginal.copy()
        self.tricks = []
        self.auswahl1 = []
        self.auswahl2 =[]
        self.auswahl = []
        self.auswahl3 = []
        self.label_set = []
        self.GVD0 = self.copy['GVD in fs^2'] <= 300
        self.GVD300 = self.copy['GVD in fs^2'] > 300
        self.GVD600 = self.copy['GVD in fs^2'] >= 600
        self.GVD900 = self.copy['GVD in fs^2'] > 800

        self.N_CWE = self.copy["Nmax"] > 22
        self.ROM_2 = self.copy["Nmax"] >= 25
        self.EL_low = self.copy['EL on target']<1.8
        self.EL_high = self.copy['EL on target'] >= 1.8
        self.z_1000 = self.copy['z um'] <= 1000.
        self.z_2000 = self.copy['z um'] > 1000.
        self.z_3000 = self.copy['z um'] > 2000.
        self.day = 20190123

        self.name = name




    def PP_out(self):
        is_out = self.copy["PP in out"] == "out"
       # print(self.copy["PP in out"])
        self.copy = self.copy[is_out][self.copy.columns]
        return self.copy

    def PP_in(self):
        is_in = self.copy["PP in out"] != "out"
       # print(self.copy["PP in out"])
        self.copy = self.copy[is_in][self.copy.columns]
        return self.copy




    def sort_by_day(self):

        day_sort = self.copy["day"] == self.day
        self.copy = self.copy[day_sort][self.copy.columns]
        return self.copy



    def plot_result(self, color, name, auswahl):


        #plt.figure(1)



        auswahl.plot(x = "divergence N=25", y = 'z um', color = color, style = '.', alpha = 0.2, label=name )

        plt.xlabel("divergence [mrad]")
        plt.ylabel("defocusing [um]")
        plt.xlim(1,15)
        #plt.ylim(-1000,4000.)

        #plt.show()


    def reset_auswahl(self):

        self.auswahl = []

        return self.auswahl

    def divergence_different_GVD(self):

        #self.auswahl = self.copy.copy()
        #print(self.auswahl, "erzeugte copy")


        self.auswahl = self.copy[self.GVD0][["z um", "divergence N=25"]]
        #print(self.auswahl, "auswahl")
        #print(self.copy, "copy")


        self.auswahl1 = self.copy[self.GVD300 != self.GVD600 ][self.copy.columns]

        print(self.auswahl1[["day", "shot"]], "GVD 300-500")

        self.auswahl2 = self.copy[self.GVD600 != self.GVD900][self.copy.columns]
        #print(self.auswahl2["day","shot","z um", "divergence N=25"], "GVD600-800")
        print(set(self.auswahl2.columns))
        print(self.auswahl2[["day", "shot"]], "GVD 600-800")



        self.auswahl3 = self.copy[self.GVD900][self.copy.columns]





        x1=self.auswahl["z um"]
        z1=self.auswahl["divergence N=25"]
        x2=self.auswahl1["z um"]
        z2=self.auswahl1["divergence N=25"]

        x3=self.auswahl2['z um']
        z3=self.auswahl2['divergence N=25']

        x4=self.auswahl3['z um']
        z4 = self.auswahl3["divergence N=25"]

        plt.figure(1)

        plt.scatter(x=x1, y=z1, color='k',label='GVD 0-300', marker = "x", alpha=0.4)
        plt.scatter(x=x2, y=z2, color='r',label='GVD 400-500', marker = "+", alpha=0.4)
        plt.scatter(x=x3,y=z3, color="c", label="GVD 600-800", marker ='1', alpha=0.4)
        plt.scatter(x=x4,y=z4, color="m", label="GVD900-1000", marker ='2', alpha=0.4)
        plt.legend(loc='upper left')
        pylab.ylim(1, 18)
        plt.xlim(-100,5000)
        plt.savefig("N25_divergence"+ "_all"+self.name+".png",  bbox_inches="tight", dpi = 1000)
        plt.show()


















    def high_energy(self, energy):
        above_EL = self.copy["EL on target"] >= energy
        self.copy = self.copy[above_EL][self.copy.columns]
        return self.copy

    def low_energy(self, energy):
        below_EL = self.copy["EL on target"] <= energy
        self.copy = self.copy[below_EL][self.copy.columns]
        print(self.copy["EL on target"], "low Energy range")
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



    def fundamental_for_high_N(self, day):
        self.copy = self.copy[self.ROM_2][['central ROM', 'GVD in fs^2']]
        print(self.copy)
        self.copy.plot(x = "GVD in fs^2", y = "central ROM", color = "b", style = '.', marker = 'o', alpha=0.1 , label = day )
        plt.ylabel("fundamental [nm] for N>28")
        plt.xlabel("GVD [fs^2}")
        plt.ylim(750,840)
        #plt.xlim(0,4500)

        plt.legend()
        plt.show()




sorting1 = Sorting_by_parameters(RESULT, "PPin_highEL")

#sorting1.PP_out()
sorting1.PP_in()
#sorting1.sort_by_day()
sorting1.high_energy(1.8)
#sorting1.low_energy(1.8)
sorting1.divergence_different_GVD()
plt.show()
#sorting1.divergence_vs_defocusing("asdfsa")

#sorting1.GVD_selection('GVD 400-600fs^2 All')
#sorting1.divergence_vs_GVD("N=25, PP out, all energy, all focusing")
#sorting1.GVD_selection()
#sorting1.fundamental_for_high_N("ALL, PP out, N>22")


