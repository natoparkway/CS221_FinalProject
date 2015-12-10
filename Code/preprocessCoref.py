import os
import xml.etree.ElementTree
from DataClasses import *

def main():
    os.system("rm -rf storyTexts")
    os.system("mkdir storyTexts")
    if not os.path.exists("./storyTexts/filelist"):
        open("./storyTexts/filelist", 'w').close()
    for dataset in ["mc160.dev", "mc160.train", "mc160.test", "mc500.dev", "mc500.train", "mc500.train", "mc500.test"]:
        extractStoryTextsToFolder(dataset)
        # run coref here
        #parseXML()



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
            filelist.flush()
            os.fsync(filelist.fileno())


def parseXML():
    for fn in os.listdir('./corefOutput'):
        if os.path.isfile(fn):
            storyIndex = fn[:-4]
            storyXML = xml.etree.ElementTree.parse(os.path(fn)).getroot()
            print storyXML
                
if __name__ == "__main__":
    main()
