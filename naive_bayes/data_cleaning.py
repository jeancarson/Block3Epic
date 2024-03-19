import pandas as pd
print("Hello World")
data = pd.read_csv("/Users/oisinfrizzell/Desktop/Repos/Block3Epic/data_copy.csv")
# data = pd.read_csv(r"C:\Users\jeanl\College\Blocks\Block 3\Epic\Block3Epic\archive\output.csv")

# Print the column names in the DataFrame
print(data.columns)


#T stage mapping
T_stage_mapping = {
    'T1': 1,
    'T2': 2,
    'T3': 3,
    'T4': 4
}
# Map the text values to numeric codes
data['T Stage'] = data['T Stage'].map(T_stage_mapping)

#N stage mapping
N_stage_mapping = {
    'N1': 1,
    'N2': 2,
    'N3': 3,
    'N4': 4
}

# Map the text values to numeric codes
data['N Stage'] = data['N Stage'].map(N_stage_mapping)

#6th stage mapping
sixth_stage_mapping = {
    'IA': 1,
    'IB': 2,
    'IC': 3,
    'IIA': 4,
    'IIB': 5,
    'IIC': 6,
    'IIIA': 7,
    'IIIB': 8,
    'IIIC': 9,
    'IV': 10,
}

# Map the text values to numeric codes
data['6th Stage'] = data['6th Stage'].map(sixth_stage_mapping)

#Differenciate mapping
#Because for most other values eg T, N stage, grade etc, bigger numbers correspond to worst cancer, I have made the choice to map poorer differenciation to a higher value.

differenciate_mapping = {
    'Undifferentiated': 0,
    'Poorly differentiated': 1,
    'Moderately differentiated': 2,
    'Well differentiated': 3
}
# Map the text values to numeric codes
data['differentiate'] = data['differentiate'].map(differenciate_mapping)

#Grade mapping
grade_mapping = {
    ' anaplastic; Grade IV': 4,
    '1':1,
    '2':2,
    '3':3,
    '4':4
}
data['Grade'] = data['Grade'].map(grade_mapping)

# anaplastic_grade_IV_data = data[data['Grade'] == 4]
# print(anaplastic_grade_IV_data)

# print(data['Grade'].unique())
#A stage mapping
A_Stage_mapping = {
    'Regional': 0,
    'Distant': 1,
}
# Map the text values to numeric codes
data['A Stage'] = data['A Stage'].map(A_Stage_mapping)


#Estrogen status mapping
estrogen_mapping = {
    'Negative': 0,
    'Positive': 1,
}
# Map the text values to numeric codes
data['Estrogen Status'] = data['Estrogen Status'].map(estrogen_mapping)

#Progesterone status mapping
Progesterone_mapping = {
    'Negative': 0,
    'Positive': 1,
}
# Map the text values to numeric codes
data['Progesterone Status'] = data['Progesterone Status'].map(Progesterone_mapping)

#Survival mapping
survival_mapping = {
    'Dead': 0,
    'Alive': 1,
}
# Map the text values to numeric codes
data['Status'] = data['Status'].map(survival_mapping)

#Remove race and marital status columns as we won't need to analyse these
data = data.drop(["Marital Status", "Race"], axis=1) 

#Analysing how clean the data is:
data.info()

data.describe()[1:].T
#Dimensionality??? LOL idk maybe this is useful to know?

#Count missing values
#is zero, yay!
data.isna().sum()
print('Before head')
#find duplicated data:

data.duplicated().sum()


# print(data.head())

def remove_outliers_tumor_size(toclean):
    Q1 = toclean['Tumor Size'].quantile(0.25)
    Q3 = toclean['Tumor Size'].quantile(0.75)
    IQR = Q3 - Q1
    toclean = toclean[~((toclean['Tumor Size'] < (Q1 - .5*IQR)) | (toclean['Tumor Size'] > (Q3 +.5*IQR)))]
    return toclean

data = pd.get_dummies(data)
#replace this with one hot encodeing

#change number nodes tested vs number nodes positive to a decimal
def regional_node_pos_to_percent(toclean):
    toclean['percent regional node positive'] = toclean['Reginol Node Positive'] / toclean['Regional Node Examined']
    toclean.drop(['Regional Node Examined', 'Reginol Node Positive'], axis=1, inplace=True)
    return toclean
data = regional_node_pos_to_percent(data)
print(data.head())


