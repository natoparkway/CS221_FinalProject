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


	def getInputOutputFormat(self):
		"""
		Returns story data as a tuple of (input, output)
		Sample elem:
			({
				text: STORY_TEXT,
				question: QUESTION,
				proposedAnswer: PROPOSED,
			}, 0)
		"""
		data = []
		for story, answerSet in zip(self.stories, self.answerSets):
			for qIndex, question in enumerate(story.questions):
				for aIndex, answer in enumerate(question.possibleAnswers):
					isCorrect = 1 if aIndex == answerSet[qIndex] else -1
					data.append(({
						"text": story.storyText,
						"question": question,
						"proposedAnswer": answer
					}, isCorrect))

		return data

	def getQuestionAnswer(self, question):
		return "NOT IMPLEMENTED"

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
	def __init__(self, storyInfo, ):
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