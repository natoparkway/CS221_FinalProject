from DataClasses import *
import DataClasses
from LinearClassifier import LinearClassifier
from util import *
import random

gold_key = Dataset()
gold_key.appendData("../MCTest/mc160.train")
gold_key.appendData("../MCTest/mc160.dev")



def featureExtractor(data):
	"""
	Data form is a dictionary: {"story": STORY, "proposedAnswer": PROPOSED}
	"""
	proposedAnswer = data["proposedAnswer"]
	if proposedAnswer == "wolfgang":
		print gold_key.getQuestionAnswer(data["question"])
	return {
		"isCorrect": 1 if proposedAnswer == gold_key.getQuestionAnswer(data["question"]) else 0,
	}



def main():
	mc160_train = Dataset()
	mc160_train.appendData("../MCTest/mc160.train")

	classifier = LinearClassifier(numIters=10, stepSize=0.5)
	data = mc160_train.getInputOutputFormat()
	weights = classifier.train(data, featureExtractor)

	def predictor(x):
		return 1 if dotProduct(featureExtractor(x), weights) > 0.0 else -1

	mc160_dev = Dataset()
	mc160_dev.appendData("../MCTest/mc160.dev")
	print weights
	#print testWeightsOnStories(weights, mc160_dev.getInputOutputFormat(), featureExtractor, mc160_dev)


if __name__ == "__main__":
	main()