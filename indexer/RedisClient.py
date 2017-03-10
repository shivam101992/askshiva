import redis
import json
class RedisClient:
	def __init__(self):
		self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

	def insertRows(self, jsonInputList, collectionName = "metaData"):
		for jsonInput in jsonInputList:
			self.r.set(jsonInput["key"], json.dumps(jsonInput["value"]))


	def getResults(self, query, collectionName):
		print query["key"]
		result = self.r.get(query["key"])
		if result:
			return json.loads(result)
		return []
