#!/usr/bin/env python3

from flask import Flask, request, jsonify

app = Flask(__name__)

# GET endpoint
@app.route('/get', methods=['GET'])
def get_endpoint():
    return jsonify({"message": "This is a GET response"})

# POST endpoint for StringOnly
@app.route('/post/string', methods=['POST'])
def post_string():
    data = request.get_json()
    return jsonify({"received": data})

# POST endpoint for IntString
@app.route('/post/int_string', methods=['POST'])
def post_int_string():
    data = request.get_json()
    return jsonify({"received": data})

# POST endpoint for Mixed
@app.route('/post/mixed', methods=['POST'])
def post_mixed():
    data = request.get_json()
    return jsonify({"received": data})

# PUT endpoint for StringOnly
@app.route('/put/string', methods=['PUT'])
def put_string():
    data = request.get_json()
    return jsonify({"updated": data})

# PUT endpoint for IntString
@app.route('/put/int_string', methods=['PUT'])
def put_int_string():
    data = request.get_json()
    return jsonify({"updated": data})

# PUT endpoint for Mixed
@app.route('/put/mixed', methods=['PUT'])
def put_mixed():
    data = request.get_json()
    return jsonify({"updated": data})

if __name__ == '__main__':
    app.run(port=5000)
