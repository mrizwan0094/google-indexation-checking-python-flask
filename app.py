from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://rizwan.power-devs.com"]}})

@app.route('/check_indexation', methods=['POST'])
def check_indexation():
    data = request.json
    urls = data.get('urls', [])
    results = []

    for url in urls:
        # Mock indexation check - Replace this with actual logic.
        # For simplicity, we simulate "indexed" or "not indexed" randomly.
        response = {"url": url, "indexed": True}  # Replace with real indexation API logic
        results.append(response)

    return jsonify({"status": "success", "results": results})

if __name__ == '__main__':
    app.run(debug=True)
