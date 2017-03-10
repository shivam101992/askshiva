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



class Searcher:
	def __init__(self):
		self.dbClient = MongoDbClient()
		self.redisClient = RedisClient()
		with open('/Users/vinusebastian/uci/quarter2/IR/project/askshiva/WEBPAGES_RAW/bookkeeping.json') as json_data:
			self.bookKeeper = json.load(json_data)
   		


	def constructQuery(self, queryTerm):
		query = {"key" : queryTerm}
		return query

	def getPostings(self, query):
		postingsMatch = {}
		queryTerms = query.lower().split()
		# if (len(queryTerms) > 1):
		# 	for i in range(1 ,len(queryTerms)):
		# 		queryTerm = queryTerms[i - 1] + " " + queryTerms[i]
		# 		databaseQuery = self.constructQuery(queryTerm)
		# 		postings = self.dbClient.getResults(databaseQuery, "Bigram")
		# 		if postings:
		# 			postingsMatch[queryTerm] = postings["value"]
			
		# 	return postingsMatch
		print "HEER"
		for queryTerm in queryTerms:
			print queryTerm
			databaseQuery = self.constructQuery(queryTerm)
			#postings = self.dbClient.getResults(databaseQuery, "postingsList")
			postings = self.redisClient.getResults(databaseQuery, "postingsList")
			if postings:
				postingsMatch[queryTerm] = postings
		
		return postingsMatch
	

	# def mergePostings(self, postingsMatch):
	# 	results = Set()
	# 	print postingsMatch
	# 	for queryTerm, postings in postingsMatch.iteritems():
	# 		if results:
	# 			results = Set(postings)
	# 		else:
	# 			results = results.union(postings)
	# 	return list(results)

	# def rankResults(self, mergePostings):
	# 	for mergedPosting in mergedPostings:
	# 		self.dbClient.getResults

	# def search(self, query):
	# 	postings = self.getPostings(query)
	# 	mergedPostings =  self.mergePostings(postings)
	# 	urlList = []
	# 	for mergedPosting in mergedPostings:
	# 		key = '/'.join(mergedPosting.split(":"))
	# 		urlList.append(self.bookKeeper[key])

	# 	return urlList

	def scoreDocuments(self, postings):
		documentScore = defaultdict(float)
		for key, values in postings.iteritems():
			for value in values:
				documentScore[value["documentId"]] += float(value["tf-idf"])
		return documentScore

	def search(self, query):
		postings = self.getPostings(query)
		scoredDocuments = self.scoreDocuments(postings)
		results = {}
		for documentId, score in scoredDocuments.iteritems():
			key = '/'.join(documentId.split(":"))
			results[self.bookKeeper[key]] = score
		return sorted(results, key=results.get, reverse=True)[0:20]
		# return sorted(results.items(), key=operator.itemgetter(1), reverse=True)


if __name__ == "__main__":
	query = "pillow indexer"
	searcher = Searcher()
	# pp = pprint.PrettyPrinter(indent=4)
	stuff = searcher.getPostings(query)
	searcher.scoreDocuments(stuff)
	# print stuff
	# pp.print(stuff)
	
