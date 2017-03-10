#!flask/bin/python
from flask import Flask, jsonify, request
from searcher import Searcher
app = Flask(__name__)

@app.route('/search', methods=['GET'])

def get_tasks():
	query = request.args.get('query')
	searcher = Searcher()
	results =  searcher.search(query)
	return jsonify({"results" : results})


if __name__ == '__main__':
    app.run(debug=True)