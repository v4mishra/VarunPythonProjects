# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 12:40:50 2017

@author: VA009MI
"""


import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split




dir = "D:/GeocodingProjects/PBM/ISL/"
inputFile = "DNB_DEC16_ISL.TXT"
countryPostCodeRegex ="^\d\d\d$"

df = pd.read_csv(dir+inputFile, sep="|")
print(df.info())



def removeCols(dropColList):   
    df.drop(dropColList,axis=1,inplace=True)
    
    

def removeRowsWithNan(naCleanUpColList):
    df.dropna(subset=naCleanUpColList, how='any',inplace=True)
      
    
def filterIncorrectPostcodes( postcodeCol, strRegexToMatch):
    strPC = df[postcodeCol].apply(str) 
    matches = strPC.str.match(strRegexToMatch)
    print("removing non-matching postboxes" )
    print(matches.value_counts())
    return df[matches]
  
    

def filterRowsWithoutNumberInStreetRecord( strStreetAddColName):
    return  df[df[strStreetAddColName].str.contains('\d')]
    

def removeDuplicateRows(strStreetAddColName):    
    df['temp'] = df[strStreetAddColName].str.strip().str.upper().str.replace("\W", "")
    df.drop_duplicates(['temp'], keep='last',inplace=True)
    df.drop('temp',axis=1,inplace=True)

def sampleRowsOnPostCode(requiredSize):
    #First create a df of unique postcodes:
    dfUnique = df.drop_duplicates('Postcode')
    requiredSize = abs(requiredSize-len(dfUnique))
    
    #First extract rows having just 1 instance of postcodes:
    vcPostcode = df.Postcode.value_counts()
    to_remove = vcPostcode[vcPostcode==1].index
    df['Postcode'].replace(to_remove, np.nan, inplace=True)
    
    df.dropna(subset=['Postcode'], how='any',inplace=True)
    #print(df)
    
    #Now perform stratified sampling:
    x = df
    y = df.Postcode
    X_train, X_test, y_train, y_test = train_test_split( x, y, test_size=requiredSize, random_state=42, stratify=y)
    
    #X_test is sampled output.
    #print (X_test)   
    
    #now merge all unique postcodes with X_tests
    dfBigSet = pd.concat([dfUnique,X_test])
    dfFinal = dfBigSet.drop_duplicates()
    
    return dfFinal
    

  #1. Remove PB_ID  , NAME and ISO column.  
removeCols(['PB_ID','Name','areaName1','ISO3'])


#2. Remove NAN rows
removeRowsWithNan(['mainAddressLine','areaName3','Postcode'])



#3. Remove rows where postbox is invalid .
df = filterIncorrectPostcodes("Postcode",countryPostCodeRegex)



#4. Remove rows where mainAddressLine does not contain a number.
df = filterRowsWithoutNumberInStreetRecord('mainAddressLine')


    
#5 Remove duplicates :
removeDuplicateRows('mainAddressLine')        



df.to_csv(dir+'Cleaned_'+inputFile ,index=False,header=True ,encoding="UTF-8",sep=";")


#6 Sample rows (probably based on postcode).
df = sampleRowsOnPostCode(10000)
df.to_csv(dir+'Sampled_'+inputFile ,index=False,header=True ,encoding="UTF-8",sep=";")

#***************