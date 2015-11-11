import re



class Dataset:
	def __init__(self):
		self.stories = []
		self.answerSets = []

	def appendData(self, dataset):
		storyInfoPath = dataset + ".tsv"
		storyAnswersPath = dataset + ".ans"
		with open(storyAnswersPath) as f:
			for line in f:
				self.answerSets.append(map(lambda ch: ord(ch) - ord('A'), line.split()))

		with open(storyInfoPath) as f:
			for i, storyInfo in enumerate(f):
				self.stories.append(Story(storyInfo))


	def getClassifierFormat(self):
		"""
		Returns story data as a list of tuples of (input, output)
		Note that each story will appear 16 times - 4 times for each of 4 questions.
		Sample elem:
			({
				text: STORY_TEXT,
				question: QUESTION,
				proposedAnswer: PROPOSED,
				isCorrect: BOOLEAN,
				remainingAnswers: [ANSWER1, ANSWER2, ...]
			}, -1)
		"""
		data = []
		for story, answerSet in zip(self.stories, self.answerSets):
			for qIndex, question in enumerate(story.questions):
				for aIndex, answer in enumerate(question.possibleAnswers):
					isCorrect = aIndex == answerSet[qIndex]
					data.append(({
						"text": story.storyText,
						"question": question,
						"proposedAnswer": answer,
						"isCorrect": isCorrect,
						"remainingAnswers": question.possibleAnswers[:aIndex] + question.possibleAnswers[aIndex + 1:]
					}, isCorrect))

		return data



	def getEvaluationFormat(self):
		"""
		Returns story data as a dictionary with
		Note that each story will appear 4 times - once for each of its questions 
		Sample elem:
			[{
				"dataPoints": [STORYCHOOSE1, STORYCHOOSE2, STORYCHOOSE3]
				"correctDataPointIndex": 0
			}
		"""
		trainingData = self.getClassifierFormat()
		evaluationData = []
		for storyIndex in xrange(0, len(trainingData), 4):
			proposedAnswers = []
			correctAnswerIndex = -1
			for answerIndex in xrange(4):
				if trainingData[storyIndex + answerIndex][1]: correctAnswerIndex = answerIndex
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
		questions (array)
			Question
				text
				numSentencesRequired (e.g multiple)
				possibleAnswers (array)

	"""
	def __init__(self, storyInfo):
		storyInfo = map(str.lower, storyInfo.split('\t'))
		self.storyID = storyInfo[0]
		self.properties = storyInfo[1]
		self.storyText = re.sub("\\\\newline", " ", re.sub("\\newline", "", storyInfo[2]))	#eliminate pesky newlines
		questions = []
		numQuestions = 4
		for i in xrange(numQuestions):
			startIndex = 3 + i * 5
			numSentencesRequired, questionText = storyInfo[startIndex].strip().split(":")
			possibleAnswers = storyInfo[startIndex + 1:startIndex + numQuestions + 1]
			possibleAnswers = map(lambda answer: re.sub(r'\s', ' ', answer).strip(), possibleAnswers) #strip newlines and tabs

			questions.append(Question(questionText.strip(), numSentencesRequired, possibleAnswers))
		self.questions = questions

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
	def __init__(self, text, numSentencesRequired, possibleAnswers):
		self.text = text
		self.numSentencesRequired = numSentencesRequired
		self.possibleAnswers = possibleAnswers