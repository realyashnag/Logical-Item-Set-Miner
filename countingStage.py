import pandas as pd
import numpy as np
import bisect
import glob

# Version : The android version file
# File:     Row per version, which is basically the analysis (including name as index) of a file

all_versions_path = np.array(glob.glob("testing_data/*.csv"))
# print (all_versions_path)


def __init__(version_path):
    df = pd.read_csv(version_path)
    df.rename(columns = {x: x.strip() for x in  df.columns}, inplace = True)
    df.rename(columns = {"Code Smells": "code_smells"}, inplace = True)
    df.set_index('code_smells', inplace=True)
    return df

def accumulateAllVersions(all_versions_path):
    allversionsdf = {}
    for version_path in all_versions_path:
        allversionsdf.update({version_path.strip().split('\\')[-1].rsplit('.',1)[0]: __init__(version_path)})

    return allversionsdf

def groupOnFiles(allversionsdf):
    filesList = []
    for version_name in allversionsdf:                      # Iterate over every file in the version
        df = allversionsdf[version_name].T
        for index in df:
            if index not in filesList:
                filesList.append(index)
                print (index)

    return filesList


var1 = accumulateAllVersions(all_versions_path)  #A Dictionary
# print (var1)
var2 = groupOnFiles(var1)

print (len(var2))

# # Rough Work
# df = pd.DataFrame({
#                 'day': ['1/1/2017','1/2/2017','1/3/2017','1/4/2017','1/5/2017','1/6/2017'],
#                 'temperature': [32,35,28,24,32,31],
#                 'windspeed': [6,7,2,7,4,2],
#                 'event': ['Rain', 'Sunny', 'Snow','Snow','Rain', 'Sunny'],
#                })
#
# random = {"android_1.1": df, "android_2.1": df}
# random.update({"android_3.1": df})


# df2 = pd.DataFrame({
#                 'random1': ['1/1/2017','1/2/2017','1/3/2017','1/4/2017','1/5/2017','1/6/2017'],
#                 'random2': [32,35,28,24,32,31],
#                 'random3': [6,7,2,7,4,2],
#                 'random4': ['Rain', 'Sunny', 'Snow','Snow','Rain', 'Sunny'],
#                })
