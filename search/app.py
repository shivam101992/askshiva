#!flask/bin/python
from flask import Flask, jsonify, request
from flask_cors import CORS
from searcher import Searcher
from autocompleter import Autocompleter
app = Flask(__name__)
CORS(app)
@app.route('/search', methods=['GET'])

def get_search():
	query = request.args.get('query')
	searcher = Searcher()
	results, count =  searcher.search(query)
	return jsonify({"results" : results, "count" : count})
CORS(app)
@app.route('/autocomplete', methods=['GET'])

def get_autocomplete():
	query = request.args.get('query')
	autocompleter = Autocompleter()
	results =  autocompleter.autocomplete(query)
	formatted = []
	for result in results:
		document = { "value": result, "data": "AE" }
		formatted.append(document)

	return jsonify({"suggestions" : formatted})


if __name__ == '__main__':
    app.run(debug=True)