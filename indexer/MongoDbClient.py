from pymongo import MongoClient

class MongoDbClient:
	def __init__(self):
		client = MongoClient('localhost:27017')
		self.db = client.indexDatabase
		self.dbCombined = client.combined

	# def insertRow(self, jsonInput, collectionName = "metaData"):
	# 	self.dbCombined[collectionName].insert_one(jsonInput)

	def insertRows(self, jsonInputList, collectionName = "metaData"):
		# return 
		bulk = self.dbCombined[collectionName].initialize_ordered_bulk_op()
		for jsonInput in jsonInputList:
			bulk.insert(jsonInput)
		bulk.execute()

	def insertRow(self, jsonInputList, collectionName = "metaData"):
		# return
		i = 0
		for jsonInput in jsonInputList:
			print i
			i += 1
			try:
				self.dbCombined[collectionName].insert_one(jsonInput)
			except:
				print "FAILLLLLL"


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
		# print query

		# print query
		result = self.dbCombined[collectionName].find_one(query)
		return result


	def getDocumentsByIds(self, documentIds, collectionName = "textDocuments"):
		return self.dbCombined[collectionName].find({"key" : {"$in" : documentIds}})
