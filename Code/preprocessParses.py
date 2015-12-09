from spacy.en import English
from DataClasses import *
import json

def toTags(parsedTokens):
	"""Returns a list of dicts: 
	"""
	tags = []
	for token in parsedTokens:
		entityType = token.ent_type_ if token.ent_type_ != "" else "NONE"
		tags.append({
			"token": str(token).lower().strip(), 
			"entityType": str(entityType).strip(), 
			"POS": str(token.tag_).strip(),
			"dependency": str(token.dep_).strip(),
			"lemma": str(token.lemma_).strip(),
		})


	return tags


def main():
	nlpParser = English()
	for dataset in ["mc160.dev", "mc160.train", "mc160.test", "mc500.dev", "mc500.train", "mc500.test"]:
		writeParseToFile(dataset, nlpParser)

def writeParseToFile(dataset, nlpParser):
	"""
	storyID: {
		storyTextParse: [{token, NER, POS, dependency},...]
		questions: [
					[{token, NER, POS, dependency},...],
					]
	}

	"""
	#IDEA. Map storyID to storyInfo, write to file and then read from file 
	#dict = eval(open(file.txt, r).read())
	trainData = Dataset()
	trainData.appendData("../MCTest/" + dataset)

	parsedData = {}
	for story in trainData.stories:
		print story.storyID
		storyParse = {}
		storyParse['questions'] = []
		for question in story.questions:
			parsedQText = nlpParser(unicode(question.casedText))
			storyParse['questions'].append(toTags(parsedQText))


		storyTextParse = nlpParser(unicode(story.casedText))
		storyParse['storyTextParse'] = toTags(storyTextParse)

		parsedData[story.storyID] = storyParse

	with open("parse" + dataset + ".txt", "w") as f:
		json.dump(parsedData, f)
	print "Dumped dictionary"




if __name__ == "__main__":
	main()