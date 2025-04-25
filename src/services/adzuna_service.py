import requests
from typing import Dict, List, Any, Optional
import logging
from config import ADZUNA_APP_ID, ADZUNA_API_KEY, ADZUNA_BASE_URL

logger = logging.getLogger(__name__)

class AdzunaService:
    """Service to interact with the Adzuna Jobs API."""
    
    def __init__(self, app_id: str = ADZUNA_APP_ID, api_key: str = ADZUNA_API_KEY):
        """Initialize the Adzuna service with API credentials."""
        self.app_id = app_id
        self.api_key = api_key
        self.base_url = ADZUNA_BASE_URL
        
        if not self.app_id or not self.api_key:
            raise ValueError("Adzuna API credentials not found. Please set ADZUNA_APP_ID and ADZUNA_API_KEY.")
    
    def search_jobs(self, 
                   country: str = "gb", 
                   keywords: Optional[List[str]] = None, 
                   location: Optional[str] = None, 
                   page: int = 1, 
                   results_per_page: int = 10) -> Dict[str, Any]:
        """
        Search for jobs using the Adzuna API.
        
        Args:
            country: Country code to search in (default: 'gb')
            keywords: List of keywords to search for
            location: Location to search in
            page: Page number for results pagination
            results_per_page: Number of results per page
            
        Returns:
            Dictionary containing job results
        """
        endpoint = f"{self.base_url}/{country}/search/{page}"
        
        params = {
            "app_id": self.app_id,
            "app_key": self.api_key,
            "results_per_page": results_per_page,
            "content-type": "application/json"
        }
        
        # Add query parameters if provided
        if keywords:
            params["what"] = " ".join(keywords)
        
        if location:
            params["where"] = location
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching jobs from Adzuna: {e}")
            return {"error": str(e), "results": []}
    
    def parse_job_results(self, response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse the response from Adzuna API to extract job details.
        
        Args:
            response_data: Raw API response data
            
        Returns:
            List of formatted job listings
        """
        job_listings = []
        
        if "results" not in response_data:
            logger.warning("No results found in Adzuna response")
            return job_listings
        
        for job in response_data["results"]:
            job_data = {
                "id": job.get("id"),
                "title": job.get("title"),
                "description": job.get("description", ""),
                "company": job.get("company", {}).get("display_name", "Unknown"),
                "location": job.get("location", {}).get("display_name", "Unknown"),
                "url": job.get("redirect_url"),
                "salary_min": job.get("salary_min", 0),
                "salary_max": job.get("salary_max", 0),
                "created": job.get("created"),
                "category": job.get("category", {}).get("label", "")
            }
            
            # Extract keywords/skills mentioned in the job description
            job_data["keywords"] = self._extract_keywords(job_data["description"])
            
            job_listings.append(job_data)
        
        return job_listings
    
    def _extract_keywords(self, description: str) -> List[str]:
        """
        Extract potential skills and keywords from job description.
        This is a simple implementation that could be enhanced with NLP techniques.
        
        Args:
            description: Job description text
            
        Returns:
            List of extracted keywords
        """
        # This is a placeholder. In a real implementation, 
        # you might use NLP techniques to extract relevant skills.
        # For now, we'll just clean and split the text
        words = description.lower().split()
        # Filter out common words, punctuation, etc.
        # This would be more sophisticated in a real implementation
        return list(set(words))