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
from sklearn.ensemble import RandomForestRegressor
import numpy as np


#this function extracts the X1-X13 row from the synthetic data created corresponding to the input test OP_1 value or OP_2 value 

def find_X (x_synthetic_pred, y_val):
    
	
    idx = np.where(x_synthetic_pred[:,13] >= y_val) 
    maxidx = np.array(idx)
    #print ' max_idx ='
    #print(maxidx[0,0])
    inversex = x_synthetic_pred[maxidx[0,0],0:13]
    #returns predicted X1 through X13 for a random test value that we input
    return inversex


#this function creates synthetic data from the linear combination of two randomly selected rows from the x_train set
def create_synthetic_data (x_train):

    random.seed(1234321)
    x_synthetic = []

    for x in range(1000000): #we generate 1 million samples of synthetic data

        #any arbitrary two rows in x_train ranging from 0 to 95..
        r1 = random.randint(0,95)
    	r2 = random.randint(0,95)

    	scalar1 = np.abs(random.uniform(0,1))
    	scalar2 = 1 - scalar1 #np.abs(random.uniform(0,1))

    	#linear combination of any two rows in x_train to create synthetic row of data
    	xvec = x_train[r1,:] * scalar1 + x_train[r2,:] * scalar2

    	#append synthetic row of data into synthetic data set
    	x_synthetic.append(xvec)
        
    x_synthetic = np.array(x_synthetic)
    np.savetxt('x_synthetic.txt', x_synthetic)


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


#--------------Create synthetic data based on x_train --------------#

create_synthetic_data (x_train)

#--------------Training OP-1 MLP--------------#
mlp = MLPRegressor(hidden_layer_sizes=50, activation='tanh', max_iter=500, learning_rate_init=0.1, random_state=1, solver='lbfgs', tol=0.001 )
mlp.fit(X_train_scaled, y1_train) 

#--------------Training OP-2 MLP--------------#
mlp1 = MLPRegressor(hidden_layer_sizes=4, activation='tanh', max_iter=500,  alpha = 0.1, learning_rate = 'adaptive', learning_rate_init=0.1, random_state=1, solver='lbfgs', tol=0.001 )
mlp1.fit(X_train_scaled, y2_train)


#--------------Training OP-1 LinReg--------------#
# Train the model using the training sets
linregr = linear_model.LinearRegression()
linregr.fit(x_train, y1_train)

#--------------Training OP-1 LinReg--------------#
# Train the model using the training sets
linregr1 = linear_model.LinearRegression()
linregr1.fit(x_train, y2_train) 


#--------------Training OP-1 RfReg--------------#
#Build RandomForestRegression Model

rfregr = RandomForestRegressor(max_depth=2, random_state=0)
rfregr.fit(x_train, y1_train)


#--------------Training OP-2 RfReg--------------#
#Build RandomForestRegression Model
rfregr1 = RandomForestRegressor(max_depth=6, random_state=0)
rfregr1.fit(x_train, y2_train)



#--------------------  Load Synthetic data ----------------------#

x_synthetic = np.loadtxt('x_synthetic.txt')

#----------------------------------------------------------------#
# MLP predicts OP1 and OP2 based off of the synthetic data
# Find the sorted list based on the MLP predicted values OP1 and OP2
# This enables us to look up the given OP1 value and read the corresponding
# row for the inverse prediction of X1-X13
# The range of predicted OP1 and OP2 values may not span the range of OP1 and OP2
# in the test data. Therefore we limit the index based off of max_MLP_op1 and max_MLP_op2

OP1_pred = mlp.predict(x_synthetic)
OP2_pred = mlp1.predict(x_synthetic)

x_synthetic_OP1 = np.column_stack((x_synthetic, OP1_pred))  
x_synthetic_OP2 = np.column_stack((x_synthetic, OP2_pred))  

x_synthetic_OP1_sorted_MLP = x_synthetic_OP1[x_synthetic_OP1[:,13].argsort()]
x_synthetic_OP2_sorted_MLP = x_synthetic_OP2[x_synthetic_OP2[:,13].argsort()]

max_MLP_op1 = x_synthetic_OP1_sorted_MLP[999999,13]
max_MLP_op2 = x_synthetic_OP2_sorted_MLP[999999,13]

#----------------------------------------------------------------#
# LR predict OP1 and OP2 based off of the synthetic data
# Find the sorted list based on the LR predicted values OP1 and OP2
# This enables us to look up the given OP1 value and read the corresponding
# row for the inverse prediction of X1-X13
# The range of predicted OP1 and OP2 values may not span the range of OP1 and OP2
# in the test data. Therefore we limit the index based off of max_LR_op1 and max_LR_op2

OP1_pred = linregr.predict(x_synthetic)
OP2_pred = linregr1.predict(x_synthetic)

x_synthetic_OP1 = np.column_stack((x_synthetic, OP1_pred))  
x_synthetic_OP2 = np.column_stack((x_synthetic, OP2_pred))  

x_synthetic_OP1_sorted_LR = x_synthetic_OP1[x_synthetic_OP1[:,13].argsort()]
x_synthetic_OP2_sorted_LR = x_synthetic_OP2[x_synthetic_OP2[:,13].argsort()]

max_LR_op1 = x_synthetic_OP1_sorted_LR[999999,13]
max_LR_op2 = x_synthetic_OP2_sorted_LR[999999,13]

#-----------------------------------------------------------------#
# RF predict OP1 and OP2 based off of the synthetic data
# Find the sorted list based on the RF predicted values OP1 and OP2
# This enables us to look up the given OP1 value and read the corresponding
# row for the inverse prediction of X1-X13
# The range of predicted OP1 and OP2 values  may not span the range of OP1 and OP2
# in the test data. Therefore we limit the index based off of max_RF_op1 and max_RF_op2

OP1_pred = rfregr.predict(x_synthetic)
OP2_pred = rfregr1.predict(x_synthetic)

x_synthetic_OP1 = np.column_stack((x_synthetic, OP1_pred))  
x_synthetic_OP2 = np.column_stack((x_synthetic, OP2_pred))  

x_synthetic_OP1_sorted_RF = x_synthetic_OP1[x_synthetic_OP1[:,13].argsort()]
x_synthetic_OP2_sorted_RF = x_synthetic_OP2[x_synthetic_OP2[:,13].argsort()]

max_RF_op1 = x_synthetic_OP1_sorted_RF[999999,13]
max_RF_op2 = x_synthetic_OP2_sorted_RF[999999,13]

#-----------------------------------------------------------------#




random.seed(111) #same set of 10 rows from test data for evaluating purposes

with open('inv_pred_output', 'w') as w:
   

    
    w.write(str("                      TestVal      X1       X2       X3        X4      X5       X6        X7        X8        X9       X10       X11        X12        X13") + '\n')
    for y in range(10):
        r1 = random.randint (0,41)
  

        
        #------OP1 based inverse prediction for all models ------#

                

        y_val = y1_test[r1]
        y_val_temp = y_val

        if y_val > max_MLP_op1:
            y_val = max_MLP_op1

        x_test_row = x_test[r1]
        x_test_row = np.array(x_test_row)
        x_test_row = np.insert(x_test_row, 0, y_val_temp)
        x_test_row = [ '%.2f' % elem for elem in x_test_row ]

	#write to file the ground truth test row
        w.write(str("OP1 Ground Truth Row ") + str(y+1) + ': '   + str(x_test_row) + '\n')

        OP1_inverse_X = find_X (x_synthetic_OP1_sorted_MLP, y_val)
        OP1_inverse_X = np.array(OP1_inverse_X)
        OP1_inverse_X = np.insert(OP1_inverse_X, 0, y_val_temp)
        OP1_inverse_X = [ '%.2f' % elem for elem in OP1_inverse_X ]
        w.write(str("   Model ANN OP1:       ") + str(OP1_inverse_X) + '\n')

       
        y_val = y_val_temp
        if y_val > max_LR_op1:
            y_val = max_LR_op1
           

        OP1_inverse_X = find_X (x_synthetic_OP1_sorted_LR, y_val)
        OP1_inverse_X = np.array(OP1_inverse_X)
        OP1_inverse_X = np.insert(OP1_inverse_X, 0, y_val_temp)
        OP1_inverse_X = [ '%.2f' % elem for elem in OP1_inverse_X ]
        w.write(str("    Model LR OP1:       ") + str(OP1_inverse_X) + '\n')        



        y_val = y_val_temp
        if y_val > max_RF_op1:
            y_val = max_RF_op1
           

        OP1_inverse_X = find_X (x_synthetic_OP1_sorted_RF, y_val)
        OP1_inverse_X = np.array(OP1_inverse_X)
        OP1_inverse_X = np.insert(OP1_inverse_X, 0, y_val_temp)
        OP1_inverse_X = [ '%.2f' % elem for elem in OP1_inverse_X ]
        w.write(str("    Model RF OP1:       ") + str(OP1_inverse_X) + '\n')        

        #------OP2 based inverse prediction for all models ------#
        
        y_val1 = y2_test[r1]
        y_val1_temp = y_val1

        if y_val1 > max_MLP_op2:
            y_val1 = max_MLP_op2

        x_test_row = x_test[r1]
        x_test_row = np.array(x_test_row)
        x_test_row = np.insert(x_test_row, 0, y_val1_temp)
        x_test_row = [ '%.2f' % elem for elem in x_test_row ]
        w.write(str("OP2 Ground Truth Row ") + str(y+1) + ': '   + str(x_test_row) + '\n')
 
        OP2_inverse_X = find_X (x_synthetic_OP2_sorted_MLP, y_val1)
        OP2_inverse_X = np.array(OP2_inverse_X)
        OP2_inverse_X = np.insert(OP2_inverse_X, 0, y_val1_temp)
        OP2_inverse_X = [ '%.2f' % elem for elem in OP2_inverse_X ]
        
        w.write(str("   Model ANN OP2:       ") +  str(OP2_inverse_X) + '\n')

        y_val1 = y_val1_temp
        if y_val1 > max_LR_op2:
            y_val1 = max_LR_op2
 
        OP2_inverse_X = find_X (x_synthetic_OP2_sorted_LR, y_val1)
        OP2_inverse_X = np.array(OP2_inverse_X)
        OP2_inverse_X = np.insert(OP2_inverse_X, 0, y_val1_temp)
        OP2_inverse_X = [ '%.2f' % elem for elem in OP2_inverse_X ]
        
        w.write(str("    Model LR OP2:       ") +  str(OP2_inverse_X) + '\n' )
       
 
        y_val1 = y_val1_temp
        if y_val1 > max_RF_op2:
            y_val1 = max_RF_op2
 
        OP2_inverse_X = find_X (x_synthetic_OP2_sorted_RF, y_val1)
        OP2_inverse_X = np.array(OP2_inverse_X)
        OP2_inverse_X = np.insert(OP2_inverse_X, 0, y_val1_temp)
        OP2_inverse_X = [ '%.2f' % elem for elem in OP2_inverse_X ]
        
        w.write(str("    Model RF OP2:       ") +  str(OP2_inverse_X) + '\n' + '\n')





    
print '__________________DATA written to inv_pred_output ______________________________'


