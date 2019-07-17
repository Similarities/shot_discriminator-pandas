# multi_parameter_discriminator-pandas

Sorting and filtering tool for a multi-parametric non uniformly formatted dataset. 
The dataframe origins from a an scientific experiment and collects
different parameters and partly evaluated data for different shot series. 
naturally the parameters have to be sorted for take only measurements 
with parameter1 =x & parameter2 =xx and parameter3 = xy and so on. 
After this discrimination for e.g. either day, laser energy, Pre-pulse in etc. 
the real data evaluation starts: taking to coupled parameters into account which
are sorted for a third parameter (e.g. result...). The coupled parameters
are here separated the following: one is just the x_axis, while the other
is shown in different colors. Now the third parameter (e.g. result) is just
shown as our y_axis. 

One of the tricky things for such databases is: the preparation of the dataset
some of the parameters are just "str", some numbers, some have 0 with the meaning
is a result, some of them have 0 as Nan wihtout being Nan etc. 
In consequence, each parameter needs to be adressed separately for formatting.


The programm handles now the coupling betwenn two parameters ("GVD in fs^2" and "z um") for
different result parameters. Here we unified the coupling, naming, plotting, saving etc. and 
organized for data point distribution or mean values. 




example database with the following columns:

day #shot no #PPin #result1 #parameter1 #parameter2 #exceptions1 # parameter4 #exceptions2 #result2 #result3 #description


Python 3.7 with PyCharm.










uses python >3.5, package pandas, package xlrd (to read .xlsx excel files)
can be used for python 2.7 version (scipy x,y e.g.), then pandas and xlrd package has to be put in the "libs/ sidepackages" folder

