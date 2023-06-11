from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_data():
    # Handle GET request
    return jsonify({'message': 'GET request received'})

@app.route('/', methods=['POST'])
def post_data():
    # Handle POST request
    data = request.get_json()
    return jsonify({'message': 'POST request received', 'data': data})

if __name__ == '__main__':
    load_dotenv()
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)