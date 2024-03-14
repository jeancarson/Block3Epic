#This is a .py file so it can be run in the model notebooks
#My idea was to have one hot encoding done here, then removal of any outliers, bsaed on judgments made in the data visualisation file
#Idk if this is best, but then we are all working off one cleaned dataset


import pandas as pd # data processing
import numpy as np # linear algebra
import seaborn as sns # for plotting
import matplotlib.pyplot as plt


#import data
df = pd.read_csv(r"C:\Users\jeanl\College\Blocks\Block 3\Epic\Block3Epic\data_copy.csv") #read dataset

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


#Removing outliers

def remove_outliers_tumor_size(toclean):
    Q1 = toclean['Tumor Size'].quantile(0.25)
    Q3 = toclean['Tumor Size'].quantile(0.75)
    IQR = Q3 - Q1
    toclean = toclean[~((toclean['Tumor Size'] < (Q1 - .5*IQR)) | (toclean['Tumor Size'] > (Q3 +.5*IQR)))]
    return toclean


