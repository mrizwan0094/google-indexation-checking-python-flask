from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rizwan.power-devs.com"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_url_indexed(url: str) -> bool:
    """Check if a URL is indexed by Google by performing a site search."""
    try:
        search_url = f"https://www.google.com/search?q=site:{url}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            if "did not match any documents" in response.text.lower():
                return False
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking URL {url}: {e}")
        return False

@app.post("/check_indexation/")
async def check_indexation(urls: List[str]):
    """API endpoint to check indexation of multiple URLs."""
    if not urls:
        raise HTTPException(status_code=400, detail="No URLs provided.")

    results = []
    for url in urls:
        indexed = is_url_indexed(url)
        results.append({"url": url, "indexed": indexed})

    return {"status": "success", "results": results}
