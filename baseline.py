import re


class Story:
	def __init__(self, storyInfo):
		storyInfo = map(str.lower, storyInfo.split('\t'))
		self.storyID = storyInfo[0]
		self.properties = storyInfo[1]
		self.storyText = re.sub("\\\\newline", " ", re.sub("\\newline", "", storyInfo[2]))
		questions = []
		self.answers = []
		numQuestions = 4
		for i in xrange(numQuestions):
			startIndex = 3 + i * 5
			informationType, questionText = storyInfo[startIndex].strip().split(":")
			questions.append({"question": questionText.strip(), "informationType": informationType, 
								"answers": storyInfo[startIndex + 1:startIndex + numQuestions + 1]})

		self.questions = questions

	def asDict(self):
		return {
			"id": self.storyID,
			"properties": self.properties,
			"text": self.storyText,
			"questions": self.questions
		}

	def answerQuestions(self):
		for questionInfo in self.questions:
			answerIndex = self._findAnswerToQuestion(questionInfo)
			self.answers.append("ABCD"[answerIndex])
			print "ABCD"[answerIndex], questionInfo["answers"][answerIndex]
		return self.answers


	def _findAnswerToQuestion(self, questionInfo):
		questionText = questionInfo["question"].strip("?")
		answers = questionInfo["answers"]
		return self._findMostSimilarSentence(questionText, answers, self.storyText)
		# mostSimilarSentence = self._findMostSimilarSentence(questionText, answers, self.storyText)

		# for i, answer in enumerate(answers):
		# 	if mostSimilarSentence and answer in mostSimilarSentence:
		# 		return i
		# return 2 #C is always right


	#returns the sentence most similar to a given text in a story.
	def _findMostSimilarSentence(self, questionText, answers, story):
		def jaccardSim(s1, s2):
			s1 = s1.split()
			s2 = s2.split()
			return float(len(set(s1) & set(s2))) / len(set(s1) | set(s2)) 

		sentences = map(str.strip, story.split("."))
		possibleAnswerSentences = []
		answerProbabilities = [max((jaccardSim(questionText + " " + answer, sentence)) for sentence in sentences) for answer in answers]
		return answerProbabilities.index(max(answerProbabilities))
		# for answer in answers:
		# 	possibleAnswerSentences += [sentence for sentence in sentences if answer in sentence]
		
		# if not possibleAnswerSentences:
		# 	return None
		
		# bestMatch = max((jaccardSim(questionText, sentence), sentence) for sentence in possibleAnswerSentences)		
		# return bestMatch[1]


def readInData(filename):
	with open(filename) as f:
		allStories = [Story(storyInfo) for storyInfo in f]

	return allStories

def readInAnswers(filename):
	with open(filename) as f:
		allAnswers = []
		for line in f:
			allAnswers.append(line.split("\t"))

	return allAnswers

def main():
	allStories = readInData("MCTest/mc160.dev.tsv")
	allAnswers = readInAnswers("MCTest/mc160.dev.ans")
	numCorrect = 0.0

	for correctAnswers, story in zip(allAnswers, allStories):
		proposedAnswers = story.answerQuestions()
		numCorrect += sum(correctAnswers[i] == proposedAnswers[i] for i in xrange(len(correctAnswers)))

	print numCorrect / len(allStories) / 4.0




if __name__ == "__main__":
	main()