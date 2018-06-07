import pandas as pd
import numpy as np
import pickle
import glob
from IPython.display import display, HTML

'''
    Code Smells: Vocabulary
    X: Android Versions (to which files are associated)


    Data: (per file)
                AntiSingleton, ....... (codesmells)...
    Android1.0      1       2           3
    Android2.0      0       2           2
    .....
    (android versions)
'''
codeSmells = ["AntiSingleton", "BaseClassKnowsDerivedClass", "BaseClassShouldBeAbstract", "Blob", "ClassDataShouldBePrivate",
               "ComplexClass", "FunctionalDecomposition", "LargeClass", "LazyClass", "LongMethod", "LongParameterList",
               "ManyFieldAttributesButNotComplex", "MessageChains", "RefusedParentBequest", "SpaghettiCode", "SpeculativeGenerality",
               "SwissArmyKnife", "TraditionBreaker"];

theta_threshold = 2

# Testing Data
fileBasedDF = pd.DataFrame({'TFD' : ['AA', 'SL', 'BB', 'D0', 'Dk', 'FF'],
                    'Snack' : ['1', '0', '1', '1', '0', '0'],
                    'Trans' : ['1', '1', '1', '0', '0', '1'],
                    'Dop' : ['1', '0', '1', '0', '1', '1']}).set_index('TFD')


#============================================================== Counts

#===================== Co-occurrence Counts
co_occurrence_counts = pd.DataFrame(columns = fileBasedDF.columns, index = fileBasedDF.columns)         # Unnecessary Declaration

# Creating Co-occurrence
fileBasedDF_asint = fileBasedDF.astype(int)
co_occurrence_counts = fileBasedDF_asint.T.dot(fileBasedDF_asint)

# Filtering Data below Threshold
co_occurrence_counts.mask(co_occurrence_counts < theta_threshold, other=0, inplace = True)
display ("Co-occurrence Counts: ", co_occurrence_counts)

#===================== Creating Marginal Counts
marginal_counts = pd.DataFrame(columns = ["Count"], index = fileBasedDF.columns)
marginal_counts = pd.DataFrame(co_occurrence_counts.sum(axis=1))
marginal_counts.rename(columns={0: 'counts'}, inplace=True)
display ("Marginal Counts: ", marginal_counts)

#===================== Creating Total Counts
total_counts = float(marginal_counts.sum(axis=0))/2
print ("Total Count :", total_counts)

# NOT SURE IF DIAGONAL ELEMENTS ARE EXCLUDED
# NOT SURE IF SAME ELEMENT COUNT IS EXCLUDED

#============================================================== Probabilities

#===================== Co-occurrence Probabilities
co_occurrence_prob = co_occurrence_counts/total_counts
display ("Co-occurrence Probabilities: ", co_occurrence_prob)

#===================== Marginal Probabilities
marginal_prob = marginal_counts/total_counts
display ("Marginal Probabilities: ", marginal_prob)









#
