import pandas as pd
import numpy as np
import pickle
import glob
from IPython.display import display, HTML

# Version : The android version file
# File:     Row per version, which is basically the analysis (including name as index) of a file

#Code Smells to be detected
codeSmells = ["AntiSingleton", "BaseClassKnowsDerivedClass", "BaseClassShouldBeAbstract", "Blob", "ClassDataShouldBePrivate",
               "ComplexClass", "FunctionalDecomposition", "LargeClass", "LazyClass", "LongMethod", "LongParameterList",
               "ManyFieldAttributesButNotComplex", "MessageChains", "RefusedParentBequest", "SpaghettiCode", "SpeculativeGenerality",
               "SwissArmyKnife", "TraditionBreaker"]

all_versions_path = np.array(glob.glob("testing_data/*.csv"))
print (all_versions_path)


def __init__(version_path):
    df = pd.read_csv(version_path)
    df.rename(columns = {x: x.strip() for x in  df.columns}, inplace = True)
    df.rename(columns = {"Code Smells": "codeSmells"}, inplace = True)
    df.set_index('codeSmells', inplace=True)
    return df

def accumulateAllVersions(all_versions_path):
    allversionsdf = {}
    allversionsname = []
    for version_path in all_versions_path:
        allversionsdf.update({version_path.strip().split('\\')[-1].rsplit('.',1)[0]: __init__(version_path)})
        allversionsname.append(version_path.strip().split('\\')[-1].rsplit('.',1)[0])

    return allversionsdf, allversionsname

def groupOnFiles(allversionsdf):
    all_files_list = []
    for version_name in allversionsdf:                      # Iterate over every file in the version
        df = allversionsdf[version_name].T
        for index in df:
            if index not in all_files_list:
                all_files_list.append(index)

    return all_files_list

def makeFileBasedDF(allversionsdf, allversionsname, all_files_list):
    fileBasedDF = {}
    non_empty_file_list = []
    for x in all_files_list:
        #print ("\nWorking for file: ", x)
        df_for_a_file = pd.DataFrame(columns = codeSmells, index = allversionsname)

        emptyDF = True
        for y in allversionsdf:
            if (x in allversionsdf[y].T.columns):
                #print ("\nIncluded")
                mycolumn = np.array(allversionsdf[y].T[x])
                if (np.any(mycolumn)):
                    emptyDF = False

                #print ("Appending ", mycolumn,  " to the file.")
                transpose = df_for_a_file.T
                transpose[y] = mycolumn
                df_for_a_file = transpose.T
            else:
                #print ("\nNot Included!")
                #print ("\n\tDropping ", y, " from DF.")
                df_for_a_file.drop(y, axis=0, inplace=True)

        #print ("\nFinal DF of ", x, ": ", df_for_a_file)
        if (emptyDF == False):
            # print ("\nDataFrame is not empty: ", x)
            # print (fileBasedDF)
            fileBasedDF.update({x:df_for_a_file})
        else:
            # print ("\nDataFrame is empty: ", x)
            # Remove that file from all_files_list
            non_empty_file_list.append(x)

    return fileBasedDF, non_empty_file_list

def saveFileBasedDFPickle(path, fileBasedDF):
    with open(path, 'wb') as pickleFile:
        pickle.dump(fileBasedDF, pickleFile, protocol=pickle.HIGHEST_PROTOCOL)


allversionsdf, allversionsname = accumulateAllVersions(all_versions_path)  #A Dictionary, #a list
all_files_list = groupOnFiles(allversionsdf)
fileBasedDF, non_empty_file_list = makeFileBasedDF(allversionsdf, allversionsname, all_files_list)

# #Print File Based DataFrames (Tables)
# for x in fileBasedDF:
#     print (x)
#     display(fileBasedDF[x])

saveFileBasedDFPickle("fileBasedDF.pickle",fileBasedDF)


#=================================================================================================


# # Rough Work
# df = pd.DataFrame({
#                 'day': ['1/1/2017','1/2/2017','1/3/2017','1/4/2017','1/5/2017','1/6/2017'],
#                 'temperature': [32,35,28,24,32,31],
#                 'windspeed': [6,7,2,7,4,2],
#                 'event': ['Rain', 'Sunny', 'Snow','Snow','Rain', 'Sunny'],
#                })
#
# df2 = pd.DataFrame(columns=['day', 'temperature', 'windspeed', 'event'])
#
#
# print (np.array(df['windspeed']))
# random = {"android_1.1": df, "android_2.1": df}
# random.update({"android_3.1": df})
# for x in df.T:
#     print (df.T[x])


# df2 = pd.DataFrame({
#                 'random1': ['1/1/2017','1/2/2017','1/3/2017','1/4/2017','1/5/2017','1/6/2017'],
#                 'random2': [32,35,28,24,32,31],
#                 'random3': [6,7,2,7,4,2],
#                 'random4': ['Rain', 'Sunny', 'Snow','Snow','Rain', 'Sunny'],
#                })
