import re
from keywordBasedFeature import questionAnswerKeyWordOccurence
from nltk.stem import SnowballStemmer

stopWords = []
with open("stopwords.txt") as f:
	stopWords = [word.strip() for word in f]
punctuation = ",.?!"
stemmer = SnowballStemmer("english").stem


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
		proposedAnswerIndex: int,
		remainingAnswers: [ANSWER1, ANSWER2, ...],
		processedStoryText: stemmedStoryText
		isCorrect: BOOLEAN (just for debugging)
	}
	"""

	"""
	Utilizes rake to do keyword weighting.
	Features include: overlap of words from question, proposed answer, and keywords
	"""


	return {
		"questionAnswerCooccurrence": questionAnswerWindowCooccurrence(data),
		"questionAnswerKeyWordOccurence": questionAnswerKeyWordOccurence(data),
	}




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


