# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 15:45:18 2017

@author: VA009MI
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
df = pd.read_csv("D:/GeocodingProjects/PBM/varunTemp/sample.csv", sep="|")
#print(df.head(5))
print(df.shape)

dropColList = ['PB_ID','ISO3']
df.drop(dropColList,axis=1,inplace=True)

naCleanUpColList = ['areaName3','Postcode']
print(df.areaName3)
df.dropna(subset=naCleanUpColList, how='any',inplace=True)
print(df.areaName3.value_counts())


#filter rows based on some particular value of cell.
matches = df.areaName3.str.contains('LIMASSOL')
print(matches)
print(df[matches])

#orr:
print(df[df.areaName3.str.contains('LIMASSOL')].areaName3)
# orr
print(df.loc[df.areaName3.str.contains('LIMASSOL'),"areaName3"])
#or:
matchesLimasol = df.areaName3.str.contains('LIMASSOL')
matchesPAFOS = df.areaName3.str.contains('PAFOS')

print(df.loc[matchesLimasol | matchesPAFOS,"areaName3"])



##REPLACE SOMETHING:
df.mainAddressLine.str.replace(",","#")


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
#get unique values of a column:
print(sorted(df.areaName3.unique()))



df['precisionCode'] ='S4'
df['add'] = df.areaName3.str + df.Postcode.str

print(df[df.areaName3.str.startswith('L')])
print(df.head())