import sys,re, time, operator
from bs4 import BeautifulSoup
from tidylib import tidy_document


class htmlParser:
	def read_tokens(self, line):
		l = line.split()
		result = []
		for i in range(len(l)):
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


	def parseHTML(self, file):
		html = file.read()
		data = {}
		parsed_html = BeautifulSoup(html, "lxml")
		if parsed_html:
			if parsed_html.find('title') and parsed_html.find('title').text:
				titles = parsed_html.find_all('title')
				title_str=""
				for title in titles:
					title_str+=title.text + " "
				data["title"] = title_str
			
			if parsed_html.find('h1'):
				h1 = parsed_html.find_all('h1')
				h1_str=""
				for head1 in h1:
					h1_str+=head1.text + " "
				data["h1"] = h1_str

			if parsed_html.find('h2'):
				h2 = parsed_html.find_all('h2')
				h2_str=""
				for head2 in h2:
					h2_str+=head2.text + " "
				data["h2"] = h2_str	

			if parsed_html.find('h3'):
				h3 = parsed_html.find_all('h3')
				h3_str=""
				for head3 in h3:
					h3_str+=head3.text + " "
				data["h3"] = h3_str	

			if parsed_html.find('h4'):
				h4 = parsed_html.find_all('h4')
				h4_str=""
				for head4 in h4:
					h4_str+=head4.text+" "
				data["h4"] = h4_str	

			if parsed_html.find('h5'):
				h5 = parsed_html.find_all('h5')
				h5_str=" "
				for head5 in h5:
					h5_str+=head5.text + " "

				data["h5"] = h5_str	

			if parsed_html.find('h6'):
				h6 = parsed_html.find_all('h6')
				h6_str = " "
				for head6 in h6:
					h6_str+=head6.text + " "
				data["h6"] = h6_str	

			if parsed_html.find('p'):
				paras = parsed_html.find_all('p')
				p_str=""
				for para in paras:
					p_str += para.text + " "
				data["p"] = p_str	
			if parsed_html.find('a'):
				paras = parsed_html.find_all('a')
				p_str=""
				for para in paras:
					p_str += para.text + " "
				data["a"] = p_str		
		return data			

if __name__ == "__main__":
	f1 = sys.argv[1]
	htmlParser = htmlParser()
	for filename in [f1]:
		with open(filename) as f:
			data = htmlParser.parseHTML(f)
			
			parsed =  htmlParser.updateTokenLibrary(data)
			for key, value in parsed.iteritems():
				print value
