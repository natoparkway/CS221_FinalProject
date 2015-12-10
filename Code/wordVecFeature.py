from util import *
import numpy
import itertools
from scipy import spatial

queryWords = ["who", "what", "when", "why", "how", "which", "where", "can", "was", "did"]

queryWords = ["who", "what", "when", "why", "how", "which", "where", "can", "was", "did"]

# Returns an array of arrays of parsed tokens.
# Each array in the original array represents one sentence in the text.
# It is assumed sentences are separated by one of ".!?"

def getSentences(parsedText):
    sentences = []
    currSentence = []
    for wordInfo in parsedText:
        if wordInfo['token'] in ".!?":            
            sentences.append(currSentence)
            currSentence = []
        else:
            currSentence.append(wordInfo)
    return sentences

# Returns the sum of the word vectors of the parsed words.

def getWordVecSum(parsedWords):
    sumArray = numpy.zeros_like(parsedWords[0]['vector'])
    for token in parsedWords:
        sumArray = numpy.add(sumArray, token['vector'])
    return sumArray

# Returns the cosine similarity between two vectors

def getCosSim(vec1, vec2):
    sim = 1 - spatial.distance.cosine(vec1, vec2)
    return sim  

# Normalizes the given vector.
# If the given vector consists of all zeros, returns it.

def normalize(vec):
    if numpy.any(vec):
        return vec/numpy.linalg.norm(vec)
    else:
        return vec 

# Returns the cosine similarity between the proposed answer and the most similar sentence(s) in the story.
# If the question requires only one sentences, checks sentences one by one,
# if it requires multiple sentences, checks pairs of sentences.

def wordVecSumSimilarity(data):
    qParsedWords = data['question'].parsedText
    aParsedWords = data['question'].parsedAnswers[data['proposedAnswerIndex']]
    qaVecSum = normalize(getWordVecSum(qParsedWords + aParsedWords))
    sentences = getSentences(data['parsedText'])
    if data['question'].numSentencesRequired == 'multiple':
        return multipleSimilarity(qaVecSum, sentences)
    else:
        return singleSimilarity(qaVecSum, sentences)

# Returns the highest cosine similarity between the given word vector sum vector of question and answers
# and each of the sentences in the given sentences. Sentences is a list of lists of parse tokens.

def singleSimilarity(qaVecSum, sentences):
    bestSim = 0
    for sentence in sentences:
        if len(sentence) == 0:
            continue
        curSentVecSum = getWordVecSum(sentence)
        if numpy.any(curSentVecSum):
            curSentVecSum = normalize(curSentVecSum)
            bestSim = max(bestSim, getCosSim(qaVecSum, curSentVecSum))
    return bestSim


# For questions that require multiple sentences, checks similarity of question + answer word vectors against every pair of consecutive sentences in the story.

def multipleSimilarity(qaVecSum, sentences):
    sentWindowSize = 2
    bestSim = 0
    for i in xrange(len(sentences) - sentWindowSize):
        sentWindow = sentences[i:i+sentWindowSize]
        sentWordCombo = sum(sentWindow, []) 
        if len(sentWordCombo) == 0:
            continue
        sentVecSum = getWordVecSum(sentWordCombo)
        if numpy.any(sentVecSum):
            sentVecSum = normalize(sentVecSum)
            bestSim = max(bestSim, getCosSim(qaVecSum, sentVecSum))
    return bestSim



######UNUSED FEATURES (They probably lower the score):##############


# Compares the question + answers word vectors agains all possible sentence pairs in the story

def allPairsMultSimilarity(qaVecSum, sentences):
    bestSim = 0
    for i, sentence in enumerate(sentences):
        for j in xrange(i+1, len(sentences)):
            sentWordCombo = sentence + sentences[j] 
            if len(sentWordCombo) == 0:
                continue
            sentVecSum = getWordVecSum(sentWordCombo)
            if numpy.any(sentVecSum):
                sentVecSum = normalize(sentVecSum)
                bestSim = max(bestSim, getCosSim(qaVecSum, sentVecSum))
    return bestSim



def getWordVecMult(parsedWords):
    multArray = numpy.ones_like(parsedWords[0]['vector'])
    for token in parsedWords:
        if not numpy.any(token['vector']):
            continue 
        multArray = numpy.multiply(multArray, token['vector'])
    return multArray


def wordVecMultSimilarity(data):
    qParsedWords = data['question'].parsedText
    aParsedWords = data['question'].parsedAnswers[data['proposedAnswerIndex']]
    qaCombinedWords = qParsedWords + aParsedWords 
    qaVecMult = normalize(getWordVecMult(qaCombinedWords))
    bestSim = 0
    for sentence in getSentences(data['parsedText']):
        curSentVecMult = normalize(getWordVecMult(sentence))
        bestSim = max(bestSim, getCosSim(qaVecMult, curSentVecMult))
    return bestSim


def qaWindowVecSumSimilarity(data):
    windowSize = 6
    qParsedWords = data['question'].parsedText
    aParsedWords = data['question'].parsedAnswers[data['proposedAnswerIndex']]
    qaCombinedWords = qParsedWords + aParsedWords 
    qaVecSum = normalize(getWordVecSum(qaCombinedWords))
    parsedStory = data['parsedText']
    bestSim = 0
    for i in xrange(len(parsedStory) - windowSize):
        window = parsedStory[i:i + windowSize]
        curWindowVecSum = getWordVecSum(window)
        if numpy.any(curWindowVecSum):
            curWindowVecSum = normalize(curWindowVecSum)
            bestSim = max(bestSim, getCosSim(qaVecSum, curWindowVecSum))
    return bestSim
