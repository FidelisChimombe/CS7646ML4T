"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math
import DTLearner as dt
import LinRegLearner as lrl

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4LinReg(seed=1489683273):
    # Here's is an example of creating a Y from randomly generated
    # X with multiple columns
    # Y = X[:,0] + np.sin(X[:,1]) + X[:,2]**2 + X[:,3]**3
	np.random.seed(seed)
	columns = np.random.randint(2,1000)
	rows = np.random.randint(10,1000)
	X = np.zeros((rows,columns))
	Y = np.random.random(size = (rows,))*2*rows-rows
	for i in range(columns):
		X[:,i] = Y	
	return X, Y

def best4DT(seed=1489683273):
	np.random.seed(seed)
	columns = np.random.randint(2,1000)
	rows = np.random.randint(10,1000)
	X = np.random.random(size = (rows,columns))*2*rows*columns-rows*columns
	Y = X[:,-1]		
	return X, Y
	
def author():
    return 'yzhang3067' #Change this to your user ID

if __name__=="__main__":
    print "they call me Tim."
