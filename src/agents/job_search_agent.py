from crewai import Agent
from typing import Dict, List, Any
from services.adzuna_service import AdzunaService
from config import LLM_MODEL, DEFAULT_NUM_RESULTS

class JobSearchAgent:
    """
    Agent responsible for searching job listings using the Adzuna API.
    """
    
    def __init__(self, llm_model: str = LLM_MODEL):
        """
        Initialize the Job Search Agent.
        
        Args:
            llm_model: Language model to use for the agent
        """
        self.adzuna_service = AdzunaService()
        self.agent = self._create_agent(llm_model)
    
    def _create_agent(self, llm_model: str) -> Agent:
        """
        Create the CrewAI agent.
        
        Args:
            llm_model: Language model to use
            
        Returns:
            CrewAI Agent instance
        """

        return Agent(
            role="Job Search Specialist",
            goal="Find the most relevant job listings based on location and keywords",
            backstory="""
            You are an experienced job search specialist with deep knowledge of various
            job markets and industries. Your expertise lies in finding the most relevant
            job opportunities that match specific criteria. You are meticulous in your
            search and ensure that the job listings you find are high-quality and relevant.
            """,
            verbose=True,
            allow_delegation=False,
            llm_model=llm_model
        )
    
    def search_jobs(self, keywords: List[str], location: str, 
                   country: str = "gb", results_per_page: int = DEFAULT_NUM_RESULTS) -> List[Dict[str, Any]]:
        """
        Search for jobs using the provided keywords and location.
        
        Args:
            keywords: List of job keywords to search for
            location: Location to search in
            country: Country code for the search
            results_per_page: Number of results to return
            
        Returns:
            List of job listings
        """
        # Use the Adzuna service to get raw job data
        job_response = self.adzuna_service.search_jobs(
            country=country,
            keywords=keywords,
            location=location,
            results_per_page=results_per_page
        )
        
        # Parse the results into a standardized format
        job_listings = self.adzuna_service.parse_job_results(job_response)
        
        return job_listings
    
    def get_agent(self) -> Agent:
        """
        Get the CrewAI agent instance.
        
        Returns:
            CrewAI Agent instance
        """
        return self.agent