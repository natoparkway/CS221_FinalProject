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
	Data form is a dictionary: 
	{
		text: STORY_TEXT,
		question: QUESTION,
		proposedAnswer: PROPOSED,
		remainingAnswers: [ANSWER1, ANSWER2, ...]
		isCorrect: BOOLEAN (just for debugging)
	}
	"""
	return {
		"feature": data["isCorrect"] if random.random() < 0.90 else 0
	}



def main():
	mc160_train = Dataset()
	mc160_train.appendData("../MCTest/mc160.train")

	classifier = LinearClassifier(numIters=10, stepSize=0.5)
	data = mc160_train.getClassifierFormat()
	weights = classifier.train(data, featureExtractor)

	mc160_dev = Dataset()
	mc160_dev.appendData("../MCTest/mc160.dev")
	print testWeightsOnStories(mc160_dev.getEvaluationFormat(), weights, featureExtractor)


if __name__ == "__main__":
	main()