
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split


dir = "D:/GeocodingProjects/PBM/ISL/"
inputFile = "Cleaned_DNB_DEC16_CYP.txt"

df = pd.read_csv(dir+inputFile, sep=";",dtype=str,encoding='utf-8')
df.columns =['Street','City','Postcode']

#print(df.head())

print(df.drop_duplicates('Postcode'))

def getSinglePostcodeRows():
    value_counts = df['Postcode'].value_counts() # Specific column 
    to_remove = value_counts[value_counts== 1].index
    df_Single=df.iloc[to_remove]
    return df_Single


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
   # print(y.value_counts())
    X_train, X_test, y_train, y_test = train_test_split( x, y, test_size=requiredSize, random_state=42, stratify=y)
    
    
    dfBigSet = pd.concat([dfUnique,X_test])
    dfFinal = dfBigSet.drop_duplicates()
    #print (X_test)
    return dfFinal


out = sampleRowsOnPostCode(10000) 

df.to_csv(dir+'Sampled'+inputFile ,index=False,header=True ,encoding="UTF-8",sep=";")
    
"""
 value_counts = df[col].value_counts() # Specific column 
    to_remove = value_counts[value_counts <= threshold].index
    df[col].replace(to_remove, np.nan, inplace=True)
"""