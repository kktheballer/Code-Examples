import pyexcel as pe
from pyexcel.ext import xlsx
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

#----------------import training set---------------#
a = pe.get_array(file_name = "train.xlsx")
training= np.array(a)

y1_train = training[1:97, 13]
y1_train = np.array(y1_train, dtype=float)

y2_train = training[1:97, 14]
y2_train = np.array(y2_train, dtype=float)

x_train = training[1:97, 0:13]
x_train = np.array(x_train, dtype=float)


#----------------import test set--------------------#
b = pe.get_array(file_name = "test.xlsx")
test = np.array(b)

y1_test = test[1:43, 13]
y1_test = np.array(y1_test, dtype=float)

y2_test = test[1:43, 14]
y2_test = np.array(y2_test, dtype=float)

x_test = test[1:43, 0:13]
x_test = np.array(x_test, dtype=float)


#regr is used for OP_1 and regr1 is used for OP_2

regr = linear_model.LinearRegression()
regr1 = linear_model.LinearRegression()


#FOR OP_1

# Train the model using the training sets
regr.fit(x_train, y1_train)

# Make predictions using the testing set
y1_test_pred = regr.predict(x_test)
               
# Make predictions using the training set
y1_train_pred = regr.predict(x_train)


print
print
#Print the coefficients
print('Coefficients for OP_1: ', regr.coef_)
print
print('OP_1 Rsq train ', r2_score(y1_train, y1_train_pred))
print('OP_1 Rsq test ', r2_score(y1_test, y1_test_pred))
print

#FOR OP_2

# Train the model using the training sets 
regr1.fit(x_train, y2_train) 

# Make predictions using the testing set
y2_test_pred = regr1.predict(x_test)

# Make predictions using the training set
y2_train_pred = regr1.predict(x_train)

#Print the coefficients
print('Coefficients for OP_2: ', regr1.coef_)
print

print('OP_2 Rsq train ', r2_score(y2_train, y2_train_pred))
print('OP_2 Rsq test ', r2_score(y2_test, y2_test_pred))
