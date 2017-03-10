import MongoDbClient
from htmlParser import htmlParser
from MongoDbClient import MongoDbClient
from RedisClient import RedisClient
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
		self.redisClient = RedisClient()

	# def getContentFromFolders(self):
	# 	metaData = []
	# 	termDocuments = []
	# 	wordMap = {}

	# 	for folder in self.folders[self.lowerBound: self.upperBound]:
	# 		folderName = folder.split('/')[-1]
	# 		files = glob.glob(folder + "/*")
	# 		for file in files:
	# 			fileName = file.split('/')[-1]
	# 			fileIdentifier = folderName + ':' + fileName
	# 			with open(file, 'r') as f:
	# 				parsedContent = self.htmlParser.parseHTML(f)
	# 				tokenizedContent = self.htmlParser.updateTokenLibrary(parsedContent)
	# 				for word, document in tokenizedContent.iteritems():
	# 					if word in wordMap:
	# 						wordMap[word].append(fileIdentifier)
	# 					else:
	# 						wordMap[word] = [fileIdentifier]
	# 					document = {"key" : word + ':' +  fileIdentifier, "value" : document}
	# 					metaData.append(document)
	# 		print folder
	# 	return wordMap, metaData

	# def addTermDocuments(self, wordMap):
	# 	termDocuments = []
	# 	for word, listOfDocuments in wordMap.iteritems():
	# 		document = {"key" : word, "value" : listOfDocuments}
	# 		termDocuments.append(document)
	# 	self.dbClient.insertRows(termDocuments, "termDocuments")
	# 	# self.dbClient.insertRows(documents, "metaData")

	# def addMetaData(self, wordMap, metaData):
	# 	d = DocumentRank()
	# 	metaData = d.rankDocuments(wordMap, metaData)
	# 	self.dbClient.insertRows(metaData, "metaData")

	###combined postings
	def createDocument(self, fileId, metaData):
		return {"documentId" :  fileId,
				"metaData" : metaData
		}

	def getContentFromFoldersCombined(self):
		metaData = []
		termDocuments = []
		wordMap = {}
		self.bigDictionary = {}

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
						json = self.createDocument(fileIdentifier, document)
						if word in self.bigDictionary:
							
							self.bigDictionary[word].append(json)
						else:
							self.bigDictionary[word] = [json]
			print folder


	def addDocuments(self, bigDictionary, collectionName = "postingsList"):
		documents = []
		# print bigDictionary
		for word, metaDataList in bigDictionary.iteritems():
			document = {"key" : word, "value" : metaDataList}
			documents.append(document)
		self.redisClient.insertRows(documents, collectionName)	



	def buildBigramDictionary(self):
		bigBigramDictionary = {}

		for folder in self.folders[self.lowerBound: self.upperBound]:
			folderName = folder.split('/')[-1]
			files = glob.glob(folder + "/*")
			for file in files:
				fileName = file.split('/')[-1]
				fileIdentifier = folderName + ':' + fileName
				with open(file, 'r') as f:
					parsedContent = self.htmlParser.parseHTMLLists(f)
					tokenizedContent = self.htmlParser.updateBigramLibrary(parsedContent)
					for word, document in tokenizedContent.iteritems():
						json = self.createDocument(fileIdentifier, document)
						if word in bigBigramDictionary:
							bigBigramDictionary[word].append(json)
						else:
							bigBigramDictionary[word] = [json]
			print folder

		return bigBigramDictionary


if __name__ == "__main__":
	folder = "*"
	if len(sys.argv) > 1:
		folderLowerBound = int(sys.argv[1])
		folderUpperBound = int(sys.argv[2])
	indexer = bulkIndexer(folderLowerBound, folderUpperBound)
	#wordMap, metaData = indexer.getContentFromFolders()

	###ORIGINAL
	indexer.getContentFromFoldersCombined()
	d = DocumentRank()
	bigDictionary = d.rankDocumentsCombined(indexer.bigDictionary)
	indexer.addDocuments(bigDictionary)
	###ORIGINAL

	####NEW
	# d = DocumentRank()

	# bigDictionary = indexer.buildBigramDictionary()
	# bigDictionary = d.rankDocumentsCombined(bigDictionary)
	# indexer.addDocuments(bigDictionary, "Bigram")
	####NEW

	# print "Got Data"
	# indexer.addTermDocuments(wordMap)
	# print "Added Term Documents"
	# indexer.addMetaData(wordMap, metaData)
	# print "Added MetaData"


