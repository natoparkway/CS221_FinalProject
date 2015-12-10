def baselineFeatureExtractor(data):
	#when doing comparisons, watch out for case! Everything is currently lower case
	return {
		"feature": 1 if data["proposedAnswer"] in data["text"] else 0
	}


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

