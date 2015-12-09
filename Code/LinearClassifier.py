import collections
from util import dotProduct, increment

class LinearClassifier:
	def __init__(self, numIters):
		self.numIters = numIters

	#Stochastic gradient descent, using hingeLoss
	def train(self, dataset, featureExtractor):
		def hingeLoss(w, features, y):
			return max(0, 1 - dotProduct(w, features) * y)

	   	def lossGradient(w, features, y):
			if hingeLoss(w, features, y) <= 0:
				return {}

			return {feature: -y * magnitude for feature, magnitude in features.iteritems()}

		weights = collections.defaultdict(int)
		for i, step in enumerate(xrange(self.numIters)):
			stepSize = (1 / (i + 1)) ** 2
			for example in dataset:
				input = example[0]
				output = example[1]

				features = featureExtractor(input)
				gradient = lossGradient(weights, features, output)
				increment(weights, -1 * stepSize, gradient)
		
		return weights