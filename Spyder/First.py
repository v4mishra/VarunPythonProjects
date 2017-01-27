# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 15:44:28 2017

@author: VA009MI
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
df = pd.read_csv("D/GeocodingProjects/PBM/varunTemp/sample.csv")
print(df.head(5))
print(df.shape)




#understanding data:
#1):
print(df.areaName3.describe())
#2):
print(df.areaName3.value_counts())
print(df.areaName3.value_counts().head())
#2_a)
print(df.areaName3.value_counts(normalize=True))
#3) Unique list:
print(df.areaName3.unique())
print(df.areaName3.nunique())
print(sorted(df.areaName3.unique()))
#4) Filter by a column value:
print(df[df.areaName3=='LIMASSOL'])
print(df[df.areaName3.str.startswith('L')])




#How to drop a column:

dropColList = ['PB_ID','ISO3']
df.drop(dropColList,axis=1,inplace=True)
del(df.'PB_ID')

#add new col:
df['precisionCode'] ='S4'
df['size']=df.areaName1.str.len()


#how to drop a row if some col is empty
naCleanUpColList = ['areaName3','Postcode']
print(df.areaName3)
df.dropna(subset=naCleanUpColList, how='any',inplace=True)
print(df.areaName3.value_counts())


#how to concatenate two df (having same columns:)

newDf = pd.concat([df1,df2])


#How to get unique values of a column: (note here column should be non-null.)
print(sorted(df.areaName3.unique()))


#how filter rows based on some particular value of cell.
matches = df.areaName3.str.contains('LIMASSOL')
print(matches)
print(df[matches])
#or another approch:
print(df.loc[df.areaName3.str.contains('LIMASSOL'),"areaName3"])
#or - for multi filter combination :
matchesLimasol = df.areaName3.str.contains('LIMASSOL')
matchesPAFOS = df.areaName3.str.contains('PAFOS')
print(df.loc[matchesLimasol | matchesPAFOS,"areaName3"])




#from sklearn.model_selection import train_test_split
from sklearn.cross_validation import train_test_split
y = df.pop("Key")
print(y.head(5))

X_train, X_test, y_train, y_test = train_test_split( df, y, test_size=100, random_state=42)
print(X_train.shape)

X_test.col
X_test.to_csv("D:/GeocodingProjects/PBM/varunTemp/sample.csv", sep='|', encoding='utf-8')