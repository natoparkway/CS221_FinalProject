import os
import xml.etree.ElementTree
from DataClasses import *

def main():
    os.system("rm -rf storyTexts")
    os.system("mkdir storyTexts")
    if not os.path.exists("./storyTexts/filelist"):
        open("./storyTexts/filelist", 'w').close()
    for dataset in ["mc160.dev", "mc160.train", "mc160.test", "mc500.dev", "mc500.train", "mc500.train", "mc500.test"]:
        #extractStoryTextsToFolder(dataset)
        # run coref here
        parseXMLS()



def extractStoryTextsToFolder(dataset):
    data = Dataset()
    data.appendData("../MCTest/" + dataset)
    with open("./storyTexts/filelist", "a") as filelist:
        for story in data.stories:
            print story.storyID
            filePrefix = "../../CS221_FinalProject/Code/storyTexts/"
            storyText = story.casedText
            filePath =  filePrefix + story.storyID
            filelist.write(filePath)
            filelist.write("\n")
            with open("./storyTexts/" + story.storyID, "w") as f:
                f.write(story.casedText)
                f.flush()
                os.fsync(f.fileno())
                f.close()
        filelist.close()


def parseXMLS():
    storyIdToCorefs = {}
    for fn in os.listdir('./corefOutput'):
        if os.path.isfile(fn):
            storyIndex = fn[:-4]
            storyTextFilename = "./storyTexts/" + storyIndex
            with open(storyTextFilename, "r") as storyTextFile:
                storyText = storyTextFile.readline()
                storyTextFile.close()
            storyXML = xml.etree.ElementTree.parse(os.path(fn)).getroot()
            fn.close()
            sentencesXML = storyXML.findall("sentences")
            corefXML = storyXML.find("document").find("coreference")
            clusters = corefXML.findall("coreference")
            for cluster in clusters:
                repMention = cluster.find("mention[@representative='true']")
                repMentionString = repMention.find("text").text
                repMentionString = filterSuffixes(repMentionString)
                mentions = cluster.findall("mention")
                for mention in mentions:
                    mentionSentenceID = mention.find("sentence").text()
                    firstTokenID = mention.find("start").text()
                    lastTokenID = mention.find("end").text()
                    if lastTokenID - firstTokenID == 1:
                        beginOffset, _ = getTokenBoundariesFromSentence(sentencesXML, mentionSentenceID, firstTokenID)
                        _, endOffset = getTokenBoundariesFromSentence(sentencesXML, mentionSentenceID, endTokenID)
                        storyText = storyText[:beginOffset] + " " + repMentionString + " " + storyText[endOffset:]
            with open("./corefdStories/" + storyIndex) as outfile:
                outfile.write(storyText)
                outfile.flush()
                os.fsync(outfile.fileno())
                outfile.close()
                

def filterSuffixes(string):
    tokens = string.split()
    if tokens[-1] == "'s":
        return " ".join(tokens[:-1])
    else:
        return string


def getTokenBoundariesFromSentence(sentencesXML, sentenceID, tokenID):
    sentenceXML = sentencesXML.find("sentence[@id='" + sentenceID + "']")
    tokenXML = sentenceXML.find("tokens").find("token[@id='" + tokenID + "']")
    beginOffset = int(tokenXML.find("CharacterOffsetBegin").text())
    endOffset = int(tokenXML.find("CharacterOffsetEnd").text())
    return beginOffset, endOffset



         

            

if __name__ == "__main__":
    main()
