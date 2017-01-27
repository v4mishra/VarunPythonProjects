# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 18:02:11 2017

@author: VA009MI
"""

import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split



dir = "D:/GeocodingProjects/PBM/SVN/"
#inputFile = "Combined.xlsx"
inputFile = "SVN_Forward_Testfile.txt"
countryPostCodeRegex ="^([0-9]+)$|^$"


#xls_file = pd.ExcelFile(dir+inputFile)
#df = xls_file.parse('Sheet1')


df = pd.read_csv(dir+inputFile, sep=";",dtype={'Postcode': object,'Street':object})
print(df.info())



print(df.info())



print(df.head(10))


def removeCols(dropColList):   
    df.drop(dropColList,axis=1,inplace=True)
    
    

def removeRowsWithNan(naCleanUpColList):
    df.dropna(subset=naCleanUpColList, how='any',inplace=True)
      
    
def filterIncorrectPostcodes( postcodeCol, strRegexToMatch):
    #strPC = df[postcodeCol].apply(str) 
    matches = df[postcodeCol].str.strip().str.contains(strRegexToMatch, na=True)
    print("removing non-matching postboxes" )
    print(matches.value_counts())    
    return df[matches]
  
    

def filterRowsWithoutNumberInStreetRecord( strStreetAddColName):
    return  df[df[strStreetAddColName].str.contains('\d')]
    

def removeDuplicateRows(strStreetAddColName):
    df['temp'] = df[strStreetAddColName].str.strip().str.upper().str.replace("\W", "")
    df.drop_duplicates(['temp'], keep='last',inplace=True)
    df.drop('temp',axis=1,inplace=True)
    
    

def sampleRowsOnPostCode(colName, requiredSize):
    #First create a df of unique postcodes:
    dfUnique = df.drop_duplicates(colName)
    requiredSize = abs(requiredSize-len(dfUnique))
    
    #First extract rows having just 1 instance of postcodes:
    vcPostcode = df[colName].value_counts()
    to_remove = vcPostcode[vcPostcode==1].index
    df[colName].replace(to_remove, np.nan, inplace=True)
    
    df.dropna(subset=[colName], how='any',inplace=True)
    #print(df)
    
    #Now perform stratified sampling:
    x = df
    y = df[colName]
    X_train, X_test, y_train, y_test = train_test_split( x, y, test_size=requiredSize, random_state=42, stratify=y)
    
    #X_test is sampled output.
    #print (X_test)   
    
    #now merge all unique postcodes with X_tests
    dfBigSet = pd.concat([dfUnique,X_test])
    dfFinal = dfBigSet.drop_duplicates()
    
    return dfFinal
    

  

  #1. Remove PB_ID  , NAME and ISO column.  
#removeCols(['PB_ID','Name','areaName1','ISO3'])


#2. Remove NAN rows
removeRowsWithNan(['Street','City'])


print(df.info())
#3. Remove rows where postbox is invalid .
df = filterIncorrectPostcodes("Postcode",countryPostCodeRegex)
print(df.info())


#4. Remove rows where Street does not contain a number.
df = filterRowsWithoutNumberInStreetRecord('Street')


    
#5 Remove duplicates :
removeDuplicateRows('SL')        


#6 remove postbox..


#6 Concatenate: (todo)


df.to_csv(dir+'Cleaned_'+inputFile+'_out.txt' ,index=False,header=True ,encoding="UTF-8",sep=";")





len(df.Postcode.value_counts())





#6 Sample rows (probably based on postcode).
df = sampleRowsOnPostCode('key',10000)
df[['Street','Postcode','City', 'SL', 'Source']].to_csv(dir+'Sampled_'+inputFile ,index=False,header=True ,encoding="UTF-8",sep=";")
