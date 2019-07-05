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
        #self.copy = self.copy.replace(np.nan, True, regex=True)
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
mam.drop_columns(["z steps", 'Comment 1', "side peaks", "EL (corrected)", "comment2", "GVD", "CWE central", "2w center", "central2", "divergence", 'category, x,y,z', 'HHG_E in uJ full range'])
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
        self.GVDneg = self.copy['GVD in fs^2'] < 0
        self.GVD0 = self.copy['GVD in fs^2'] < 301
        self.GVD300 = self.copy['GVD in fs^2'] > 300
        self.GVD600 = self.copy['GVD in fs^2'] <= 601
        self.GVD900 = self.copy['GVD in fs^2'] >= 900

        self.N_CWE = self.copy["Nmax"] > 22
        self.ROM_2 = self.copy["Nmax"] >= 25
        self.EL_low = self.copy['EL on target']<1.8
        self.EL_high = self.copy['EL on target'] >= 1.8
        self.z_1000 = self.copy['z um'] <= 1000.
        self.z_2000 = self.copy['z um'] > 1000.
        self.z_3000 = self.copy['z um'] > 2000.
        self.auswahl_GVD0 = []
        self.auswahl_GVD600 = []
        self.auswahl_GVD900 = []
        self.auswahl_GVDneg = []

        self.day = int

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




    def sort_by_day(self, day):

        if day == 0:

            self.day = 0

            return self.copy, self.day


        else:
            self.day = day
            day_sort = self.copy["day"] == day
            self.copy = self.copy[day_sort][self.copy.columns]
            #print(self.copy[["day"]])
            return self.copy, self.day






    def reset_auswahl(self):

        self.auswahl = []
        self.auswahl1 = []
        self.auswahl2 = []
        self.auswahl3 = []

        return self.auswahl, self.auswahl1, self.auswahl2, self.auswahl3







    def divergence_different_GVD(self):

        #self.auswahl = self.copy.copy()
        #print(self.auswahl, "erzeugte copy")


        self.auswahl = self.copy[self.GVD0][["z um", "divergence N=25"]]
        print(self.auswahl, "auswahl")
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



        self.reset_auswahl()
















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


    def set_nan_to_number(self, dataframe, C, column_name):


        dataframe[column_name] = dataframe[column_name].replace(np.nan, 0)
        #print(dataframe[[column_name]], "nan inside?")


        return dataframe





    def energy_content_vs_z_highE(self, do_save, energy_column_name):
        auswahl=[]

        self.GVD_selection_dataframe()



        self.auswahl_GVDneg.dropna()
        #self.set_nan_to_number(self.auswahl_GVDneg, 0, "HHG 24nm-34nm")


        self.auswahl_GVD0.dropna()

        #self.set_nan_to_number(self.auswahl_GVD0, 0, "HHG 24nm-34nm")



        #self.set_nan_to_number(self.auswahl_GVD600, 0, "HHG 24nm-34nm")
        self.auswahl_GVD600.dropna()
        self.auswahl_GVD900.dropna()
        #self.set_nan_to_number(self.auswahl_GVD900, 0, "HHG 24nm-34nm")

        #auswahl = self.auswahl[self.copy.columns]
        x_label = "z um"
        y_label= energy_column_name
        name_0 = "GVD 0 -300"
        name_1 = "GVD -600 to 0"
        name_2 = "GVD 400-600"
        name_3 = "GVD 700-1000"
        #print(auswahl, "auswahl")


        self.plot_result( "b", name_0, self.auswahl_GVD0, x_label, y_label)
        self.plot_result( "m", name_1, self.auswahl_GVDneg, x_label, y_label)

        self.plot_result( "g", name_2, self.auswahl_GVD600, x_label, y_label)
        self.plot_result( "r", name_3, self.auswahl_GVD900, x_label, y_label)

        plt.ylim(-0.01,0.4)



        # this call does not work, creates single plots each

        #self.auswahl2.plot(x = x_label, y = y_label, color = "c", style = '.', alpha = 0.2, label=name_2)

        if do_save == True:



            if self.day >0:

                print("picture saved")
                plt.savefig(str(self.day)+y_label+ "_PPout_highE"+".png",  bbox_inches="tight", dpi = 1000)

            else:
                self.day = "ALL"
                print('picture saved')
                plt.savefig(self.day+y_label+ "_PPout_highE"+".png",  bbox_inches="tight", dpi = 1000)

        else:

            print("no picture saved")

        plt.show()
        self.reset_auswahl()

    def GVD_selection_dataframe(self):


        self.auswahl_GVDneg= self.copy[self.GVDneg][self.copy.columns]
        self.auswahl_GVD0 = self.copy[self.GVD0 != self.GVDneg][self.copy.columns]
        self.auswahl_GVD600 = self.copy[ self.GVD600 != self.GVD0][self.copy.columns]
        self.auswahl_GVD900 = self.copy[self.GVD900][self.copy.columns]

        return self.auswahl_GVD0, self.auswahl_GVD600, self.auswahl_GVD900


    def mean_energy_GVD_vs_z(self, do_save, energy_coloumnlabel):

        #parameter_x (liste)

        x_label = "z um"
        z_values = list(range(-40,50))
        scale_factor_x = 100
        energy_column = energy_coloumnlabel

        self.GVD_selection_dataframe()



        self.mean_of_something_vs_something(self.auswahl_GVDneg, z_values, scale_factor_x, x_label, energy_column, energy_coloumnlabel+"[uJ]", "GVD -600 - (-300)")
        self.mean_of_something_vs_something(self.auswahl_GVD0, z_values, scale_factor_x, x_label, energy_column, energy_coloumnlabel+"[uJ]", "GVD 0 - 300")
        self.mean_of_something_vs_something(self.auswahl_GVD600, z_values, scale_factor_x, x_label, energy_column, energy_coloumnlabel+"[uJ]", "GVD 400 - 600")
        self.mean_of_something_vs_something(self.auswahl_GVD900, z_values, scale_factor_x, x_label, energy_column, energy_coloumnlabel+"[uJ]", "GVD 700 - 1100")




        if do_save == True:

            if self.day > 0:
                plt.savefig(str(self.day)+"24nm_34nm_integrated_energy_mean"+ "_PPout_highE"+".png",  bbox_inches="tight", dpi = 1000)
                print("picture saved")
            else:
                self.day = "ALL"
                print("picture_saved")
                plt.savefig(self.day+"24nm_34nm_integrated_energy"+ "_PPout_highE"+".png",  bbox_inches="tight", dpi = 1000)

        else:
            print('no picture saved')

        plt.show()


    def mean_of_something_vs_something(self, auswahl, parameter_x,scale_factor_x, x_label, parameter_sorted, y_label, name):

        #auswahl.sort_values(by=['z um'])



        result_array_z_meanEnergy = np.zeros([1,3])



        self.reset_auswahl()
        #print(auswahl)

        for x in range(0, len(parameter_x)):
            #print(auswahl[x_label])


            criteria = auswahl[x_label] == parameter_x[x]*scale_factor_x
            self.auswahl= auswahl[criteria][parameter_sorted]


            print(auswahl[criteria][parameter_sorted], "entries for mean value")

            mean_var = self.auswahl.mean(axis = 0, skipna = True)
            print(mean_var, "mittelwert")


            std_var=self.auswahl.std()



            if np.isnan(mean_var):

                None

            elif np.isnan(std_var):
                None

            else:

                #print(parameter_x[x]*scale_factor_x, x_label, name)




                result_array_z_meanEnergy = np.vstack((result_array_z_meanEnergy,np.array([parameter_x[x]*scale_factor_x, mean_var, std_var])))

               #print (result_array_z_meanEnergy)



        if len(result_array_z_meanEnergy) < 2:
            print("nothing to plot for mean in: ", name)

        else:


            plt.figure(1)

            errY = result_array_z_meanEnergy[1::,2]
            errX = 200
            #plt.scatter(result_array_z_meanEnergy[1::,0],result_array_z_meanEnergy[1::,1],color = "c", marker=".", label=name)

            plt.errorbar(result_array_z_meanEnergy[1::,0] + errX, result_array_z_meanEnergy[1::,1]+errY,  xerr=errX, yerr=errY, fmt='o', label= name, alpha=0.3)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.legend()


            #print(cleaned






        print(parameter_x[:], "schritte")

        print(result_array_z_meanEnergy[1::], "mean_value for", parameter_sorted, " vs ", x_label, " criteria: ", name)
        result_array_z_meanEnergy = np.zeros([1,3])







    def plot_result(self, color, name, auswahl, x_label, y_label):



        #plt.figure(1)


        #print(auswahl[x_label], "x Achse")
        #print(auswahl[y_label], "y Achse")

        print(auswahl[x_label].count(), "len")
        print(auswahl[y_label].count(), "len y", name)

        if auswahl[x_label].count() == 0:
            print("empty dataframe in:", x_label)

        elif auswahl[y_label].count() == 0:
            print("empty dataframe in:", y_label)

        else:
                  #print(auswahl[[x_label]], auswahl[[y_label]], "in the plot")



            plt.scatter(x = auswahl[x_label], y = auswahl[y_label], color = color, marker = '.', alpha = 0.2, label=name )

            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.legend()

        #plt.xlim(1,15)
        #plt.ylim(-1000,4000.)

        #plt.show()




    def mean_fundamental_GVD_vs_z(self, save_plot, y_label):

        self.GVD_selection_dataframe()

        name_0 = "GVD -600 - 0"
        name_1 = "GVD 0 - 300"
        name_2 = "GVD 400 600"
        name_3 = "GVD 700-1100"

        y_label = y_label
        x_label = "z um"

        parameter_x = list(range(-50, 50))
        #(self, auswahl, parameter_x,scale_factor_x, x_label, parameter_sorted, y_label, name)

        #self.auswahl_GVDneg[y_label].replace(to_replace=0, value=np.nan, regex=True)

        self.auswahl_GVDneg.dropna()
        self.mean_of_something_vs_something(self.auswahl_GVDneg, parameter_x, 100, x_label, y_label, y_label+"[nm]", name_0)


        self.auswahl_GVD0.dropna()
        self.mean_of_something_vs_something(self.auswahl_GVD0, parameter_x, 100, x_label, y_label, y_label+"[nm]", name_1)

        #self.auswahl_GVD600.fillna()
        self.auswahl_GVD600.dropna()
        #print(self.auswahl_GVD600[y_label], "data 600")
       # self.mean_of_something_vs_something(self.auswahl_GVD600, parameter_x, 100, x_label, y_label, y_label+"[nm]", name_2)


        self.auswahl_GVD900.dropna()
        self.mean_of_something_vs_something(self.auswahl_GVD900, parameter_x, 100, x_label, y_label, y_label+"[nm]", name_3)

        plt.ylim(600, 1400)


        if save_plot == True:

            if self.day == 0:
                self.day == "ALL_"

            else:
                self.day = self.day

            print("picture_saved")
            plt.savefig(str(self.day)+y_label+'_mean'+ "_PPout_highE"+".png",  bbox_inches="tight", dpi = 1000)

        else:
            None



        plt.show()








    def fundamental_ROM_single_GVD(self):

        if self.day == 0:
            self.day = "All"

        else:
            self.day = str(self.day)
            self.copy = self.copy[self.ROM_2][['central ROM', 'GVD in fs^2']]
            print(self.copy)
            self.copy.plot(x = "GVD in fs^2", y = "central ROM", color = "b", style = '.', marker = 'o', alpha=0.1 , label = self.day)
            plt.ylabel("fundamental [nm] for N>28")
            plt.xlabel("GVD [fs^2}")
            plt.ylim(750,840)
            #plt.xlim(0,4500)

            plt.legend()
            plt.show()




sorting1 = Sorting_by_parameters(RESULT, "PPin_highEL")

sorting1.PP_out()
#sorting1.PP_in()
sorting1.sort_by_day(0)
sorting1.high_energy(1.8)
#sorting1.low_energy(1.8)
#sorting1.divergence_different_GVD()

############ True argument is call to save picture ##########
############## second argument gives name of column for evaluation (y axis), since for energy two different ranges existing
energy_coloumnlabel = "HHG 24nm-34nm"
#sorting1.energy_content_vs_z_highE(True, energy_coloumnlabel)
#sorting1.mean_energy_GVD_vs_z(True, energy_coloumnlabel)

######## either "central ROM", "central" or "CWE...something"
columname ='central ROM'
sorting1.mean_fundamental_GVD_vs_z(True, columname)


#plt.show()
#sorting1.divergence_vs_defocusing("asdfsa")

#sorting1.GVD_selection('GVD 400-600fs^2 All')
#sorting1.divergence_vs_GVD("N=25, PP out, all energy, all focusing")
#sorting1.GVD_selection()
#sorting1.fundamental_for_high_N("ALL, PP out, N>22")


