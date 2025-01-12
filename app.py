from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://rizwan.power-devs.com"]}})

def is_url_indexed(url):
    """Check if a URL is indexed by Google by performing a site search."""
    try:
        search_url = f"https://www.google.com/search?q=site:{url}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Check for results in the Google search page
            if "did not match any documents" in response.text.lower():
                return False
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking URL {url}: {e}")
        return False

@app.route('/check_indexation', methods=['POST'])
def check_indexation():
    data = request.json
    urls = data.get('urls', [])
    results = []

    for url in urls:
        indexed = is_url_indexed(url)
        results.append({"url": url, "indexed": indexed})

    return jsonify({"status": "success", "results": results})

if __name__ == '__main__':
    app.run(debug=True)
