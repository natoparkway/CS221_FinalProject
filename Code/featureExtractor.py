import re
from util import *

stopWords = []
with open("stopwords.txt") as f:
	stopWords = [word.strip() for word in f]
punctuation = ",.?!"
queryWords = ["who", "what", "when", "why", "how", "which", "where", "can", "was", "did"]
stemmer = SnowballStemmer("english").stem

incorrectParses = 0
totalParses = 0

def baselineFeatureExtractor(data):
	#when doing comparisons, watch out for case! Everything is currently lower case
	return {
		"feature": 1 if data["proposedAnswer"] in data["text"] else 0
	}

def betterFeatureExtractor(data):
	"""
	Data form is a dictionary: 
	{
		text: STORY_TEXT,
		processedStory: PREPROCESSED STORY TEXT
		parsedText: array of {
								"token": lowerCasedToken, 
								"entityType": NERTag, 
								"POS": POSTag,
								"dependency": dependency (e.g root or nsubj etc.),
								"lemma": lemma,
								"vector": wordVector
							}, one per word.
		question: QUESTION,
		proposedAnswer: proposedText,
		remainingAnswers: [ANSWER1, ANSWER2, ...],
		processedStoryText: stemmedStoryText
		isCorrect: BOOLEAN (just for debugging)
	}
	"""

	"""
	Utilizes rake to do keyword weighting.
	Features include: overlap of words from question, proposed answer, and keywords
	"""

	nextFeatureTests(data)

	print incorrectParses, totalParses
	return {
		"questionAnswerCooccurrence": questionAnswerWindowCooccurrence(data),
	}

def nextFeatureTests(data):
	question = data['question']
	qSubj, qVerb = getSubjVerb(question.parsedText)
	queryWord = queryWordInQuestion(question.text)

	print question.text
	print queryWord, qSubj, qVerb


def getSubjVerb(parsedText):
	verb = ""
	subj = ""

	personFound = False
	rootVerbFound = False
	for wordInfo in parsedText:
		lemmatizedToken = wordInfo['lemma']
		#Find the Subject
		if wordInfo['entityType'] == "PERSON" and not personFound:
			subj = lemmatizedToken
			personFound = True #A person is probably the subject
		if wordInfo['dependency'] == 'nsubj' and not personFound:
			subj = lemmatizedToken
		if 'NN' in wordInfo['POS'] and not subj:
			subj = lemmatizedToken

		#Find the noun
		if 'VB' in wordInfo['POS'] and not rootVerbFound: #Worst case, we just take a random verb
			verb = lemmatizedToken
		if wordInfo['dependency'] == 'ROOT' and 'VB' in wordInfo['POS'] and not rootVerbFound:
			verb = lemmatizedToken
			rootVerbFound = True


	return subj, verb

def queryWordInQuestion(text):
	for word in queryWords:
		if word in text:
			return word

	return "NONE"

def toBagOfWords(questionText, answer):
	return [word.strip(punctuation) for word in (questionText.split() + answer.split()) if word not in stopWords]

def stripPunctAndStopWords(arr):
	return [elem.strip(punctuation) for elem in arr if elem not in stopWords]

def questionAnswerWindowCooccurrence(data):
	"""
	Returns the greatest percentage of question-answer words in any window in the story text.

	We stem the question and answer words and strip stop words and punctuation.
	Proprocessed story text has punctuation and stop words removed. It is also stemmed.

	Notes: Window size 6 is the best of 5 - 10 
	"""
	windowSize = 6
	score = 0
	proposedAnswer = data["proposedAnswer"]
	question = data["question"].text
	stemmedStoryText = data["processedStoryText"]
	#stemmedStoryText = " ".join(map(stemmer, stripPunctAndStopWords(data["text"].split())))

	storyTextArray = [word.strip(punctuation) for word in stemmedStoryText.split()]
	qaWords = map(stemmer, toBagOfWords(question, proposedAnswer))

	bestWindowScore = -1
	for i in xrange(len(storyTextArray) - windowSize):
		window = storyTextArray[i:i + windowSize]
		wordsInWindow = [word for word in qaWords if word in window]
		score = float(len(wordsInWindow)) / (len(set(window + qaWords)))
		if score > bestWindowScore:
			bestWindowScore = score

	return bestWindowScore





######DEPRECATED FEATURES###################
def questionAnswerSentenceCooccurrence(data):
	"""
	Returns the average number of times the words in a question-answer pair cooccur in every sentence in the text

	Notes: This does basically the same as the window cooccurrence feature.
	"""
	score = 0
	sentences = data["text"].split('.')
	qaWords = toBagOfWords(data["question"], data["proposedAnswer"])

	for sentence in sentences:
		sentence = stripPunctAndStopWords(sentence.split())
		wordsInSentence = [word for word in qaWords if word in sentence]
		score += len(wordsInSentence)

	return float(score) / len(sentences)


def stopWordFilteredCoocurrence(data):
	"""
	Utilizes rake to do keyword weighting.
	Features include: overlap of words from question, proposed answer, and keywords
	"""
	features = {}

	if data["processedStory"]:
		phraseList = data["processedStory"][0]
		print phraseList
		stopWordsPattern = data["processedStory"][1]

		questionAnsText = re.sub(r'\?', '', data["question"].text + " " + data["proposedAnswer"])
		questionAnsText = stem(re.sub(stopWordsPattern, '', questionAnsText))
		questionAnsList = questionAnsText.split()
		questionAnsSet = set(questionAnsList)


		maxScore = float("-inf")
		bestIndex = 0
		windowSize = 5

		for windowIndex in xrange(len(phraseList) - windowSize):
			tempNum = 0.0
			tempDenom = 0.01
			tempScore = 0.0
			for i in xrange(windowSize):
				phrase = phraseList[windowIndex + i]
				phraseSet = set(phrase.split())
				tempNum += float(len(phraseSet & questionAnsSet))
				tempDenom += len(phraseSet | questionAnsSet)
			tempScore = tempNum / tempDenom
			if tempScore > maxScore:
				bestIndex = windowIndex
				maxScore = tempScore

		# print "Question: " + data["question"].text
		# print "Proposed answer: " + data["proposedAnswer"]
		# print questionAnsSet
		# print "Correct" if data["isCorrect"] else "Incorrect"
		# if bestIndex != -1:
		# 	print phraseList[bestIndex : bestIndex + windowSize]
		# print "Score: %f" % (maxScore,)

	return maxScore

