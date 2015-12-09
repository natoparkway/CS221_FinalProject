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
	trainData.appendData("mc160.train", parse=True)

	print "Training"
	classifier = LinearClassifier(numIters=10)
	data = trainData.getClassifierFormat(preprocessor)

	weights = classifier.train(data, featureExtractor)
	print weights

	print "Prepping Test Data"
	mc160_dev = Dataset()
	mc160_dev.appendData("mc160.dev", parse=True)

	print "Testing"
	print testWeightsOnStories(mc160_dev.getEvaluationFormat(preprocessor), weights, featureExtractor)


if __name__ == "__main__":
	main()