from DataClasses import *
import DataClasses
from LinearClassifier import LinearClassifier
from util import *
import random
from rake import *
import re
from nltk.stem import *

gold_key = Dataset()
gold_key.appendData("../MCTest/mc160.train")
gold_key.appendData("../MCTest/mc160.dev")

stemmer = SnowballStemmer("english")

def stem(nltkStemmer, text):
	"""
	text is a string, possibly of multiple words
	return a stemmed string
	"""
	return " ".join([stemmer.stem(word) for word in text.split()])

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
	features = {}

	if data["processedStory"]: #so that we can test even if there is no preprocessing
		keyWordDict = data["processedStory"][0]
		phraseList = data["processedStory"][1]
		stopWordsPattern = data["processedStory"][2]

		questionAnsText = re.sub(r'\?', '', data["question"].text + " " + data["proposedAnswer"])
		questionAnsText = stem(stemmer, re.sub(stopWordsPattern, '', questionAnsText))
		questionAnsList = questionAnsText.split()
		questionAnsSet = set(questionAnsList)


		maxScore = float("-inf")
		bestIndex = -1
		windowSize = 5

		for windowIndex in xrange(len(phraseList) - windowSize):
			tempNum = 0.0
			tempDenom = 0.01
			tempScore = 0.0
			for i in xrange(windowSize):
				phrase = phraseList[windowIndex + i]
				phraseSet = set(phrase.split())
				numerator = float(len(phraseSet & questionAnsSet))
				denominator = len(phraseSet | questionAnsSet)
				tempNum += numerator
				tempDenom += denominator
			tempScore = tempNum / tempDenom
			if tempScore > maxScore:
				bestIndex = windowIndex
				maxScore = tempScore

		print "Question: " + data["question"].text
		print "Proposed answer: " + data["proposedAnswer"]
		print questionAnsSet
		print "Correct" if data["isCorrect"] else "Incorrect"
		if bestIndex != -1:
			print phraseList[bestIndex : bestIndex + windowSize]
		print "Score: %f" % (maxScore,)

		features["keyWordFeature"] = maxScore
		#print keyWordScore
	return features

def rakePreprocess(storyText):
	"""
	Keyword extraction and weighting with the RAKE algorithm.
	"""
	stop_words_pattern = build_stop_word_regex("SmartStoplist.txt")
	sentence_list = split_sentences(storyText)
	phrase_list = generate_candidate_keywords(sentence_list, stop_words_pattern)
	phrase_list = [stem(stemmer, phrase) for phrase in phrase_list]
	word_scores = calculate_word_scores(phrase_list)
	output = generate_candidate_keyword_scores(phrase_list, word_scores)
	# regexList = []
	# for word in output.iterkeys():
	#     wordRegex = r'\b' + word + r'(?![\w-])'  # added look ahead for hyphen
	#     regexList.append(wordRegex)
	# phrasePattern = re.compile('|'.join(regexList), re.IGNORECASE)
	# punctuationPattern = re.compile(u'[.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]')
	# removePunctuation = re.sub(punctuationPattern, ' ', storyText)
	# # use pattern to process story into list of word
	# tmp = re.sub(phrasePattern, lambda x: "|" + x.group(0) + "|", removePunctuation)
	# document = []
	# for val in tmp.split('|'):
	# 	phr = val.strip()
	# 	if len(phr) > 0:
	# 		document.append(phr)

	return [output, phrase_list, stop_words_pattern]

def main():
	"""
	Change these values to change feature extractor / preprocessing being used
	"""
	usingFeatureExtractor = betterBaselineFeatureExtractor
	usingPreprocess = rakePreprocess #if you don't want any preprocessing, set to None
	##########################################################################

	mc160_train = Dataset()
	mc160_train.appendData("../MCTest/mc160.train")

	classifier = LinearClassifier(numIters=10, stepSize=0.5)
	data = mc160_train.getClassifierFormat(usingPreprocess)
	weights = classifier.train(data, usingFeatureExtractor)

	mc160_dev = Dataset()
	mc160_dev.appendData("../MCTest/mc160.dev")
	print testWeightsOnStories(mc160_dev.getEvaluationFormat(usingPreprocess), weights, usingFeatureExtractor)


if __name__ == "__main__":
	main()