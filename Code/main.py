from DataClasses import *
from LinearClassifier import LinearClassifier
from util import *
import random
from featureExtractor import *
from preprocessor import *
from pprint import PrettyPrinter


def main():
	"""
	Change these values to change feature extractor / preprocessing being used
	"""
	featureExtractor = betterFeatureExtractor 
	preprocessor = removeStopwordsAndStem
	testOnTrainSet = False 
	testOn500 = False 
	testOn160 = True 
	##########################################################################

	print "Appending Data"
	trainData = Dataset()
	trainData.appendData("mc160.train", parse=True)

	print "Training"
	classifier = LinearClassifier(numIters=10)
	data = trainData.getClassifierFormat(preprocessor)

	weights = classifier.train(data, featureExtractor)
	print weights


	if testOnTrainSet:
		print "Testing (on train set)"
		print testWeightsOnStories(trainData.getEvaluationFormat(preprocessor), weights, featureExtractor)
	else:
		testData = Dataset()
		if testOn500:
			print "Prepping Test Data (MC500)"
			testData.appendData("mc500.dev", parse=True)
		if testOn160:
			print "Prepping Test Data (MC160)"
			testData.appendData("mc160.dev", parse=True)
		print "Testing"
		print testWeightsOnStories(testData.getEvaluationFormat(preprocessor), weights, featureExtractor)


if __name__ == "__main__":
	main()
