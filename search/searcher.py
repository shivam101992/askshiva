from pymongo import MongoClient
#from htmlParser import htmlParser
import sys
from pprint import pprint
from sets import Set
sys.path.append("/Users/vinusebastian/uci/quarter2/IR/project/askshiva/indexer")
#pprint(sys.path)
from MongoDbClient import MongoDbClient
from RedisClient import RedisClient
from collections import defaultdict
import json
import operator
import nltk
import time



class Searcher:
	def __init__(self):
		self.dbClient = MongoDbClient()
		self.redisClient = RedisClient()
		with open('/Users/vinusebastian/uci/quarter2/IR/project/WEBPAGES_RAW/bookkeeping.json') as json_data:
			self.bookKeeper = json.load(json_data)
   		self.stopWords = []
   		self.documentFrequencyThreshold = 1000

	def constructQuery(self, queryTerm):
		query = {"key" : queryTerm}
		return query

	def posTag(self, queryTerms):
		tagged = nltk.pos_tag(queryTerms)
		print tagged
		filteredQuery = []
		for tag in tagged:
			if tag[1] not in ["CC" , "DT" , "EX", "SYM", "WP", "WRB", "IN", "RB", "MD", "PRP$", "PRP"]:
				filteredQuery.append(tag[0])
		print filteredQuery

		return filteredQuery

	def orderUnigrams(self, queryTerms):
		# return queryTerms
		unigramTokens = []
		documentFrequencies = self.getDocumentFrequency(queryTerms)
		return sorted(documentFrequencies, key=documentFrequencies.get)

	def orderBigrams(self, queryTerms):
		# return queryTerms
		bigramTokens = []
		for i in range(1 ,len(queryTerms)):
			bigramTokens.append(queryTerms[i - 1] + " " + queryTerms[i])

		documentFrequencies = self.getDocumentFrequency(bigramTokens)

		return sorted(documentFrequencies, key=documentFrequencies.get)


	def collectResults(self, tokens, ngram, postingsMatch, totalLength):
		for token in tokens:
			databaseQuery = self.constructQuery(token)
			postings = self.dbClient.getResults(databaseQuery, ngram)
			if postings:
				postingsMatch[token] = postings["value"]
				totalLength += len(postings["value"])
			if totalLength > 1000:
				break
		return postingsMatch, totalLength

	def getPostings(self, query):
		postingsMatch = {}
		length = 0
		queryTerms = query.lower().split()
		queryTerms = self.posTag(queryTerms)[0:10]
		if (len(queryTerms) > 1):
			bigrams = self.orderBigrams(queryTerms)
			postingsMatch, length = self.collectResults(bigrams, "Bigram", postingsMatch, length)
			if length > 30:
				return postingsMatch
		unigrams = self.orderUnigrams(queryTerms)
		postingsMatch, length = self.collectResults(unigrams, "postingsList", postingsMatch, length)
		return postingsMatch

	def scoreDocuments(self, postings):
		documents = defaultdict(dict)
		documentScore = defaultdict(float)
		for key, values in postings.iteritems():
			for value in values:
				if "score" in documents[value["documentId"]]:
					documents[value["documentId"]]["score"] +=    float(value["tf-idf"]) + 10 * float(value["importance"])
				else:
					documents[value["documentId"]]["score"] =  float(value["tf-idf"]) + 10 *  float(value["importance"])
				if "metaData" in documents[value["documentId"]]:
					documents[value["documentId"]]["metaData"].append(value["metaData"])
				else:
					documents[value["documentId"]]["metaData"] = [value["metaData"]]
		return documents

	def dressResults(self, finalResults):
		final = []
		# millis = int(round(time.time() * 1000))
		# print "6:" +str(millis)
		for documentId, metaData  in finalResults:
			key = '/'.join(documentId.split(":"))
			url = self.bookKeeper[key]
			document = self.dbClient.getResults({"key" : documentId}, "textDocuments")
			textData = ""
			if document:
				for tag,positions in metaData["metaData"][0].iteritems():
					for position in positions:
							textData += " ".join(document["value"][tag].split()[position - 10 : position + 10]) + " ... "
				final.append({"url" : url, "text" : textData[0:200], "title" : document["value"].get("title", "")[0:200]})
				# final.append(url)
		# millis = int(round(time.time() * 1000))
		# print "7:" +str(millis)
		return final


	def search(self, query):
		# millis = int(round(time.time() * 1000))
		# print "1:" + str(millis) 
		postings = self.getPostings(query)
		# millis = int(round(time.time() * 1000))
		# print "2:" +str(millis)
		scoredDocuments = self.scoreDocuments(postings)
		# millis = int(round(time.time() * 1000))
		# print "3:" + str(millis)
		results = {}
		for documentId, document in scoredDocuments.iteritems():
			try :
				key = '/'.join(documentId.split(":"))
				scoredDocuments[documentId]["documentId"] = self.bookKeeper[key]
			except:
				continue
		# millis = int(round(time.time() * 1000))
		# print "4:" +str(millis)
		results = sorted(scoredDocuments.items(), key = self.keyfunc)[0:20]
		# millis = int(round(time.time() * 1000))
		# print "5:" +str(millis)
		count = len(scoredDocuments)
		return self.dressResults(results), count


	def keyfunc(self, tup):
		key, d = tup
		return -1 * d["score"]

	def getDocumentFrequency(self, tokens):
		query = tokens
		documentFrequencies = self.redisClient.multiget(tokens)
		return documentFrequencies

if __name__ == "__main__":
	query = "pillow indexer"
	searcher = Searcher()
	stuff = searcher.getPostings(query)
	searcher.scoreDocuments(stuff)
	
