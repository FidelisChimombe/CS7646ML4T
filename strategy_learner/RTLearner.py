"""
Name: Yangfan Zhang
User ID: yzhang3067
"""
import numpy as np
import random
from scipy import stats

class RTLearner:

    def __init__(self, leaf_size, verbose = False):
	self.leaf_size = leaf_size
	self.verbose = verbose
        pass # move along, these aren't the drones you're looking for

    def author(self):
        return 'yzhang3067' # replace tb34 with your Georgia Tech username

    #get the best factor for split, return 
    def get_feature(self, dataX, dataY):
	
	n = dataX.shape[1]
	max_id = random.randint(0, n - 1)
	return max_id 
	
    def isSame(self, dataY):
	for i in range(0, dataY.shape[0]):
	   if dataY[i] != dataY[0]:
		return False
	return True
    

    def build_tree(self,dataX,dataY):
	# only one leaf left
	if dataX.shape[0] <= self.leaf_size:
	    #counts = np.bincount(dataY)
	    m = stats.mode(dataY)
	    leaf = np.array([ -1, m[0][0] , None, None])
	    leaf = leaf[np.newaxis]
	    return leaf
	
	#see if all Y are exact same

	if self.isSame(dataY) == True:
	    leaf = np.array([ -1, dataY[0], None, None])
	    leaf = leaf[np.newaxis]
	    return leaf

	#get most correlated factor's column id
	factor_id = self.get_feature(dataX,dataY)
        #get value for split
	n = dataX.shape[1]
	m = dataX.shape[0]
	while True:	
		random_1 = random.randint(0, m/2)
		random_2 = random.randint(m/2, m - 1)
		if not random_1==random_2:
			break

	splitVal = ( dataX[random_1][factor_id] + dataX[random_2][factor_id]) /2 
	#get split values into two subtrees
	
	#sub_leftX=dataX[dataX[:,factor_id]<=splitVal,:]
	#sub_leftY=dataY[dataX[:,factor_id]<=splitVal]

        #sub_rightX=dataX[dataX[:,factor_id]>splitVal,:]
        #sub_rightY=dataY[dataX[:,factor_id]>splitVal]
	sub_leftX = np.ndarray(shape=(1,n))
 	sub_rightX = np.ndarray(shape=(1,n))
 	sub_leftY = np.array([0])
 	sub_rightY = np.array([0])
	for i in range(0,m):
	    if dataX[i][factor_id] <= splitVal:
		sub_leftX=np.vstack((sub_leftX,dataX[i]))
		sub_leftY=np.append(sub_leftY,dataY[i])
	    else:
		sub_rightX=np.vstack((sub_rightX,dataX[i]))
		sub_rightY=np.append(sub_rightY,dataY[i])
	sub_leftX = sub_leftX[1:,:]
	sub_rightX = sub_rightX[1:,:]
	sub_leftY = sub_leftY[1:]
	sub_rightY=sub_rightY[1:]
	
	#do the recursion and get the root


	if sub_leftX.shape[0] == 0:
	    m_left = stats.mode(dataY) 
	    return np.array([[-1,m_left[0][0],None,None]])
	if sub_rightX.shape[0] == 0:
	    m_right = stats.mode(dataY)
	    return np.array([[-1,m_right[0][0],None,None]])

	left_tree = self.build_tree(sub_leftX, sub_leftY )
	right_tree = self.build_tree(sub_rightX, sub_rightY)
	root = np.array([factor_id, splitVal, 1, left_tree.shape[0]+1])

	#return np.array([root, left_tree, right_tree])
	return np.vstack((root,left_tree,right_tree))
    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
	
	self.dataX = dataX
	self.dataY = dataY        
        
        self.tree = self.build_tree(dataX, dataY)
        
  	return self.tree
        
    def query(self,testX):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
	tree = self.tree
	result = np.array([])
	count = testX.shape[0]
	#print count
	#print type(testX)
	#print type(testX)
	#print testX[0,:]
	for i in range (0, count):
	    test_row = testX[i]
	    j = 0
	    tree_row = tree[j,:]
	    while tree_row[0] != -1:
		fac_id = tree_row[0]
		fac_id=int(fac_id)
		if test_row[fac_id] <= tree_row[1]:
		    j +=  tree_row[2]
		else:
		    j +=  tree_row[3] 
		j=int(j)
	    	tree_row = tree[j,:]
	    #print tree[j][1]
	    result=np.append(result,tree[j][1])
	#print result.shape			
	return result
		
if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
