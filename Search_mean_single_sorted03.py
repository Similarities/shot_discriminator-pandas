__author__ = 'similarities'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab


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

    def __init__(self,  database, name, save_bool):
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
        self.GVD0_2 = self.copy['GVD in fs^2'] >= 0
        self.GVD300 = self.copy['GVD in fs^2'] > 300
        self.GVD600 = self.copy['GVD in fs^2'] > 300
        self.GVD600_2 = self.copy['GVD in fs^2'] < 700
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
        self.name_original = name
        self.save = save_bool
        self.name_attributes ="_"
        self.marker = int
        self.selection_members = ()


    def reset_name(self):

        self.name = self.name_original

        return self.name




    def PP_out(self):
        is_out = self.copy["PP in out"] == "out"
       # print(self.copy["PP in out"])
        self.copy = self.copy[is_out][self.copy.columns]
        self.name_attributes = self.name_attributes +"PPout"

        return self.copy, self.name_attributes



    def PP_in(self):
        is_in = self.copy["PP in out"] != "out"
       # print(self.copy["PP in out"])
        self.copy = self.copy[is_in][self.copy.columns]
        self.name_attributes = self.name_attributes +"PPin"


        return self.copy, self.name_attributes




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


    def high_energy(self, energy):
        above_EL = self.copy["EL on target"] >= energy
        self.copy = self.copy[above_EL][self.copy.columns]
        self.name_attributes = self.name_attributes +"_highEL"


        return self.copy, self.name_attributes






    def low_energy(self, energy):

        below_EL = self.copy["EL on target"] <= energy

        self.copy = self.copy[below_EL][self.copy.columns]

        print(self.copy["EL on target"], "low Energy range")

        self.name_attributes = self.name_attributes +"_lowEL"


        return self.copy, self.name_attributes





    def set_nan_to_number(self, dataframe, C, column_name):


        dataframe= dataframe.replace({column_name:np.nan},0)

        #print(dataframe[[column_name]], "nan inside?")


        return dataframe




    def all_or_one_day(self):


        if self.day == 0:

            self.day = "_All_"

        else:
            self.day = self.day

        return self.day





    def save_picture(self, y_label):


        self.all_or_one_day()


        if self.save == True:


            print("picture saved:       ",      self.name+str(self.day)+y_label+ self.name_attributes+".png")


            plt.savefig(self.name+str(self.day)+y_label+ self.name_attributes+".png",  bbox_inches="tight", dpi = 1000)



        else:


            print("no picture saved -- set bool to True")




    def energy_content_vs_z_highE(self, energy_column_name):


        self.GVD_selection_dataframe()


        self.auswahl_GVDneg.dropna()


        self.auswahl_GVD0.dropna()


        self.auswahl_GVD600.dropna()

        self.auswahl_GVD900.dropna()



        x_label = "z um"

        y_label= energy_column_name


        self.reset_marker()



        self.plot_together_in_one_graph( "b", self.selection_members[0], self.auswahl_GVDneg, x_label, y_label)

        self.plot_together_in_one_graph( "m", self.selection_members[1], self.auswahl_GVD0, x_label, y_label)

        self.plot_together_in_one_graph( "g", self.selection_members[2], self.auswahl_GVD600, x_label, y_label)

        self.plot_together_in_one_graph( "r", self.selection_members[3], self.auswahl_GVD900, x_label, y_label)






        self.save_picture(y_label)

        self.reset_name_list()


        plt.show()





    def GVD_selection_dataframe(self):


        self.auswahl_GVDneg= self.copy[self.GVDneg][self.copy.columns]


        self.auswahl_GVD0 = self.copy[self.GVD0][self.copy.columns]
        self.auswahl_GVD0 = self.auswahl_GVD0[self.GVD0_2][self.copy.columns]


        self.auswahl_GVD600 = self.copy[self.GVD600_2][self.copy.columns]
        self.auswahl_GVD600 = self.auswahl_GVD600[ self.GVD600][self.copy.columns]


        self.auswahl_GVD900 = self.copy[self.GVD900][self.copy.columns]


        print(self.auswahl_GVDneg[["shot", "z um", "GVD in fs^2"]], "GVD<0")

        print(self.auswahl_GVD0[["shot", "z um", "GVD in fs^2"]], "GVD0")

        print(self.auswahl_GVD600[["shot", "z um", "GVD in fs^2"]], "GVD 600")

        print( self.auswahl_GVD900[["shot", "z um", "GVD in fs^2"]], "GVD900")

        self.selection_members = ("GVD -600 - 0", "GVD 0 - 300","GVD 400 600","GVD 700-1100")


        return self.auswahl_GVDneg, self.auswahl_GVD0, self.auswahl_GVD600, self.auswahl_GVD900, self.selection_members





    def mean_energy_GVD_vs_z(self, energy_coloumnlabel):



        x_label = "z um"

        z_values = list(range(-40,50))

        scale_factor_x = 100

        energy_column = energy_coloumnlabel

        self.GVD_selection_dataframe()



        self.mean_of_something_vs_something(self.auswahl_GVDneg, z_values, scale_factor_x, x_label, energy_column, energy_coloumnlabel+"[uJ]", "GVD -600 - (-300)")

        self.mean_of_something_vs_something(self.auswahl_GVD0, z_values, scale_factor_x, x_label, energy_column, energy_coloumnlabel+"[uJ]", "GVD 0 - 300")

        self.mean_of_something_vs_something(self.auswahl_GVD600, z_values, scale_factor_x, x_label, energy_column, energy_coloumnlabel+"[uJ]", "GVD 400 - 600")

        self.mean_of_something_vs_something(self.auswahl_GVD900, z_values, scale_factor_x, x_label, energy_column, energy_coloumnlabel+"[uJ]", "GVD 700 - 1100")



        self.reset_name()

        self.name = self.name+"mean"

        self.save_picture(energy_coloumnlabel)


        plt.show()







    def mean_of_something_vs_something(self, auswahl, parameter_x, scale_factor_x, x_label, parameter_sorted, y_label, name):

        #auswahl.sort_values(by=['z um'])



        result_array_z_meanEnergy = np.zeros([1,3])

        #print(result_array_z_meanEnergy)

        self.reset_auswahl()

        #print(auswahl, "reseted")

        for x in range(0, len(parameter_x)):
            #print(auswahl[x_label])


            criteria = auswahl[x_label] == parameter_x[x]*scale_factor_x

            self.auswahl= auswahl[criteria][parameter_sorted]


            #print(auswahl[criteria][parameter_sorted], "entries for mean value", parameter_x[x], name)


            mean_var = self.auswahl.mean(axis = 0, skipna = True)

            #print(mean_var, "mittelwert x_paramerter at:", parameter_x[x])
               #print (result_array_z_meanEnergy)


            std_var=self.auswahl.std()




            if np.isnan(mean_var) or mean_var == 0:


                None



            elif np.isnan(std_var):

                None


            else:

                result_array_z_meanEnergy = np.vstack((result_array_z_meanEnergy,np.array([parameter_x[x]*scale_factor_x, mean_var, std_var])))

               #print (result_array_z_meanEnergy)



        if len(result_array_z_meanEnergy) < 1:


            print("nothing to plot for mean in: ", name)



        else:


            plt.figure(3)

            errY = result_array_z_meanEnergy[1::,2]

            errX = 200
            #plt.scatter(result_array_z_meanEnergy[1::,0],result_array_z_meanEnergy[1::,1],color = "c", marker=".", label=name)

            plt.errorbar(result_array_z_meanEnergy[1::,0] + errX, result_array_z_meanEnergy[1::,1]+errY,  xerr=errX, yerr=errY, fmt='o', label= name, alpha=0.3)

            plt.xlabel(x_label)

            plt.ylabel(y_label)

            plt.legend()



        #print(parameter_x[:], "schritte")

        #print(result_array_z_meanEnergy[1::], "mean_value for", parameter_sorted, " vs ", x_label, " criteria: ", name)








    def plot_result(self, color, name, auswahl, x_label, y_label):





        #print(auswahl[x_label], "x Achse")

        #print(auswahl[y_label], "y Achse")

        print(auswahl[x_label].count(), "len")

        print(auswahl[y_label].count(), "len y", name)



        if auswahl[x_label].count() == 0:

            print("empty dataframe in:", x_label)



        elif auswahl[y_label].count() == 0:

            print("empty dataframe in:", y_label)



        else:

            plt.scatter(x = auswahl[x_label], y = auswahl[y_label], color = color, marker = '.', alpha = 0.2, label=name )

            plt.xlabel(x_label)

            plt.ylabel(y_label)

            plt.legend()

            plt.show()








    def plot_together_in_one_graph(self,color, name, auswahl, x_label, y_label):




        x1= auswahl[x_label]

        y1 = auswahl[y_label]


        marker_list= (".", "x","+","<", ">")


        marker = marker_list[self.marker]

        print (marker)


        if x1.count() == 0:

            print("empty dataframe in:", x_label)

        elif y1.count() == 0:

            print("empty dataframe in:", y_label)


        else:


            self.marker = self.marker + 1

            plt.scatter(x1, y1, color = color, alpha = 0.2, label=name, marker = marker )

            plt.xlabel(x_label)

            plt.ylabel(y_label)

            plt.legend()



    def reset_marker(self):

        self.marker = 0

        return self.marker








    def mean_fundamental_GVD_vs_z(self, y_label):


        self.GVD_selection_dataframe()



        y_label = y_label

        x_label = "z um"

        parameter_x = list(range(-50, 50))


        self.mean_of_something_vs_something(self.auswahl_GVDneg, parameter_x, 100, x_label, y_label, y_label+"[nm]", self.selection_members[0])


        self.mean_of_something_vs_something(self.auswahl_GVD0, parameter_x, 100, x_label, y_label, y_label+"[nm]", self.selection_members[1])


        self.mean_of_something_vs_something(self.auswahl_GVD600, parameter_x, 100, x_label, y_label, y_label+"[nm]", self.selection_members[2])



        self.mean_of_something_vs_something(self.auswahl_GVD900, parameter_x, 100, x_label, y_label, y_label+"[nm]", self.selection_members[3])





        plt.ylim(760, 860)


        self.reset_name()


        self.name = self.name + "mean"


        self.save_picture(y_label)


        self.reset_name_list()



        plt.show()





    def fundamental_GVD_vs_z(self, y_label):


        x_label = "z um"

        self.GVD_selection_dataframe()

        self.zero_to_none(self.auswahl_GVDneg,x_label, y_label)
        self.zero_to_none(self.auswahl_GVD0, x_label, y_label)
        self.zero_to_none(self.auswahl_GVD600, x_label, y_label)
        self.zero_to_none(self.auswahl_GVD900, x_label, y_label)

        print(self.selection_members, "tuple")



        self.reset_marker()


        self.plot_together_in_one_graph("b", self.selection_members[0], self.auswahl_GVDneg, x_label, y_label)
        self.plot_together_in_one_graph('m', self.selection_members[1], self.auswahl_GVD0, x_label, y_label)
        self.plot_together_in_one_graph('g', self.selection_members[2], self.auswahl_GVD600, x_label, y_label)
        self.plot_together_in_one_graph('r', self.selection_members[3], self.auswahl_GVD900, x_label, y_label)


        self.reset_name_list()
        plt.show()






    def GVD_N25_div_vs_z(self):


        x_label = "z um"

        y_label = 'divergence N=25'



        self.GVD_selection_dataframe()

        self.zero_to_none(self.auswahl_GVDneg, x_label, y_label)
        self.zero_to_none(self.auswahl_GVD0, x_label, y_label)
        self.zero_to_none(self.auswahl_GVD600, x_label, y_label)
        self.zero_to_none(self.auswahl_GVD900, x_label, y_label)

        self.reset_marker()

        plt.figure(1)


        self.plot_together_in_one_graph("k",self.selection_members[1],self.auswahl_GVD0, x_label, y_label)


        self.plot_together_in_one_graph("g",self.selection_members[2],self.auswahl_GVD600, x_label, y_label)


        self.plot_together_in_one_graph("r",self.selection_members[3],self.auswahl_GVD900, x_label, y_label)



        plt.ylabel("divergence [mrad]")

        plt.xlabel("z [um]")

        plt.ylim(1,20)

        plt.xlim(0,4500)

        plt.legend()


        self.save_picture(y_label)

        plt.show()

        self.reset_name_list()









    def zero_to_none(self, auswahl, x_label, y_label):



        auswahl = auswahl.replace({x_label: 0.}, np.nan)[[y_label, "z um", 'shot', 'day']]

        return auswahl





    def reset_name_list(self):



        liste = ()

        return liste






    def mean_GVD_div_N25(self):




        x_label = "z um"

        y_label = 'divergence N=25'

        self.GVD_selection_dataframe()

        self.zero_to_none(self.auswahl_GVDneg, x_label, y_label)
        self.zero_to_none(self.auswahl_GVD0, x_label, y_label)
        self.zero_to_none(self.auswahl_GVD600, x_label, y_label)
        self.zero_to_none(self.auswahl_GVD900, x_label, y_label)









        z_list = list(range(-20,50))

        z_faktor = 100



        self.mean_of_something_vs_something(self.auswahl_GVDneg,z_list,z_faktor,x_label,y_label, y_label+"[mrad]", self.selection_members[0])

        self.mean_of_something_vs_something(self.auswahl_GVD0,z_list,z_faktor,x_label,y_label, y_label+"[mrad]", self.selection_members[1])

        self.mean_of_something_vs_something(self.auswahl_GVD600,z_list,z_faktor,x_label,y_label, y_label+"[mrad]", self.selection_members[2])

        self.mean_of_something_vs_something(self.auswahl_GVD900,z_list,z_faktor,x_label,y_label, y_label+"[mrad]", self.selection_members[3])



        self. reset_name_list()

        self.reset_name()


        self.name = self.name+"_mean_"

        self.save_picture(y_label)


        plt.show()



























# Sorting_by_parameters(dataframe, str(name), bool(save_picture???))
sorting1 = Sorting_by_parameters(RESULT, "SHHG19_", True)

sorting1.PP_out()
#sorting1.PP_in()

############ either day (number) or (0) which means "ALL" #########
sorting1.sort_by_day(0)
sorting1.high_energy(1.8)
#sorting1.low_energy(1.8)



############## second argument gives name of column for evaluation (y axis), since for energy two different ranges existing
####### name of column high energy range "HHG 24nm-34nm
energy_coloumnlabel = "HHG 34-50nm"
################ is not working !!! sorting1.energy_content_vs_z_highE(energy_coloumnlabel)
#sorting1.mean_energy_GVD_vs_z(energy_coloumnlabel)
sorting1.energy_content_vs_z_highE(energy_coloumnlabel)

######## either "central ROM", "central" or "CWE...something"
columname ='central ROM'
#sorting1.mean_fundamental_GVD_vs_z(columname)
#sorting1.fundamental_GVD_vs_z(columname)



###### GVD25_N25_div() ... plots all selection for different GVD values in scatter plot, if True then mean is plotted in addition (separate it!!!)
sorting1.GVD_N25_div_vs_z()
# returns sorted dataframes:
#sorting1.GVD_selection()
#sorting1.mean_GVD_div_N25()







plt.show()
