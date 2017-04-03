import math
class DocumentRank:
	def __init__(self):
		self.N = 37497
		self.limit = 1000
		self.dfList = {}
	def rankDocuments(self, termDocumentMatrix, metaData):
		documentFrequency = {}
		for i in range(len(metaData)):

			word = metaData[i]["key"].split(':')[0]
			metaDataWord = metaData[i]["value"]
			tf = 0 
			for k,v in metaDataWord.iteritems():
				tf += len(v)
			metaData[i]["tf-idf"] = (1 + math.log(int(tf))) * math.log(1.0 / (int(len(termDocumentMatrix[word]))))
		return metaData


	def rankDocumentsCombined(self, bigDictionary, documentLength):
		for word, jsonList in bigDictionary.iteritems():
			df = len(jsonList)
			self.dfList[word] = df
			tags = {"title" : 100, "h1" : 6, "h2" : 5, "h3" : 4, "h4" : 3, "h6" : 2, "p" : 1} 
			for i in range(len(jsonList)):
				multiplicationFactor = 1
				json = jsonList[i]
				documentId = json["documentId"]
				l = json["metaData"].values()
				for key, value in tags.iteritems():
					if key in json["metaData"]:
						multiplicationFactor += value + len(json["metaData"][key])
				tf = len([item for sublist in l for item in sublist])
				try:
					bigDictionary[word][i]["tf-idf"] = (1 + math.log(int(tf))) * math.log(self.N / df) / documentLength[documentId]
				except:
					bigDictionary[word][i]["tf-idf"] = (1 + math.log(int(tf))) * math.log(self.N / df)
				bigDictionary[word][i]["importance"] =  multiplicationFactor
		return bigDictionary



