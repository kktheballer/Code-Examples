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




#---------------import training set-------------------#

a = pe.get_array(file_name = "train.xlsx")
training= np.array(a)


y1_train = training[1:97, 13]
y1_train = np.array(y1_train, dtype=float)


y2_train = training[1:97, 14]
y2_train = np.array(y2_train, dtype=float)

x_train = training[1:97, 0:13]
x_train = np.array(x_train, dtype=float)


#scale the training set data
scaler = pre.StandardScaler()
X_train_scaled = scaler.fit_transform(x_train)



#-----------------import test set----------------#
b = pe.get_array(file_name = "test.xlsx")
test = np.array(b)


y1_test = test[1:43, 13]
y1_test = np.array(y1_test, dtype=float)

y2_test = test[1:43, 14]
y2_test = np.array(y2_test, dtype=float)

x_test = test[1:43, 0:13]
x_test = np.array(x_test, dtype=float)

#scale the test set data
X_test_scaled = scaler.fit_transform(x_test)



#--------------Training OP-1--------------#
mlp = MLPRegressor(hidden_layer_sizes=50, activation='tanh', max_iter=500, learning_rate_init=0.1, random_state=1, solver='lbfgs', tol=0.001 )
mlp.fit(X_train_scaled, y1_train) 
print

#prediction is for OP_1 test
prediction = mlp.predict(X_test_scaled)
#prediction1 is for OP_1 train
prediction1 = mlp.predict(X_train_scaled)


print ('OP_1 train Rsq: ', mlp.score(X_train_scaled, y1_train)) 
print ('OP_1 test Rsq: ', mlp.score(X_test_scaled, y1_test))


#--------------Training OP-2--------------#
mlp1 = MLPRegressor(hidden_layer_sizes=4, activation='tanh', max_iter=500,  alpha = 0.1, learning_rate = 'adaptive', learning_rate_init=0.1, random_state=1, solver='lbfgs', tol=0.001 )
mlp1.fit(X_train_scaled, y2_train)
print

#prediction is for OP_2 test
prediction = mlp1.predict(X_test_scaled)
#prediction1 is for OP_2 train
prediction1 = mlp1.predict(X_train_scaled)


print ('OP_2 train Rsq: ',  mlp1.score(X_train_scaled, y2_train))
print ('OP_2 test Rsq: ', mlp1.score(X_test_scaled, y2_test))


