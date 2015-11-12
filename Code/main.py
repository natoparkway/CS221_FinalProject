from DataClasses import *
import DataClasses
from LinearClassifier import LinearClassifier
from util import *
import random
from rake import *

gold_key = Dataset()
gold_key.appendData("../MCTest/mc160.train")
gold_key.appendData("../MCTest/mc160.dev")



def featureExtractor(data):
	"""
	Data form is a dictionary: 
	{
		text: STORY_TEXT,
		processedStory: PREPROCESSED STORY DATA
		question: QUESTION,
		proposedAnswer: PROPOSED,
		remainingAnswers: [ANSWER1, ANSWER2, ...]
		isCorrect: BOOLEAN (just for debugging)
	}
	"""
	return {
		"feature": data["isCorrect"] if random.random() < 0.90 else 0
	}

def betterBaselineFeatureExtractor(data):
	"""
	Utilizes rake to do keyword weighting.
	Features include: overlap of words from question, proposed answer, and keywords
	"""
	keywordOverlap = []
	return {
		"feature": random.random()
	}

def rakePreprocess(storyText):
	"""
	Keyword extraction and weighting with the RAKE algorithm.
	"""
	raker = Rake("SmartStoplist.txt")
	return raker.run(storyText)

def main():
	"""
	Change these values to change feature extractor / preprocessing being used
	"""
	usingFeatureExtractor = betterBaselineFeatureExtractor
	usingPreprocess = rakePreprocess
	##########################################################################

	mc160_train = Dataset()
	mc160_train.appendData("../MCTest/mc160.train")

	classifier = LinearClassifier(numIters=10, stepSize=0.5)
	data = mc160_train.getClassifierFormat(usingPreprocess)
	weights = classifier.train(data, usingFeatureExtractor)

	mc160_dev = Dataset()
	mc160_dev.appendData("../MCTest/mc160.dev")
	print testWeightsOnStories(mc160_dev.getEvaluationFormat(usingPreprocess), weights, featureExtractor)


if __name__ == "__main__":
	main()