from nltk.stem import SnowballStemmer

stopWords = []
with open("stopwords.txt") as f:
	stopWords = [word.strip() for word in f]
punctuation = ",.?!"
queryWords = ["who", "what", "when", "why", "how", "which", "where", "can", "was", "did"]
stemmer = SnowballStemmer("english").stem

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
	numSents = data['question'].numSentencesRequired
	windowSize = 6
	if numSents == 'multiple':
		windowSize *= 2
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
