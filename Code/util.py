def increment(v1, scale, v2):
	for feature, value in v2.items():
		v1[feature] = v1.get(feature, 0) + value * scale

def dotProduct(v1, v2):
	if len(v1) < len(v2):
		return dotProduct(v2, v1)
	else:
		return sum(v1.get(f, 0) * v for f, v in v2.items())

def evaluatePredictor(examples, predictor):
	'''
	predictor: a function that takes an x and returns a predicted y.
	Given a list of examples (x, y), makes predictions based on |predict| and returns the fraction
	of misclassiied examples.
	'''
	error = 0
	for x, y in examples:
		print predictor(x), y
		if predictor(x) != y:
			error += 1
	return 1.0 * error / len(examples)

def testWeightsOnStories(data, weights, featureExtractor):
	numCorrect = 0 
	for datapoint in data:
		proposedAnswers = datapoint["proposedAnswers"]
		correctIndex = datapoint["correctAnswerIndex"]
		bestAnswerIndex = -1
		bestAnswerScore = float("-inf")
		for aIndex, proposed in enumerate(proposedAnswers):
			score = dotProduct(weights, featureExtractor(proposed))
			if score > bestAnswerScore:
				bestAnswerIndex = aIndex
				bestAnswerScore = score
		numCorrect += correctIndex == bestAnswerIndex

	return float(numCorrect) / len(data)