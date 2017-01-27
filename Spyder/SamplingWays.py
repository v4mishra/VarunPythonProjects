# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 12:59:50 2017

@author: VA009MI
"""



import pandas as pd
from sklearn.cross_validation import train_test_split

d = [('indore',33),
     ('pune',32),
     ('Ujjain',21),
     ('pune',55),
     ('Noida',29),
     ('bhopal',87),  
     ('bhopal',87),
     ('pune',87),
     ('indore',94)]

df = pd.DataFrame.from_records(d,columns=['city','code'])

#print(df)
x = df
y = df.code
print(y.value_counts())
X_train, X_test, y_train, y_test = train_test_split( x, y, test_size=0.45, random_state=42, stratify=y)

print (X_test)




"""
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold

d = [('indore',33),
     ('pune',32),
     ('noida',21),
     ('pune',55),
     ('pune',29),
     ('bhopal',87),  
     ('bhopal',87),
     ('noida',87),
     ('indore',94)]

df = pd.DataFrame.from_records(d,columns=['city','code'])


X = df #np.ones(10)
y = df.city #[0, 0, 0, 0, 1, 1, 1, 1, 1, 1]



#print(y.value_counts())
skf = StratifiedKFold(n_splits=2)
for train, test in skf.split(X, y):
    print("Train:%s ,Test: %s" % (train, test))
    
print("**")
print(test)
dfTest = (pd.DataFrame(test))
print(df.iloc[test])


from sklearn.model_selection import StratifiedShuffleSplit
sss = StratifiedShuffleSplit(n_splits=3, test_size=0.3, random_state=0.2 )
#print(sss.get_n_splits(X, y))
sss.get_n_splits(X, y)

train,test = sss.split(X, y)



for train_index, test_index in sss.split(X, y):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

"""