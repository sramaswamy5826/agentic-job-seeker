from crewai import Agent
from langchain.tools import BaseTool
from typing import Dict, List, Any, Optional, Type
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from services.dynamodb_service import DynamoDBService
from config import LLM_MODEL, TOP_MATCHES

class JobMatchInput(BaseModel):
    """Input schema for the job matching tool."""
    job_listings: List[Dict[str, Any]] = Field(
        description="List of job listings to match against the resume"
    )
    resume_id: str = Field(
        description="ID of the resume to match against job listings"
    )

class JobMatchingTool(BaseTool):
    """Tool for matching job listings with a candidate's resume using LLM."""
    
    name = "job_matcher"
    description = "Match job listings with a candidate's resume based on skills, experience, and qualifications"
    args_schema: Type[BaseModel] = JobMatchInput

    # Define class attributes for the LLM and database service
    llm: Optional[ChatOpenAI] = None
    dynamodb_service: Optional[DynamoDBService] = None
    
    def __init__(self, llm) -> None:
        """
        Initialize the Job Matching Tool.
        
        Args:
            llm: Language model to use for matching
        """
        super().__init__()
        self.llm = llm
        self.dynamodb_service = DynamoDBService()
        
    def _run(self, job_listings: List[Dict[str, Any]], resume_id: str) -> List[Dict[str, Any]]:
        """
        Match job listings to a resume and calculate match scores using LLM.
        
        Args:
            job_listings: List of job listings to match
            resume_id: ID of the resume to match against
            
        Returns:
            List of ranked job matches with match percentages
        """
        # Retrieve the resume from DynamoDB
        resume = self._get_resume(resume_id)
        
        if not resume:
            return []
        
        # Process and rank each job using LLM
        ranked_jobs = []
        for job in job_listings:
            match_score = self._calculate_match_score(job, resume)
            job_with_score = {**job, "match_percentage": match_score}
            ranked_jobs.append(job_with_score)
        
        # Sort by match percentage in descending order
        ranked_jobs.sort(key=lambda x: x["match_percentage"], reverse=True)
        
        # Return top matches
        return ranked_jobs[:TOP_MATCHES]
    
    def _get_resume(self, resume_id: str) -> Optional[Dict[str, Any]]:
        """
        Get resume data from DynamoDB or use sample data for testing.
        
        Args:
            resume_id: ID of the resume to retrieve
            
        Returns:
            Resume data as dictionary
        """
        # For development, use sample resume data
        # In production, uncomment to use actual database:
        # return self.dynamodb_service.get_resume(resume_id)
        
        return {
            'resume_id': 'resume.pdf',
            'skills': ['software development', 'system integration', 'database design', 
                      'user experience', 'deployment', 'problem-solving', 'communication', 
                      'programming', 'teamwork', 'SDLC', 'data management', 
                      'performance testing', 'optimization', 'WPF', 'MVVM', 'Azure', 
                      'XML', 'eConnect', 'DotNetNuke'],
            'education': ['M.S. in Computer Science from Oklahoma State University, USA', 
                         'Bachelors in Computer Science from Mumbai University, India'],
            'experience_keywords': ['Amazon Rufus', 'Alexa Shopping Post Purchase Experience', 
                                   'Amazon mshop', 'Peak Readiness POC', 'ISOFlex Packaging Prism Application', 
                                   'Railcar Fleet management System', 'Azure Web App for Fuel Vendors and Paperless Invoices', 
                                   'Automatic Touchless Approvals', 'GP Integration Tool', 
                                   'Reston Association DotNetNuke Ecommerce Website', 'Axapta Client for Live Assistant'],
            'contact_info': {
                'name': 'MINALWAD', 
                'email': 'minalwad@gmail.com', 
                'phone': '+1(405)880-4889'
            }
        }
    
    def _calculate_match_score(self, job: Dict[str, Any], resume: Dict[str, Any]) -> float:
        """
        Use LLM to calculate match score between a job and resume.
        
        Args:
            job: Job listing as dictionary
            resume: Resume data as dictionary
            
        Returns:
            Match percentage as float (0-100)
        """
        # Prepare prompt for the LLM
        prompt = f"""
        Analyze the match between the following job listing and resume.
        Provide a numerical score from 0 to 100 representing how well the candidate matches the job requirements.
        
        JOB LISTING:
        {job}
        
        RESUME:
        {resume}
        
        Consider the following factors:
        1. Skills match (technical skills, soft skills)
        2. Experience relevance
        3. Education qualifications
        4. Any specific requirements mentioned in the job listing
        
        Return only the numeric score (0-100).
        """
        
        # Get response from LLM
        try:
            response = self.llm.predict(prompt)
            # Extract numeric match score from response
            # Handling potential non-numeric responses
            score = float(response.strip())
            # Ensure score is within valid range
            score = max(0, min(100, score))
            return score
        except Exception as e:
            # Handle exceptions gracefully
            print(f"Error calculating match score: {e}")
            # Return a default score if LLM call fails
            return 50.0