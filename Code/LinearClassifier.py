import collections
from util import dotProduct, increment

class LinearClassifier:
	def __init__(self, numIters, stepSize):
		self.numIters = numIters
		self.stepSize = stepSize

	#Stochastic gradient descent, using hingeLoss
	def train(self, dataset, featureExtractor):
		def hingeLoss(w, features, y):
			return max(0, 1 - dotProduct(w, features) * y)

	   	def lossGradient(w, features, y):
			if hingeLoss(w, features, y) <= 0:
				return {}

			return {feature: -y * magnitude for feature, magnitude in features.iteritems()}

		weights = collections.defaultdict(int)
		for _ in xrange(self.numIters):
			for example in dataset:
				input = example[0]
				output = example[1]

				features = featureExtractor(input)
				gradient = lossGradient(weights, features, output)
				increment(weights, -1 * self.stepSize, gradient)
		
		return weights