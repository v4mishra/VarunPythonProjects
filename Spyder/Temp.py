# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 12:59:50 2017

@author: VA009MI
"""



import pandas as pd
from sklearn.cross_validation import train_test_split

d = [('indore',33),
     ('pune',312),
     ('Ujjain',),
     ('pune',255),
     ('Noida',29),
     ('bhopal',),  
     ('bhopal',87),
     ('pune',871),
     ('indore',94)]
     
d2 = [('zzzzz',33333),
     ('eeeee',111112)]
     
df = pd.DataFrame.from_records(d,columns=['city','code'])


dir = "D:/GeocodingProjects/PBM/ISL/"
inputFile = "temp.TXT"
countryPostCodeRegex ="^\d\d\d$"

df = pd.read_csv(dir+inputFile, sep=";")

df.columns = ['Street','City','Postcode']
print(df.info())
     
print(df)


def filterIncorrectPostcodes( postcodeCol, strRegexToMatch):
    strPC = df[postcodeCol].apply(str) 
    matches = df[postcodeCol].str.strip().str.contains(strRegexToMatch)
    print("removing non-matching postboxes" )
    print(matches.value_counts())
    print("Non matching: ")
    print(df[~matches])
    return df[matches]


countryPostCodeRegex ="^([0-9]+)$|^$"
f = filterIncorrectPostcodes('Postcode',countryPostCodeRegex)
print("matching: ")
print(f)





import pandas as pd
dir = "D:/GeocodingProjects/PBM/SVN/"
inputFile = "SVN_Forward_Testfile.txt"
df = pd.read_csv(dir+inputFile, sep=";",dtype={'Postalcode': object},na_filter=False)

df['Postalcode'] = df['Postalcode'].astype(str)
df['SL'] = df['Street'] + " " +df['City'] + " " +df['Postalcode'].map(str)
df[['Street','Postcode','City', 'SL','Source']].to_csv(dir+'2_Combined_WithSL.txt' ,index=False,header=True ,encoding="UTF-8",sep=";")


'mainAddressLine','Postcode','areaName3'



"""
import numpy as np
dir = "D:/GeocodingProjects/PBM/CYP/"
inputFile = "Cleaned_DNB_DEC16_CYP.TXT"
df = pd.read_csv(dir+inputFile, sep=";")
value_counts = df['Postcode'].value_counts() # Specific column 
to_remove = value_counts[value_counts== 1].index
df_Single=df.iloc[to_remove]

df['Postcode'].replace(to_remove, np.nan, inplace=True)
print(len(df))
df.dropna(subset=['Postcode'], how='any',inplace=True)
print(len(df))

"""



import pandas as pd


dir = "D:/GeocodingProjects/PBM/SVN/"
inputFile = "1_Sampled_SVN_MasterCard_Addr_Full.txt"


df = pd.read_csv(dir+inputFile, sep=";",dtype={'Postcode': object,'Street':object})
print(df.info())
df.SL= df.SL.str.strip()
df.SL().head()
