import collections
from util import dotProduct, increment
import math

def softmax(arr):
	for elem in arr:
		if elem < 0:
			arr = map(lambda x: x + elem, arr)


	expsum = sum(math.exp(elem) for elem in arr)
	probabilityArr = []
	for i, elem in enumerate(arr):
		probabilityArr.append(math.exp(elem) / expsum)
	return probabilityArr

class LinearClassifier:
	def __init__(self, numIters):
		self.numIters = 30 

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
			for example in dataset:
				input = example[0]
				output = example[1]

				features = featureExtractor(input)
				gradient = lossGradient(weights, features, output)

				increment(weights, -1 * stepSize, gradient)
		
		return weights

	def trainCorrect(self, dataset, featureExtractor):
		def squareLoss(answerProb, y):
			return (answerProb - y) ** 2

	   	def lossGradient(answerProb, y, features):
	   		derivative = 2 * (answerProb - y)
			return {feature: derivative * magnitude for feature, magnitude in features.iteritems()}

		def getAnswerProbs(weights, questionData):
			proposedAnswers = questionData["proposedAnswers"]
			correctIndex = questionData["correctAnswerIndex"]
			answerScores = []

			for aIndex, proposed in enumerate(proposedAnswers):
				score = dotProduct(weights, featureExtractor(proposed))
				answerScores.append(score)

			return softmax(answerScores)

		weights = collections.defaultdict(int)
		for _ in xrange(self.numIters):
			error = 0
			stepSize = 0.12
			for questionData in dataset:
				yVector = [int(i == questionData["correctAnswerIndex"]) for i in xrange(4)] #[0, 1, 0, 0], where the 1 indicates which is correct
				answerProbs = getAnswerProbs(weights, questionData) #[0.2, 0.7, 0.06, 0.04] -> each indicates the likelihood
				# print answerProbs, yVector

				proposedAnswers = questionData["proposedAnswers"]
				for aIndex, proposed in enumerate(proposedAnswers):
					error += squareLoss(answerProbs[aIndex], yVector[aIndex])
					features = featureExtractor(proposed)
					gradient = lossGradient(answerProbs[aIndex], yVector[aIndex], features)
					increment(weights, -1 * stepSize, gradient)

			print "Error:", error, weights
		
		return weights


