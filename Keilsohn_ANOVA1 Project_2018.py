# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 19:46:40 2018

@author: William Keilsohn
"""

### Perform an ANOVA on a series of data

# Import packages
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison

# Load in the data
dataFile = pd.read_csv('Example_Data.csv')
'''
We can tell python what the headings are, or python can figure it out on its own.
In this case it is more convienent to let python figure it out, as then we don't 
get an extra row with just the headings.
'''

# Run the ANOVA first, check the assumptions later
model = ols('Data ~ Group', data = dataFile).fit() # Create a model for the anova
anov_table = sm.stats.anova_lm(model, typ = 1) # note that this is a one-way ANOVA
print('ANOVA results:')
print(anov_table) #Looks alright.
print('\n') # Just looks nicer

# Now to test for assumptions
dataResid = model.resid #Normality testing is done on the residuals of the data
normTest = stats.shapiro(dataResid) #Just going to use a shapio-wilks due to small sample
print('Normality test results:')
print(normTest) #B/c the p-value > 0.05 the data is normally distributed.
print('\n') # just looks nice

# Now to look at variance homogeneity
letLis = ['A', 'B', 'C', 'D']
dataLis = []
for x in letLis: #Bartlett test works better if provided a list of data
   groupData = dataFile.loc[dataFile['Group'] == x, 'Data'].tolist()
   dataLis.append(groupData)

bartData = stats.bartlett(dataLis[0], dataLis[1], dataLis[2])
print('The results of the bartlett test are: ')
print(bartData) # This is insiginifant, which is good.
print('\n')

# Sweet! So we have a significant ANOVA, and it passes all the tests. Time to see what  treatments matter.
dataCompare = MultiComparison(dataFile['Data'], dataFile['Group']) #Runs comparisons between treatments
tukeyResult = dataCompare.tukeyhsd() #Runs a tukey HSD test based on those comparisons
print(tukeyResult) #prints out a table displaying all relationships between groups
print('Therefore, the unique treatments (a = 0.05) are:')
print(dataCompare.groupsunique) #prints out a list of all treatments which are unique.

# With a sucessful ANOVA we can plot the data
plt.figure() #I don't want them to overlap
sns.set_palette("Blues") #I want some blue colors for this plot
dataPlot = sns.violinplot(x = dataFile['Group'], y = dataFile['Data'])#This one is gonna be fun
dataPlot.set_title('Weight vs. Group') #Add a title
dataPlot.set(xlabel = 'Group', ylabel = 'Weight (g)') #Change the labels
print('\n') #Spacing and formatting...

# How about one with Tufte priniclples
plt.figure()
ax = plt.gca() #pull out just the background
ax.set_facecolor('xkcd:white') #Remove the gray background
mpl.rcParams['boxplot.medianprops.color'] = 'black' #Make the median line black and thus visable
plt.boxplot(dataLis, labels = letLis) #The data needs to be in list format for this
# Additionally it is beneficial to have the labels for the treatments in a list
## Everything below this is styling
plt.xlabel('Treatment') #Label your variables
plt.ylabel('Weight (g)')
ax.spines['top'].set_color(None) #Delete the two sides you don't want
ax.spines['right'].set_color(None) 
ax.tick_params(direction = 'in') #Ticks should point inward.
plt.savefig('graph1.png') #Saves a png of the graph