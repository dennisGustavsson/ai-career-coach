import requests
from typing import Dict, Any, List, Optional
from app.core.config import settings

class AFJobSearchService:
    def __init__(self):
        self.base_url = settings.AF_API_BASE_URL
        self.headers = {
            "Accept": "application/json",
            # "api-key": settings.AF_API_KEY # If needed in future, currently open
        }

    def search_jobs(self, query: str, offset: int = 0, limit: int = 10) -> Dict[str, Any]:
        url = f"{self.base_url}/search"
        params = {
            "q": query,
            "offset": offset,
            "limit": limit
        }
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error searching jobs: {e}")
            return {"hits": [], "total": {"value": 0}}

    def get_job_details(self, ad_id: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/ad/{ad_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error getting job details: {e}")
            return None

af_service = AFJobSearchService()
