from pymongo import MongoClient

class MongoDbClient:
	def __init__(self):
		client = MongoClient('localhost:27017')
		self.db = client.indexDatabase
		self.dbCombined = client.combined

	# def insertRow(self, jsonInput, collectionName = "metaData"):
	# 	self.dbCombined[collectionName].insert_one(jsonInput)

	def insertRows(self, jsonInputList, collectionName = "metaData"):
		bulk = self.dbCombined[collectionName].initialize_ordered_bulk_op()
		for jsonInput in jsonInputList:
			bulk.insert(jsonInput)
		bulk.execute()

	def findOne(self, collectionName, key, value):
		return self.dbCombined[collectionName].find_one({key: value})

	# def addDocumentNumber(self, jsonInputList, collectionName = "termDocuments"):
	# 	bulk = self.dbCombined[collectionName].initialize_ordered_bulk_op()
	# 	for jsonInput in jsonInputList:
	# 		keyString = "key"
	# 		keyValue = jsonInput[keyString]
	# 		documentIds = jsonInput["value"]
	# 		bulk.find({  keyString: keyValue}).upsert().update(
	#    	 		{ "$push": { "value": documentIds}}
	# 		)
	# 	bulk.execute()


	def getResults(self, query, collectionName):
		print query
		return self.dbCombined[collectionName].find_one(query)



# # document = {"word" : "artificial",  "documentList" : ["1", "5", "9"]}

# metaDataDocument = {"key" : "artificial1", 
# 					"title": ["1", "10", "5"],
# 					"h1": ["5", "67", "78"],
# 					"p" : ["10", "20", "34"]
# 				}

# addDocumentNumber("termDocuments", "word", "artificial", "1")

# addDocumentNumber("termDocuments", "word", "artificial", "10")
# insertRow(metaDataDocument, "metaData")