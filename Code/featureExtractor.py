import re
from keywordBasedFeature import questionAnswerKeyWordOccurence
from wordVecFeature import wordVecSumSimilarity
from cooccurrenceFeature import questionAnswerWindowCooccurrence

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
        proposedAnswerIndex: int
		remainingAnswers: [ANSWER1, ANSWER2, ...],
		processedStoryText: stemmedStoryText
		isCorrect: BOOLEAN (just for debugging)
	}
	"""

	def isNegative(parsedQuestion):
		for wordInfo in parsedQuestion:
			if wordInfo['dependency'] == 'neg':
				return True

		return False

	multiplier = -1 if isNegative(data['question'].parsedText) else 1
	return {
		"questionAnswerCooccurrence": questionAnswerWindowCooccurrence(data),
		"questionAnswerKeyWordOccurence": questionAnswerKeyWordOccurence(data),
		"wordVecSumSimilarity": wordVecSumSimilarity(data),
	}




