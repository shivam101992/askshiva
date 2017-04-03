import MongoDbClient
from htmlParser import htmlParser
from MongoDbClient import MongoDbClient
from RedisClient import RedisClient
import glob
import sys
from rank.DocumentRank import DocumentRank
import nltk
class bulkIndexer:
	def __init__(self, lowerBound, upperBound):
		self.bigDictionary = {}
		self.folders = glob.glob("/Users/vinusebastian/uci/quarter2/IR/project/WEBPAGES_RAW/*")
		self.htmlParser = htmlParser()
		self.lowerBound = lowerBound
		self.upperBound = upperBound

		self.dbClient = MongoDbClient()
		self.redisClient = RedisClient()
		self.documentLength = {}
		self.textDictionary = {}
		# self.f = open("documentFrequencyBigram.txt", "w")
	###combined postings
	def createDocument(self, fileId, metaData):
		return {"documentId" :  fileId,
				"metaData" : metaData
		}



	def buildUnigramDictionary(self):
		metaData = []
		termDocuments = []
		wordMap = {}
		bigDictionary = {}

		for folder in self.folders[self.lowerBound: self.upperBound]:
			folderName = folder.split('/')[-1]
			files = glob.glob(folder + "/*")
			for file in files:
				fileName = file.split('/')[-1]
				fileIdentifier = folderName + ':' + fileName
				with open(file, 'r') as f:
					parsedContent = self.htmlParser.parseHTMLLists(f, fileIdentifier)
					tokenizedContent = self.htmlParser.updateTokenLibrary(parsedContent)
					bigramContent = self.htmlParser.updateBigramLibrary(parsedContent)
					self.textDictionary[fileIdentifier] = parsedContent
					self.documentLength[fileIdentifier] = len(parsedContent)
					for word, document in tokenizedContent.iteritems():
						json = self.createDocument(fileIdentifier, document)
						if word in bigDictionary:
							bigDictionary[word].append(json)
						else:
							bigDictionary[word] = [json]
			print folder
		return bigDictionary


	def addDocuments(self, bigDictionary, collectionName = "postingsList"):
		documents = []
		for word, metaDataList in bigDictionary.iteritems():
			document = {"key" : word, "value" : metaDataList}
			documents.append(document)
		self.dbClient.insertRows(documents, collectionName)	


	def addTextDocuments(self):
		documents = []
		for documentId, json in self.textDictionary.iteritems():
			document = {"key" : documentId, "value" : json}
			documents.append(document)
		self.dbClient.insertRow(documents, "textDocuments")	

	def buildBigramDictionary(self):
		bigBigramDictionary = {}
		self.textDictionary = {}
		for folder in self.folders[self.lowerBound: self.upperBound]:
			folderName = folder.split('/')[-1]
			files = glob.glob(folder + "/*")
			for file in files:
				fileName = file.split('/')[-1]
				fileIdentifier = folderName + ':' + fileName
				with open(file, 'r') as f:
					parsedContent = self.htmlParser.parseHTMLLists(f, fileIdentifier)
					tokenizedContent = self.htmlParser.updateBigramLibrary(parsedContent)
					self.textDictionary[fileIdentifier] = parsedContent
					for word, document in tokenizedContent.iteritems():
						json = self.createDocument(fileIdentifier, document)
						if word in bigBigramDictionary:
							bigBigramDictionary[word].append(json)
						else:
							bigBigramDictionary[word] = [json]
			print folder

		return bigBigramDictionary


	def addDocumentFrequenciesRedis(self):
		self.unigramCount = self.writeDocumentFrequency("documentFrequency.txt")
   		self.bigramCount = self.writeDocumentFrequency("documentFrequencyBigram.txt")
		

	def writeDocumentFrequency(self, filePath):
		f = open(filePath)
		documents = []
		for line in f:
			token, count = line.split(",")
			count  = int(count)
			document = {"key" : token, "value" : count}
			documents.append(document)
			print document
		self.redisClient.insertRows(documents)
		


if __name__ == "__main__":
	folder = "*"
	if len(sys.argv) > 1:
		folderLowerBound = int(sys.argv[1])
		folderUpperBound = int(sys.argv[2])
	indexer = bulkIndexer(folderLowerBound, folderUpperBound)
	# #wordMap, metaData = indexer.getContentFromFolders()

	# ###ORIGINAL
	# unigramDictionary = indexer.buildUnigramDictionary()
	d = DocumentRank()
	# bigDictionary = d.rankDocumentsCombined(unigramDictionary, indexer.documentLength)
	# # # "Writing Document Frequencies to file"

	# # # for key, value in d.df.iteritems():
	# # # 	indexer.f.write(key + "," + str(value) + "\n")
	# # # print "Adding Unigram"
	# indexer.addDocuments(bigDictionary)
	# # # print "Adding Documents"
	# # # # indexer.addTextDocuments()
	# # # print "Building Bigram"
	bigDictionary = indexer.buildBigramDictionary()
	# # # print "Rankgin"
	bigDictionary = d.rankDocumentsCombined(bigDictionary, indexer.documentLength)
	indexer.addDocuments(bigDictionary, "Bigram")
	# for key, value in d.dfList.iteritems():
		# indexer.f.write(key + "," + str(value) + "\n")
	# indexer.addTextDocuments()
	###ORIGINAL

	####Add Document Frequencies to redis
	# indexer.addDocumentFrequenciesRedis()



