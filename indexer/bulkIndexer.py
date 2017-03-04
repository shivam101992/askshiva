import MongoDbClient
from htmlParser import htmlParser
from MongoDbClient import MongoDbClient
import glob
import sys
from rank.DocumentRank import DocumentRank
class bulkIndexer:
	def __init__(self, lowerBound, upperBound):
		self.bigDictionary = {}
		self.folders = glob.glob("/Users/vinusebastian/uci/quarter2/IR/project/WEBPAGES_RAW/*")
		self.htmlParser = htmlParser()
		self.lowerBound = lowerBound
		self.upperBound = upperBound

		self.dbClient = MongoDbClient()

	def getContentFromFolders(self):
		metaData = []
		termDocuments = []
		wordMap = {}

		for folder in self.folders[self.lowerBound: self.upperBound]:
			folderName = folder.split('/')[-1]
			files = glob.glob(folder + "/*")
			for file in files:
				fileName = file.split('/')[-1]
				fileIdentifier = folderName + ':' + fileName
				with open(file, 'r') as f:
					parsedContent = self.htmlParser.parseHTML(f)
					tokenizedContent = self.htmlParser.updateTokenLibrary(parsedContent)
					for word, document in tokenizedContent.iteritems():
						if word in wordMap:
							wordMap[word].append(fileIdentifier)
						else:
							wordMap[word] = [fileIdentifier]
						document = {"key" : word + ':' +  fileIdentifier, "value" : document}
						metaData.append(document)
			print folder
		return wordMap, metaData

	def addTermDocuments(self, wordMap):
		termDocuments = []
		for word, listOfDocuments in wordMap.iteritems():
			document = {"key" : word, "value" : listOfDocuments}
			termDocuments.append(document)
		self.dbClient.insertRows(termDocuments, "termDocuments")
		# self.dbClient.insertRows(documents, "metaData")

	def addMetaData(self, wordMap, metaData):
		d = DocumentRank()
		metaData = d.rankDocuments(wordMap, metaData)
		self.dbClient.insertRows(metaData, "metaData")
					
				




if __name__ == "__main__":
	folder = "*"
	if len(sys.argv) > 1:
		folderLowerBound = int(sys.argv[1])
		folderUpperBound = int(sys.argv[2])
	indexer = bulkIndexer(folderLowerBound, folderUpperBound)
	wordMap, metaData = indexer.getContentFromFolders()
	print "Got Data"
	indexer.addTermDocuments(wordMap)
	print "Added Term Documents"
	indexer.addMetaData(wordMap, metaData)
	print "Added MetaData"


