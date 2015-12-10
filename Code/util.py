import re
from keywordBasedFeature import getQuestionKeyWords, getSentenceForTesting
#### STRING UTILS ####
def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False

def load_stop_words(stop_word_file):
	"""
	Utility function to load stop words from a file and return as a list of words
	@param stop_word_file Path and file name of a file containing stop words.
	@return list A list of stop words.
	"""
	stop_words = []
	for line in open(stop_word_file):
		if line.strip()[0:1] != "#":
			for word in line.split():  # in case more than one per line
				stop_words.append(word)
	return stop_words

def separate_words(text):
	"""
	Utility function to return a list of words
	@param text The text that must be split in to words.
	@param min_word_return_size The minimum no of characters a word must have to be included.
	"""
	splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
	words = []
	for single_word in splitter.split(text):
		current_word = single_word.strip().lower()
		#leave numbers in phrase, but don't count as words, since they tend to invalidate scores of their phrases
		if current_word != '' and not is_number(current_word):
			words.append(current_word)
	return words

def split_sentences(text):
	"""
	Utility function to return a list of sentences.
	@param text The text that must be split in to sentences.
	"""
	sentence_delimiters = re.compile(u'[.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s')
	sentences = sentence_delimiters.split(text)
	return sentences

def build_regex(word_list):
	"""
	Utility function to build regex pattern that matches all words in word_list
	@param word_list The list of words to match
	"""
	word_regex_list = []
	for word in word_list:
		word_regex = r'\b' + word + r'(?![\w-])'  # added look ahead for hyphen
		word_regex_list.append(word_regex)
	word_pattern = re.compile('|'.join(word_regex_list), re.IGNORECASE)
	return word_pattern

#### MATH UTILS ####

def increment(v1, scale, v2):
	for feature, value in v2.items():
		v1[feature] = v1.get(feature, 0) + value * scale

def dotProduct(v1, v2):
	if len(v1) < len(v2):
		return dotProduct(v2, v1)
	else:
		return sum(v1.get(f, 0) * v for f, v in v2.items())

#### EVALUATOR UTILS ######

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

def prettyPrint(storyData):
	"""
	{
		"text": STORY_TEXT,
		"processedStory": PREPROCESSED STORY DATA
		"question": QUESTION,
		"proposedAnswer": PROPOSED,
		"remainingAnswers": [ANSWER1, ANSWER2, ...]
		"isCorrect": BOOLEAN (just for debugging)
	}
	"""
	story = storyData["proposedAnswers"][0]
	print "Text:", story["text"]
	print "Question:", story["question"].text
	for answer in (story["remainingAnswers"] + [story["proposedAnswer"]]):
		print "\t", answer,
	print
	print

def testWeightsOnStories(data, weights, featureExtractor):
	outputFile = open("classifierOutput.txt", "w")
	numCorrect = 0 
	for datapoint in data:
		proposedAnswers = datapoint["proposedAnswers"]
		correctIndex = datapoint["correctAnswerIndex"]
		bestAnswerIndex = -1
		bestAnswerScore = float("-inf")

		outputFile.write("-----------------------\n")
		outputFile.write("Text: " + proposedAnswers[0]['text'] + "\n")
		question = proposedAnswers[0]['question']
		queryWord, qSubj, qVerb = getQuestionKeyWords(proposedAnswers[0])
		if not qSubj: qSubj = {"token": "NONE"}
		if not qVerb: qVerb = {"token": "NONE"}
		outputFile.write('Question: ' + question.text + ": " + qSubj['token'] + ", " + qVerb['token'] + "\n")


		for aIndex, proposed in enumerate(proposedAnswers):
			score = dotProduct(weights, featureExtractor(proposed))
			if score > bestAnswerScore:
				bestAnswerIndex = aIndex
				bestAnswerScore = score

			if aIndex == correctIndex:
				outputFile.write("****")
			outputFile.write(chr(ord('a') + aIndex) + ")" + proposed['proposedAnswer'] + "\t" + str(score) + "\n")
			outputFile.write(getSentenceForTesting(proposed) + '\n')

		numCorrect += correctIndex == bestAnswerIndex
		if correctIndex == bestAnswerIndex: outputFile.write("^CORRECT^\n")
		else: outputFile.write("^INCORRECT^\n")
		outputFile.write("\n\n")

	return float(numCorrect) / len(data)






