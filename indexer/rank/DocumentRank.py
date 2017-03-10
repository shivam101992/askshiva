import math
class DocumentRank:
	def __init__(self):
		self.N = 37497
		self.limit = 1000

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


	def rankDocumentsCombined(self, bigDictionary):
		for word, jsonList in bigDictionary.iteritems():
			df = len(jsonList)
			tags = {"title" : 10, "h1" : 6, "h2" : 5, "h3" : 4, "h4" : 5, "h6" : 6} 

			for i in range(len(jsonList)):
				multiplicationFactor = 1
				json = jsonList[i]
				l = json["metaData"].values()
				print json
				for key, value in tags.iteritems():
					if key in json["metaData"]:
						multiplicationFactor *= value * len(json["metaData"][key])

				tf = len([item for sublist in l for item in sublist])
				bigDictionary[word][i]["tf-idf"] = (1 + math.log(int(tf))) * math.log(self.N / df) * multiplicationFactor

		return bigDictionary



