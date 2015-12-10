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


	return {
		"questionAnswerCooccurrence": questionAnswerWindowCooccurrence(data),
		"questionAnswerKeyWordOccurence": questionAnswerKeyWordOccurence(data),
		#"wordVecSumSimilarity": wordVecSumSimilarity(data)
	}




