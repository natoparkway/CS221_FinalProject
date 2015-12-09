from util import *
import re

punctuation = ",.?!"
def removeStopwordsAndStem(storyText):
	"""
	Removes punctuation and stop words, then stems text.
	"""
	with open("stopwords.txt") as f:
		stopWords = [word.strip() for word in f]

	storyText = " ".join([SnowballStemmer("english").stem(word.strip(punctuation)) for word in storyText.split() if word not in stopWords])
	return storyText
