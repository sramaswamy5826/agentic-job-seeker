from crewai import Agent
from langchain.tools import BaseTool
from typing import Dict, List, Any, Optional, Type
from pydantic import BaseModel, Field
from services.dynamodb_service import DynamoDBService
from config import LLM_MODEL, TOP_MATCHES
from src.tools.job_matching_tool import JobMatchingTool
from langchain_openai import ChatOpenAI


class JobMatcherAgent:
    """
    Agent responsible for matching job listings with a candidate's resume.
    """
    
    def __init__(self, llm_model: str = LLM_MODEL):
        """
        Initialize the Job Matcher Agent.
        
        Args:
            llm_model: Language model to use for the agent
        """
        #from langchain.llms import BaseLLM
        
        # Initialize LLM
        self.llm = ChatOpenAI(model=llm_model)
        
        # Create the job matching tool
        self.job_matching_tool = JobMatchingTool(llm=self.llm)
        
        # Create agent with the tool
        self.agent = self._create_agent(llm_model)
        
    def _create_agent(self, llm_model: str) -> Agent:
        """
        Create the CrewAI agent with tools.
        
        Args:
            llm_model: Language model to use
            
        Returns:
            CrewAI Agent instance
        """
        return Agent(
            role="Job Matching Specialist",
            goal="Match job listings with candidate resumes based on skills and experience",
            backstory="""
            You are a skilled job matching specialist with expertise in analyzing resumes
            and job descriptions to find the perfect match. You have a keen eye for
            identifying transferable skills and understanding how a candidate's background
            aligns with job requirements. Your recommendations help job seekers focus on
            opportunities where they have the highest chance of success.
            """,
            verbose=True,
            allow_delegation=False,
            llm_model=llm_model,
            tools=[self.job_matching_tool]
        )
    
    def match_jobs_to_resume(self, job_listings: List[Dict[str, Any]], resume_id: str) -> List[Dict[str, Any]]:
        """
        Match job listings to a candidate's resume using the job matching tool.
        
        Args:
            job_listings: List of job listings to match
            resume_id: ID of the resume to match against
            
        Returns:
            List of ranked job matches with match percentages
        """
        # Use the tool directly
        return self.job_matching_tool._run(job_listings, resume_id)
    
    def get_agent(self) -> Agent:
        """
        Get the CrewAI agent instance.
        
        Returns:
            CrewAI Agent instance
        """
        return self.agent