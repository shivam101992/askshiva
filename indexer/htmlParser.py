import sys,re, time, operator
from bs4 import BeautifulSoup, Comment
from tidylib import tidy_document
import json
from urlparse import urlparse, parse_qs
import re, os
import sys
class htmlParser:
	def __init__(self):
		with open('/Users/vinusebastian/uci/quarter2/IR/project/WEBPAGES_RAW/bookkeeping.json') as json_data:
			self.bookKeeper = json.load(json_data)
			self.urls = self.bookKeeper.values()
			self.keys = self.bookKeeper.keys()
			self.anchorTagInformation = {}
			self.graph = [[0] * 38000] * 38000

	def read_tokens(self, line):
		l = line.split()
		result = []
		for i in range(len(l)):
			l[i] = l[i].replace(",", "")
			l[i] = l[i].replace(".", "")
			if re.match('^[\w-]+$', l[i]):
				result.append((l[i].lower(), i))

		return result


	def updateTokenLibrary(self, data):
		dict1 = {}
		tokenLibrary = {}
		for documentTag, tagContents in data.items():
			for token,position in self.read_tokens(tagContents):
				if token in tokenLibrary:
					if documentTag in tokenLibrary[token]:
						tokenLibrary[token][documentTag].append(position)
					else:
						tokenLibrary[token][documentTag] = [position]
				else:
					tokenLibrary[token] = {}
					tokenLibrary[token][documentTag] = [position]

		return tokenLibrary

	def updateBigramLibrary(self, data):
		bigramLibrary = {}
		for documentTag, tagContents in data.items():
			tokenPositionList = self.read_tokens(tagContents)
			for i in range(1, len(tokenPositionList)):
				bigramToken =  tokenPositionList[i - 1][0]+ " " + tokenPositionList[i][0]
				# print bigramToken
				position = tokenPositionList[i - 1][1]
				if bigramToken in bigramLibrary:
					if documentTag in bigramLibrary[bigramToken]:
						bigramLibrary[bigramToken][documentTag].append(position)
					else:
						bigramLibrary[bigramToken][documentTag] = [position]
				else:
					bigramLibrary[bigramToken] = {}
					bigramLibrary[bigramToken][documentTag] = [position]

		return bigramLibrary

	def parseHTMLLists(self, file, fileIdentifier):
		fileIdentifier = "/".join(fileIdentifier.split(":"))
		html = file.read()
		data = {}
		###Removing comments
		parsed_html = BeautifulSoup(html, "lxml")
		# comments = parsed_html.findAll(text=lambda text:isinstance(text, Comment))
		# [comment.extract() for comment in comments]
		# parsed_html = BeautifulSoup(str(parsed_html), "lxml")

		for tag in ["title", "h1", "h2", "h3", "h4", "h5", "h6", "p", "a"]:
			if parsed_html.find(tag):
				tagTexts = parsed_html.find_all(tag)
				for tagText in tagTexts:
					if tag in data:
						data[tag] += " " + tagText.text
					else:
						data[tag] = tagText.text
		# if parsed_html.find("a"):
		# 	anchors = parsed_html.findAll("a")
		# 	if anchors:
		# 		self.addToPageRankGraph(anchors, fileIdentifier)
			# for anchor in anchors:
			# 	if anchor.text and anchor.text.strip() != "":
			# 		if not self.is_valid(anchor["href"]):
			# 			if self.bookKeeper[fileIdentifier] + anchor["href"] in self.urls:
			# 				self.addAnchorTag(self.bookKeeper[fileIdentifier] + anchor["href"], anchor.text)

			# 		else:
			# 			if anchor["href"] in self.urls:
			# 				self.addAnchorTag(anchor["href"], anchor.text)
		return data

	# def addToPageRankGraph(self, anchorTags, fileIdentifier):
	# 	for anchor in anchorTags:
	# 		# print type(anchor["href"])
	# 		# if "href" in anchor:
	# 		url = ""
	# 		try:
	# 			if (anchor["href"][-1]) == "/":
	# 				url = anchor["href"][0:-1]
	# 		except Exception:
	# 			continue
	# 		print url
	# 		if url in self.urls:
	# 			print "yes"
	# 			sys.exit()
	# 			self.addNode(self.keys.index(fileIdentifier), self.urls.index(url))
	# 		elif self.bookKeeper[fileIdentifier] + url in self.urls:
	# 			self.addNode(self.keys.index(fileIdentifier), self.urls.index(self.bookKeeper[fileIdentifier] + url))

	# def addNode(self, source, destination):
	# 	self.graph[source][destination] = 1



	# def addAnchorTag(key, value):
	# 	if key in self.anchorTagInformation:
	# 		self.anchorTagInformation[key] += " " + value 
	# 	else:
	# 		self.anchorTagInformation[key] = value

	# def is_valid(self, url):
	# 	parsed = urlparse(url)
	# 	if parsed:
	# 		try:
	# 		    return ".ics.uci.edu" in parsed.hostname \
	# 		        and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
	# 		        + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
	# 		        + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
	# 		        + "|thmx|mso|arff|rtf|jar|csv"\
	# 		        + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
	# 		except TypeError as e:
	# 		    return False
	# 	return False


if __name__ == "__main__":
	f1 = sys.argv[1]
	htmlParser = htmlParser()
	for filename in [f1]:
		with open(filename) as f:
			data = htmlParser.parseHTMLLists(f, "0:115")
			# bigramLibrary =  htmlParser.updateBigramLibrary(data)
	# for k, v in bigramLibrary.iteritems():
	# 	print k,v
