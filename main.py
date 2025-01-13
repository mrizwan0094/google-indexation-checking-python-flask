from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from queue import Queue
from threading import Thread
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS using Flask-CORS
CORS(app, resources={r"/check-index-status": {"origins": ["https://rizwan.power-devs.com"]}})

def check_index_status(url):
    """
    Check if a URL is indexed by searching it on Google.
    """
    search_url = f"https://www.google.com/search?q=site:{url}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for results in the search result page
            if "did not match any documents" in soup.text:
                return {"url": url, "status": "Not Indexed"}
            else:
                return {"url": url, "status": "Indexed"}
        else:
            return {"url": url, "status": f"Error: HTTP {response.status_code}"}
    except Exception as e:
        return {"url": url, "status": f"Error: {str(e)}"}

def worker(queue, results):
    while not queue.empty():
        url = queue.get()
        results.append(check_index_status(url))
        queue.task_done()

@app.route('/check-index-status', methods=['POST', 'OPTIONS'])
def check_status():
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers['Access-Control-Allow-Origin'] = 'https://rizwan.power-devs.com'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 200

    # Handle POST request
    data = request.json
    urls = data.get('urls', [])

    if not urls or not isinstance(urls, list):
        return jsonify({"error": "Invalid input. Please provide a list of URLs."}), 400

    queue = Queue()
    results = []

    # Add URLs to the queue
    for url in urls:
        queue.put(url)

    # Create threads to process the queue
    threads = []
    for _ in range(min(5, len(urls))):  # Limit to 5 concurrent threads
        thread = Thread(target=worker, args=(queue, results))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
