import re
import json
import numpy


def convertToString(input):
	"""
	Converts from unicode to string.
	"""
	if isinstance(input, dict):
		return {convertToString(key):convertToString(value) for key,value in input.iteritems()}
	elif isinstance(input, list):
		return [convertToString(element) for element in input]
	elif isinstance(input, unicode):
		return input.encode('utf-8')
	else:
		return input

def convertListsToNumpy(input):
    if isinstance(input, dict):
        return {key : convertListsToNumpy(value) for key,value in input.iteritems()}
    elif isinstance(input, list) and len(input)>0:
        if isinstance(input[0], float):
            return numpy.asarray(input)
        else:
            return [convertListsToNumpy(elem) for elem in input]
    else:
        return input


class Dataset:
	def __init__(self):
		self.stories = []
		self.answerSets = []
		self.parsedStoryInfo = None

	def appendData(self, dataset, parse=False):
		if parse:
			parsedFile = "parse" + dataset + ".txt"
			self.parsedStoryInfo = convertToString(json.loads(open(parsedFile).read()))
                        self.parsedStoryInfo = convertListsToNumpy(self.parsedStoryInfo)

		storyInfoPath = "../MCTest/" + dataset + ".tsv"
		storyAnswersPath = "../MCTest/" + dataset + ".ans"
		with open(storyAnswersPath) as f:
			for line in f:
				self.answerSets.append(map(lambda ch: ord(ch) - ord('A'), line.split()))

		with open(storyInfoPath) as f:
			for i, storyInfo in enumerate(f):
				self.stories.append(Story(storyInfo, parsedDict=self.parsedStoryInfo))


	def getClassifierFormat(self, preprocessFn = None):
		"""
		preprocessFn is an optional function that takes in storyText and returns data
		representing the preprocessed form of the story.
		Returns story data as a list of tuples of (input, output)
		Note that each story will appear 16 times - 4 times for each of 4 questions.
		Sample elem:
			({
				text: STORY_TEXT,
				parsedInfo: array of {
								"token": lowerCasedToken, 
								"entityType": NERTag, 
								"POS": POSTag,
								"dependency": dependency (e.g root or nsubj etc.),
								"lemma": lemma of the token,
								"vector": word vector representation (a list)
							}, one per word.
				processedStory: PREPROCESSED STORY DATA or None if no preprocessFn was supplied
				question: QUESTION,
				proposedAnswer: PROPOSED,
				isCorrect: BOOLEAN,
				remainingAnswers: [ANSWER1, ANSWER2, ...]
			}, -1)
		"""
		data = []
		for story, answerSet in zip(self.stories, self.answerSets):
			processedStory = None
			if preprocessFn:
				processedStory = preprocessFn(story.storyText)
			for qIndex, question in enumerate(story.questions):
				for aIndex, answer in enumerate(question.possibleAnswers):
					isCorrect = aIndex == answerSet[qIndex]
					data.append(({
						"text": story.storyText,
						"parsedText": story.parsedInfo,
						"processedStoryText": processedStory,
						"question": question,
						"proposedAnswer": answer,
                                                "proposedAnswerIndex": aIndex,
						"isCorrect": isCorrect,
						"remainingAnswers": question.possibleAnswers[:aIndex] + question.possibleAnswers[aIndex + 1:]
					}, isCorrect))

		return data



	def getEvaluationFormat(self, preprocessFn = None):
		"""
		Returns story data as a dictionary with
		Note that each story will appear 4 times - once for each of its questions 
		Sample elem:
			[{
				"proposedAnswers": [STORYCHOOSE1, STORYCHOOSE2, STORYCHOOSE3]
				"correctAnswerIndex": 0 or 1 or 2 or 3
			}
		"""
		trainingData = self.getClassifierFormat(preprocessFn)
		evaluationData = []
		for storyIndex in xrange(0, len(trainingData), 4):
			proposedAnswers = []
			correctAnswerIndex = -1
			for answerIndex in xrange(4):
				if trainingData[storyIndex + answerIndex][1]:
					correctAnswerIndex = answerIndex

				proposedAnswers.append(trainingData[storyIndex + answerIndex][0])
			
			evaluationData.append({
				"proposedAnswers": proposedAnswers,
				"correctAnswerIndex": correctAnswerIndex
			})

		return evaluationData




class Story:
	"""
	Story:
		storyID
		properties
		storyText
		parsedInfo: array of
			token
			POS
			NER
			dependency (e.g root vs. neg vs nsubj)
			lemma
			vector
		casedText
		questions (array)
			Question
				text
				numSentencesRequired (e.g multiple)
				possibleAnswers (array)

	"""
	def __init__(self, storyInfo, parsedDict=None):
		storyInfo = storyInfo.split('\t')
		self.storyID = storyInfo[0]
		self.properties = storyInfo[1]
		self.parsedInfo = parsedDict[self.storyID]['storyTextParse'] if parsedDict else None
		self.casedText = re.sub("\\\\newline", " ", re.sub("\\newline", "", storyInfo[2]))	#eliminate pesky newlines
		questions = []
		numQuestions = 4
		for i in xrange(numQuestions):
			startIndex = 3 + i * 5
			numSentencesRequired, questionText = storyInfo[startIndex].strip().split(":")
			possibleAnswers = storyInfo[startIndex + 1:startIndex + numQuestions + 1]
			possibleAnswers = map(lambda answer: re.sub(r'\s', ' ', answer).strip(), possibleAnswers) #strip newlines and tabs
			parsedQuestionText = parsedDict[self.storyID]['questions'][i] if parsedDict else None
                        parsedAnswers = parsedDict[self.storyID]['answers'][i] if parsedDict else None

			questions.append(Question(questionText.strip(), numSentencesRequired, possibleAnswers, parsedAnswers, parsedQuestionText))
		self.questions = questions

		#We keep the text cased until this point so that we can do better NER parsing
		self.properties = self.properties.lower()
		self.storyText = self.casedText.lower()

	def asDict(self):
		return {
			"id": self.storyID,
			"properties": self.properties,
			"text": self.storyText,
			"questions": self.questions
		}

	def prettyPrint(self):
		print "Story ID:", self.storyID
		print "Properties:", self.properties
		print "Text:", self.storyText
		print "Questions:"
		for questionNum, question in enumerate(self.questions):
			print str(questionNum + 1) + ")", question.text, "(" + question.numSentencesRequired + ")"
			for answerIndex, answer in enumerate(question.possibleAnswers):
				print "\t", answer, " "


class Question:
	def __init__(self, text, numSentencesRequired, possibleAnswers, parsedAnswers, parsedText):
		self.casedText = text
		self.casedPossibleAnswers = possibleAnswers

		self.parsedText = parsedText
		self.text = text.lower()
		self.numSentencesRequired = numSentencesRequired
		self.possibleAnswers = map(str.lower, possibleAnswers)
                self.parsedAnswers = parsedAnswers

		# print "---------------------"
		# print text
		# for word in self.parsedTokens:
		# 	print word, "NER:", word.ent_type_, "POS:", word.tag_, "Head:", word.head


