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
	##########################################################################

	print "Appending Data"
	trainData = Dataset()
	#trainData.appendData("mc500.test", parse=True)
	trainData.appendData("mc500.train", parse=True)
	#trainData.appendData("mc160.dev", parse=True)
	# trainData.appendData("mc500.dev", parse=True)

	print "Training"
	classifier = LinearClassifier(numIters=6)
	data = trainData.getClassifierFormat(preprocessor)

	weights = classifier.trainCorrect(trainData.getEvaluationFormat(preprocessor), featureExtractor)
	print weights

	testData = Dataset()
	testData.appendData("mc160.test", parse=True)
	print testWeightsOnStories(testData.getEvaluationFormat(preprocessor), weights, featureExtractor)
	#testData = Dataset()
	#testData.appendData("mc500.test", parse=True)
	#print testWeightsOnStories(testData.getEvaluationFormat(preprocessor), weights, featureExtractor)


if __name__ == "__main__":
	main()
