"""
Name: Yangfan Zhang
User ID: yzhang3067
"""

import numpy as np
#import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
from scipy import stats
#import LinRegLearner as lrl

class BagLearner:

    def __init__(self, learner = rt.RTLearner, kwargs = {"leaf_size":20, "verbose":False}, bags = 20, boost = False, verbose = False):
	self.kwargs = kwargs
	self.bags = bags
	self.verbose = verbose
	self.boost = boost
	self.learners = []
	self.learner = learner
	for i in range(0, bags):
	    self.learners.append(learner(**kwargs))
	    
        pass # move along, these aren't the drones you're looking for

    def author(self):
        return 'yzhang3067' # replace tb34 with your Georgia Tech username
 
    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """	
	self.dataX = dataX
	self.dataY = dataY        
	
	for i in range (0, len(self.learners)):
	    self.learners[i].addEvidence(dataX, dataY)     

        
    def query(self,testX):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
	n=testX.shape[0]
	result = np.array([0]*n)[np.newaxis]
	output = np.array([])

	for i in range(0, self.bags):
	    new_result = self.learners[i].query(testX)
	    #print i
	    #print testX.shape
	    #print new_result.shape
	    #print result.shape
	    new_result = new_result[np.newaxis]
	    result = np.vstack((result , new_result))
	
	result=result[1:,:]
	
	for j in range(0, result.shape[1]):
	    m = stats.mode(result[:,j])
	    output = np.append( output, m[0][0])
	
	return output

		
if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
