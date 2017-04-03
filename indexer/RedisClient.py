import redis
import json
class RedisClient:
	def __init__(self):
		self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

	def insertRows(self, jsonInputList, collectionName = "metaData"):
		for jsonInput in jsonInputList:
			# print jsonInput
			self.r.set(jsonInput["key"], json.dumps(jsonInput["value"]))


	def getResults(self, query):
		print query["key"]
		result = self.r.get(query["key"])
		if result:
			return json.loads(result)
		return []

	def multiget(self, tokens):
		if tokens:
			results = self.r.mget(tokens)
			if results:
				counts = []
				for result in results:
					if result:
						counts.append(int(result))
					else:
						counts.append(0)
				return dict(zip(tokens, counts))
		return {}
