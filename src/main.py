import argparse
import logging
from crewai import Crew, Task
from agents.job_search_agent import JobSearchAgent
from agents.job_matcher_agent import JobMatcherAgent
from services.dynamodb_service import DynamoDBService
from config import TOP_MATCHES, DEFAULT_NUM_RESULTS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Job matching with CrewAI agents")
    
    parser.add_argument("--resume-id", required=True, help="ID of the resume to match jobs against")
    parser.add_argument("--keywords", required=True, nargs='+', help="Keywords for job search")
    parser.add_argument("--location", required=True, help="Location for job search")
    parser.add_argument("--country", default="gb", help="Country code for job search (default: gb)")
    parser.add_argument("--results", type=int, default=DEFAULT_NUM_RESULTS, 
                        help=f"Number of job results to fetch (default: {DEFAULT_NUM_RESULTS})")
    parser.add_argument("--top", type=int, default=TOP_MATCHES, 
                        help=f"Number of top matches to display (default: {TOP_MATCHES})")
    
    return parser.parse_args()

def main():
    """Main function to run the job matching crew."""
    args = parse_arguments()
    
    # Verify resume exists before proceeding
    db_service = DynamoDBService()
    resume = True#db_service.get_resume(args.resume_id)
    
    if not resume:
        logger.error(f"Resume with ID {args.resume_id} not found.")
        return
    
    #logger.info(f"Found resume for {resume.get('contact_info', {}).get('name', 'Unknown')}")
    
    # Initialize agents
    job_search_agent = JobSearchAgent()
    job_matcher_agent = JobMatcherAgent()
    
    # Define tasks
    search_task = Task(
        description=f"""
        Search for jobs using the following criteria:
        - Keywords: {{', '.join(args.keywords)}}
        - Location: {{args.location}}
        - Country: {{args.country}}
        - Number of results: {{args.results}}
        
        Return a comprehensive list of job listings matching these criteria.
        """,
        agent=job_search_agent.get_agent(),
        expected_output="A list of job listings with detailed information",
    )
    
    matching_task = Task(
        description=f"""
        Match the provided job listings with the resume ID {args.resume_id}.
        Analyze the skills, experience, and education in the resume and compare 
        them with the job requirements. Rank the job listings by match percentage 
        and return the top {args.top} matches.
        """,
        agent=job_matcher_agent.get_agent(),
        expected_output=f"Top {args.top} job matches with match percentages",
        context=[search_task]
    )
    
    # Create the crew
    crew = Crew(
        agents=[job_search_agent.get_agent(), job_matcher_agent.get_agent()],
        tasks=[search_task, matching_task],
        verbose=True
    )
    
    # Start the process
    logger.info("Starting job search and matching process...")
    
    try:
        # Instead of using crew.kickoff() which uses the LLM for task execution,
        # we'll manually handle the flow to use our custom implementations
        
        # Step 1: Search for jobs
        logger.info("Searching for jobs...")
        job_listings = job_search_agent.search_jobs(
            keywords=args.keywords,
            location=args.location,
            country=args.country,
            results_per_page=args.results
        )
        
        logger.info(f"Found {len(job_listings)} job listings")
        
        # Step 2: Match jobs to resume
        logger.info(f"Matching jobs to resume {args.resume_id}...")
        top_matches = job_matcher_agent.match_jobs_to_resume(
            job_listings=job_listings,
            resume_id=args.resume_id
        )
        
        # Display results
        logger.info(f"\nTop {len(top_matches)} Job Matches:")
        for job in top_matches:
            logger.info(f"\nRank: {job['rank']} - Match: {job['match_percentage']}%")
            logger.info(f"Title: {job['title']}")
            logger.info(f"Company: {job['company']}")
            logger.info(f"Location: {job['location']}")
            if job.get('url'):
                logger.info(f"URL: {job['url']}")
            
        return top_matches
        
    except Exception as e:
        logger.error(f"Error in job matching process: {e}")
        return []

if __name__ == "__main__":
    main()