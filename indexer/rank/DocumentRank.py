import math
class DocumentRank:
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



