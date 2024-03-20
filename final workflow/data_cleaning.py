#This is a .py file so it can be run in the model notebooks
#My idea was to have one hot encoding done here, then removal of any outliers, bsaed on judgments made in the data visualisation file
#Idk if this is best, but then we are all working off one cleaned dataset


import pandas as pd # data processing
import numpy as np # linear algebra
import seaborn as sns # for plotting
import matplotlib.pyplot as plt
from sklearn.calibration import LabelEncoder


#import data
df = pd.read_csv("C:\Users\jeanl\College\Blocks\Block 3\Epic\Block3Epic\archive\Breast_Cancer.csv") #read dataset

def clean_data(df):
    # Renaming columns
    df.rename({'Tumor Size': 'Tumor Size (mm)', 'T Stage ': 'T Stage', 
               'Reginol Node Positive': 'Regional Node Positive', 'differentiate': 'Differentiate'}, axis=1, inplace=True)
    df['Grade'] = df['Grade'].map({'1': 'Grade 1', '2': 'Grade 2', '3': 'Grade 3', ' anaplastic; Grade IV': 'Grade 4'})

    # Drop unnecessary columns
    df.drop(["Marital Status", "Race", "Differentiate"], axis=1, inplace=True)

    # One-hot Encoding
    categorical_features = df.select_dtypes(include="object").columns
    df.loc[df['Grade'] == 'anaplastic; Grade IV', 'Grade'] = 4
    df[categorical_features] = df[categorical_features].apply(LabelEncoder().fit_transform)

    

    # Removing outliers
    df = remove_outliers_tumor_size(df)
    df = remove_outliers_survival_months(df)

    return df



#Removing outliers

def remove_outliers_tumor_size(toclean):
    Q1 = toclean['Tumor Size (mm)'].quantile(0.25)
    Q3 = toclean['Tumor Size (mm)'].quantile(0.75)
    IQR = Q3 - Q1
    toclean = toclean[~((toclean['Tumor Size (mm)'] < (Q1 - 1.5*IQR)) | (toclean['Tumor Size (mm)'] > (Q3 +1.5*IQR)))]
    return toclean

def remove_outliers_survival_months(toclean):
    Q1 = toclean['Survival Months'].quantile(0.25)
    Q3 = toclean['Survival Months'].quantile(0.75)
    IQR = Q3 - Q1
    toclean = toclean[~((toclean['Survival Months'] < (Q1 - .5*IQR)) | (toclean['Survival Months'] > (Q3 +.5*IQR)))]
    return toclean

df_cleaned = clean_data(df)

# Save cleaned data to a new CSV file
df_cleaned.to_csv("cleaned_data_new.csv", index=False)

