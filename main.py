from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import time

app = FastAPI()

# Configure CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rizwan.power-devs.com"],  # Replace this with your actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

class URLRequest(BaseModel):
    urls: list[str]

# Your existing function to check URL indexing
def check_index_status(url):
    search_url = f"https://www.google.com/search?q=site:{url}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        if "did not match any documents" in soup.text:
            return {"url": url, "status": "Not Indexed"}
        else:
            return {"url": url, "status": "Indexed"}
    else:
        return {"url": url, "status": f"Error: HTTP {response.status_code}"}

@app.post("/check-index-status")
async def check_urls(data: URLRequest):
    results = []
    for url in data.urls:
        status = check_index_status(url)
        results.append(status)
        time.sleep(2)  # Avoid hitting Google too fast with requests
    return {"results": results}
