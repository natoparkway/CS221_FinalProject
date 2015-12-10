stopWords = []
with open("stopwords.txt") as f:
	stopWords = [word.strip() for word in f]
punctuation = ",.?!"
queryWords = ["who", "what", "when", "why", "how", "which", "where", "can", "was", "did"]
pronouns = ["he", "she", "they"]

EMPTY_PARSED_TOKEN = {
						"token": "NONE", 
						"entityType": "NONE", 
						"POS": "NONE",
						"dependency": "NONE",
						"lemma": "NONE",
						"vector": "NONE"
					}

def isNegative(parsedQuestion):
	for wordInfo in parsedQuestion:
		if wordInfo['dependency'] == 'neg':
			return True

	return False

def questionAnswerKeyWordOccurence(data):
	question = data['question']
	qSubj, qVerb = getSubjVerb(question.parsedText)
	queryWord = queryWordInQuestion(question.text)


	parsedAnswer = question.parsedAnswers[data['proposedAnswerIndex']]
	aSubj, aVerb = getSubjVerb(parsedAnswer) 
	answerKeyWord = aVerb if aSubj == None or aSubj['token'] in stopWords or aSubj['token'] in pronouns else aSubj
	if not answerKeyWord:
		answerKeyWord = parsedAnswer[0]

	score, sentence = findRelevantSentence(data['parsedText'], qSubj, qVerb, answerKeyWord)
	negativeMultiplier = -1 if isNegative(data['question'].parsedText) else 1

	return negativeMultiplier * score

def findRelevantSentence(parsedStoryText, qSubj, qVerb, qAnswer):
	"""
	parsedText: array of {
		"token": lowerCasedToken, 
		"entityType": NERTag, 
		"POS": POSTag,
		"dependency": dependency (e.g root or nsubj etc.),
		"lemma": lemma,
		"vector": wordVector
	}, one per word.
	"""
	def score(arr): return arr[0] + arr[1] + 3 * arr[2]
	qSubj = qSubj if qSubj else EMPTY_PARSED_TOKEN
	qVerb = qVerb if qVerb else EMPTY_PARSED_TOKEN
	qAnswer = qAnswer if qAnswer else EMPTY_PARSED_TOKEN
	
	currSentence = []
	bestScore = -1
	bestSentence = [{"token": "NONE", "lemma": "NONE"}]
	currOccurrences = [False, False, False]
	
	for wordInfo in parsedStoryText:
		if wordInfo['token'] in ['.', '!', '?']: 			
			if score(currOccurrences) > bestScore:
				bestScore = score(currOccurrences)
				bestSentence = currSentence
			currOccurrences = [False, False, False]
			currSentence = []
		else: 
			currSentence.append(wordInfo)

		#deal with coreference to some extent
		if wordInfo['token'] in ['he', 'she'] and qSubj['entityType'] == 'PERSON':
			currOccurrences[0] = True

		if wordInfo['lemma'] == qSubj['lemma']:
			currOccurrences[0] = True
		if wordInfo['lemma'] == qVerb['lemma']:
			currOccurrences[1] = True
		if wordInfo['lemma'] == qAnswer['lemma']:
			currOccurrences[2] = True

	return bestScore, bestSentence



def getSubjVerb(parsedText):
	verb = None
	subj = None

	personFound = False
	rootVerbFound = False
	isNegative = False
	for wordInfo in parsedText:
		lemmatizedToken = wordInfo['lemma']
		if wordInfo['token'] in queryWords:	#DON'T PICK UP WHO, WHAT ETC.
			continue
		#Find the Subject
		if wordInfo['entityType'] == "PERSON" and not personFound:
			subj = wordInfo
			personFound = True #A person is probably the subject
		if wordInfo['dependency'] == 'nsubj' and not personFound:
			subj = wordInfo
		if 'NN' in wordInfo['POS'] and not subj:
			subj = wordInfo

		#Find the noun
		if 'VB' in wordInfo['POS'] and not rootVerbFound: #Worst case, we just take a random verb
			verb = wordInfo
		if wordInfo['dependency'] == 'ROOT' and 'VB' in wordInfo['POS'] and not rootVerbFound:
			verb = wordInfo
			rootVerbFound = True


	return subj, verb

def queryWordInQuestion(text):
	for word in queryWords:
		if word in text:
			return word

	return "NONE"

########################################
def parsedToString(tokens, lemma=False):
	text = ""
	for wordInfo in tokens:
		if lemma:
			text += wordInfo['lemma'] + " "
		else:
			text += wordInfo['token'] + " "

	return text

def getSentenceForTesting(data):
	"""
	Just for utils
	"""

	question = data['question']
	qSubj, qVerb = getSubjVerb(question.parsedText)
	queryWord = queryWordInQuestion(question.text)


	parsedAnswer = question.parsedAnswers[data['proposedAnswerIndex']]
	aSubj, aVerb = getSubjVerb(parsedAnswer) 
	answerKeyWord = aVerb if aSubj == None or aSubj['token'] in stopWords or aSubj['token'] in pronouns else aSubj
	if not answerKeyWord:
		answerKeyWord = parsedAnswer[0]

	score, sentence = findRelevantSentence(data['parsedText'], qSubj, qVerb, answerKeyWord)
	return parsedToString(sentence) + ":" + answerKeyWord['token']

def getQuestionKeyWords(data):
	question = data['question']
	qSubj, qVerb = getSubjVerb(question.parsedText)
	queryWord = queryWordInQuestion(question.text)
	return queryWord, qSubj, qVerb
