import numpy as np
import LinRegLearner as lrl
import BagLearner as bl
class InsaneLearner(object):
	def __init__(self, verbose = False):
		self.learners = []
		self.numofbl = 20
		for i in range(self.numofbl):
			self.learners.append(bl.BagLearner(learner = lrl.LinRegLearner, kwargs = {}, bags = 20, boost = False, verbose = False))
	def author(self):
		return 'yzhang3067'	
	def addEvidence(self,dataX,dataY):
		for i in range(self.numofbl):
			self.learners[i].addEvidence(dataX, dataY)			
	def query(self,points):
		Y = []
		for i in range(self.numofbl):
			Y.append(self.learners[i].query(points))
		return np.mean(Y, axis = 0)