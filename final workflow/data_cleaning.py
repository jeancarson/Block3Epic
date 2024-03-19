#This is a .py file so it can be run in the model notebooks
#My idea was to have one hot encoding done here, then removal of any outliers, bsaed on judgments made in the data visualisation file
#Idk if this is best, but then we are all working off one cleaned dataset


import pandas as pd # data processing
import numpy as np # linear algebra
import seaborn as sns # for plotting
import matplotlib.pyplot as plt


#import data
df = pd.read_csv("/Users/miaborko/Documents/epic3/Block3Epic/data_copy.csv") #read dataset

#drop unnecesary columns

df.drop("Marital Status", axis=1, inplace=True)
df.drop("Race", axis=1, inplace=True)
df.drop("differentiate", axis=1, inplace=True)


#Onehot Encoding
categorical_features = df.select_dtypes(include = "object").columns
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder
df.loc[df['Grade'] == 'anaplastic; Grade IV', 'Grade'] = 4
df[categorical_features] = df[categorical_features].apply(LabelEncoder().fit_transform) # Encoding all categorical features

#Renaming 
df.rename({'Tumor Size': 'Tumor Size (mm)', 'T Stage ': 'T Stage', 'Reginol Node Positive': 'Regional Node Positive', 'differentiate': 'Differentiate'}, axis=1, inplace=True)
df['Grade'] = df['Grade'].map({'1': 'Grade 1', '2': 'Grade 2', '3': 'Grade 3', ' anaplastic; Grade IV': 'Grade 4'})

df.to_csv('/Users/miaborko/Documents/epic3/Block3Epic/cleaned_data.csv', index=False)


#Removing outliers

def remove_outliers_tumor_size(toclean):
    Q1 = toclean['Tumor Size'].quantile(0.25)
    Q3 = toclean['Tumor Size'].quantile(0.75)
    IQR = Q3 - Q1
    toclean = toclean[~((toclean['Tumor Size'] < (Q1 - .5*IQR)) | (toclean['Tumor Size'] > (Q3 +.5*IQR)))]
    return toclean

def remove_other_outliers(toclean):
    outlier_indices = []
    for col in df.columns:
        # Skip the 'Tumor Size (mm)' column
        if col == 'Tumor Size (mm)':
            continue

        Q1 = toclean[col].quantile(0.25)
        Q3 = toclean[col].quantile(0.75)
        IQR = Q3 - Q1

        is_outlier = (toclean[col] < (Q1 - 1.5 * IQR)) | (toclean[col] > (Q3 + 1.5 * IQR))
        outlier_indices.extend(toclean.index[is_outlier])

    # removes duplicates from the outlier indices list
    outlier_indices = list(set(outlier_indices))

    cleaned_data = toclean.drop(outlier_indices)

    return cleaned_data


