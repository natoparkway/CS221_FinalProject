import os
import xml.etree.ElementTree
from DataClasses import *

def main():
    for dataset in ["mc160.dev", "mc160.train", "mc160.test", "mc500.dev", "mc500.train", "mc500.train", "mc500.test"]:
        extractStoryTextsToFolder(dataset)
        # run coref here
        parseXML()



def extractStoryTextsToFolder(dataset):
    data = Dataset()
    data.appendData("../MCTest/" + dataset)
    os.system("rm -rf storyTexts")
    os.system("mkdir storyTexts")
    with open("./storyTexts/filelist", "w") as filelist:
        for story in data.stories:
            print story.storyID
            storyText = story.casedText
            filePath =  story.storyID
            filelist.write(filePath)
            filelist.write("\n")
            with open("./storyTexts/" + story.storyID, "w") as f:
                f.write(story.casedText)
                f.flush()
                os.fsync(f.fileno())    


def parseXML():
    for fn in os.listdir('./corefOutput'):
        if os.path.isfile(fn):
            storyIndex = fn[:-4]
            storyXML = xml.etree.ElementTree.parse(os.path(fn)).getroot()
            print storyXML
                
if __name__ == "__main__":
    main()
