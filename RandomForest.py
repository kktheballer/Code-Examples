import csv
import numpy as np 
import random
import os.path
import pyexcel as pe
from pyexcel.ext import xlsx

from sklearn import preprocessing as pre
from sklearn.neural_network import MLPRegressor
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

#import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression


#------------import training set-------------------

a = pe.get_array(file_name = "train.xlsx")
training= np.array(a)


y1_train = training[1:97, 13]
y1_train = np.array(y1_train, dtype=float)


y2_train = training[1:97, 14]
y2_train = np.array(y2_train, dtype=float)

x_train = training[1:97, 0:13]
x_train = np.array(x_train, dtype=float)


#------------import test set-------------------
b = pe.get_array(file_name = "test.xlsx")
test = np.array(b)


y1_test = test[1:43, 13]
y1_test = np.array(y1_test, dtype=float)

y2_test = test[1:43, 14]
y2_test = np.array(y2_test, dtype=float)

x_test = test[1:43, 0:13]
x_test = np.array(x_test, dtype=float)


#---------------------OP_1----------------------#

#Build RandomForestRegression Model

regr = RandomForestRegressor(max_depth=2, random_state=0)
regr.fit(x_train, y1_train)

#Predict using model
train_predicted = regr.predict(x_train)
test_predicted = regr.predict(x_test)


#Compute Rsq using OP_1 (train/test) and prediction
train_rsq = r2_score(y1_train, train_predicted)
test_rsq = r2_score(y1_test, test_predicted)

#output Rsq values for OP_1 train and OP_1 test
print ('OP_1 Train Rsq: ',train_rsq, ' OP_1 Test Rsq: ', test_rsq)



#---------------------OP_2----------------------#

#Build RandomForestRegression Model
regr1 = RandomForestRegressor(max_depth=6, random_state=0)
regr1.fit(x_train, y2_train)

#Predict using model
train_predicted = regr1.predict(x_train)
test_predicted = regr1.predict(x_test)

#Compute Rsq using OP_2 (train/test) and prediction
train_rsq = r2_score(y2_train, train_predicted)
test_rsq = r2_score(y2_test, test_predicted)


#output Rsq values for OP_2 train and OP_2 test
print ('OP_2 Train Rsq: ',train_rsq, ' OP_2 Test Rsq: ', test_rsq)
