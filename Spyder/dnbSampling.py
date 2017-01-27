# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 12:40:50 2017

@author: VA009MI
"""


import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split




dir = "D:/GeocodingProjects/PBM/SVN/"
inputFile = "DNB_DEC16_SVN.TXT"
#inputFile = "temp.TXT"
countryPostCodeRegex ="^([0-9]+)$|^$"

df = pd.read_csv(dir+inputFile, sep="|",dtype={'Postcode': object,'mainAddressLine':object,'areaName1':object})
print(df.info())



def removeCols(dropColList):   
    df.drop(dropColList,axis=1,inplace=True)
    
    

def removeRowsWithNan(naCleanUpColList):
    df.dropna(subset=naCleanUpColList, how='any',inplace=True)
      
    """
def filterIncorrectPostcodes2( postcodeCol, strRegexToMatch):
    strPC = df[postcodeCol].apply(str) 
    matches = strPC.str.match(strRegexToMatch)
    print(matches.head())
    print("removing non-matching postboxes" )
    #print(matches.value_counts())
    return df[matches]
  """

def filterIncorrectPostcodes( postcodeCol, strRegexToMatch):
    df.Postcode.replace(np.nan,'', regex=True, inplace=True)
    return 
    

def filterRowsWithoutNumberInStreetRecord( strStreetAddColName):
    return  df[df[strStreetAddColName].str.contains('\d')]


def filterRowsHavingBoxInStreetRecord( strStreetAddColName):
    return  df[~df['mainAddressLine'].str.contains('.*box.*', case=False)]
    
def removeSemiColon():
    for colName in df.columns:
        print(colName)
        df[colName]= df[colName].str.replace(';','')    
    return df
    
    
    #return df.str.replace(';','', regex=False, inplace=True)
               

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
removeRowsWithNan(['mainAddressLine','areaName3'])

removeSemiColon()

#3. Remove rows where postcode is invalid .
df = filterIncorrectPostcodes("Postcode",countryPostCodeRegex)



#4. Remove rows where mainAddressLine does not contain a number.
df = filterRowsWithoutNumberInStreetRecord('mainAddressLine')

#5. Remove rows where mainAddressLine does not contain a number.
df = filterRowsHavingBoxInStreetRecord('mainAddressLine')
    
#6 Remove duplicates :
removeDuplicateRows('mainAddressLine')        

#6 Create Single Line
df['SL'] = df['mainAddressLine'] + " " +df['areaName3'] + " " +df['Postcode'].map(str)
df['Source'] = 'Dnb'


df[['mainAddressLine','Postcode','areaName3', 'SL', 'Source']].to_csv(dir+'Cleaned_'+inputFile ,index=False,header=True ,encoding="UTF-8",sep=";")


#6 Sample rows (probably based on postcode).
df = sampleRowsOnPostCode(10000)
df[['mainAddressLine','Postcode','areaName3', 'SL', 'Source']].to_csv(dir+'1_Sampled_'+inputFile ,index=False,header=True ,encoding="UTF-8",sep=";")

#***************