from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import time

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model to accept URL data
class URLRequest(BaseModel):
    urls: list[str]

def check_index_status(url):
    """
    Check if a URL is indexed by searching it on Google.
    """
    search_url = f"https://www.google.com/search?q=site:{url}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Look for results in the search result page
        if "did not match any documents" in soup.text:
            return {"url": url, "status": "Not Indexed"}
        else:
            return {"url": url, "status": "Indexed"}
    else:
        return {"url": url, "status": f"Error: HTTP {response.status_code}"}

@app.post("/check-index-status")
async def check_urls(data: URLRequest):
    """
    Endpoint to check index status of multiple URLs.
    """
    results = []
    for url in data.urls:
        try:
            status = check_index_status(url)
            results.append(status)
            time.sleep(2)  # Be polite and avoid triggering Google's rate limits
        except Exception as e:
            results.append({"url": url, "status": f"Error: {str(e)}"})
    return {"results": results}
