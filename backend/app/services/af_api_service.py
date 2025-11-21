import requests
import math
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
        """Search jobs with offset/limit and return pagination metadata.

        Returns a dict with:
        - hits: list of job ads
        - total: integer total number of matches
        - pagination: object with page info (page, total_pages, has_next, etc.)
        """
        url = f"{self.base_url}/search"
        params = {
            "q": query,
            "offset": max(0, int(offset or 0)),
            "limit": max(1, int(limit or 10)),
        }
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json() or {}
            hits = data.get("hits", []) or []
            # AF API typically returns total as {"value": <int>}
            total_val = 0
            total_obj = data.get("total")
            if isinstance(total_obj, dict):
                total_val = int(total_obj.get("value", 0) or 0)
            elif isinstance(total_obj, (int, float)):
                total_val = int(total_obj)

            limit_val = params["limit"]
            offset_val = params["offset"]
            page = (offset_val // limit_val) + 1 if limit_val > 0 else 1
            total_pages = max(1, math.ceil(total_val / limit_val)) if limit_val > 0 else 1
            has_next = (offset_val + limit_val) < total_val
            has_prev = offset_val > 0
            next_offset = (offset_val + limit_val) if has_next else None
            prev_offset = (offset_val - limit_val) if has_prev else None

            return {
                "hits": hits,
                "total": total_val,
                "pagination": {
                    "offset": offset_val,
                    "limit": limit_val,
                    "page": page,
                    "total_pages": total_pages,
                    "has_next": has_next,
                    "has_prev": has_prev,
                    "next_offset": next_offset,
                    "prev_offset": max(0, prev_offset) if prev_offset is not None else None,
                    "next_page": (page + 1) if has_next else None,
                    "prev_page": (page - 1) if has_prev else None,
                },
            }
        except requests.RequestException as e:
            print(f"Error searching jobs: {e}")
            return {"hits": [], "total": 0, "pagination": {"offset": offset, "limit": limit, "page": 1, "total_pages": 1, "has_next": False, "has_prev": False, "next_offset": None, "prev_offset": None, "next_page": None, "prev_page": None}}

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
