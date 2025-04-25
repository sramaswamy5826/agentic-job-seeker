import unittest
from unittest.mock import patch, MagicMock
from src.agents.job_matcher_agent import JobMatcherAgent

class TestJobMatcherAgent(unittest.TestCase):
    """Tests for the Job Matcher Agent."""
    
    @patch('src.agents.job_matcher_agent.DynamoDBService')
    @patch('src.agents.job_matcher_agent.rank_jobs')
    @patch('src.agents.job_matcher_agent.get_top_matches')
    def setUp(self, mock_get_top_matches, mock_rank_jobs, mock_dynamodb_service):
        """Set up test fixtures."""
        self.mock_dynamodb_service = mock_dynamodb_service.return_value
        self.mock_rank_jobs = mock_rank_jobs
        self.mock_get_top_matches = mock_get_top_matches
        self.agent = JobMatcherAgent()
    
    def test_agent_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.get_agent())
    
    def test_match_jobs_to_resume_success(self):
        """Test matching jobs to resume successfully."""
        # Mock data
        resume_id = "resume123"
        job_listings = [
            {
                "id": "job1",
                "title": "Python Developer",
                "description": "Need Python and Django skills",
                "company": "Tech Co",
                "keywords": ["python", "django", "development"]
            },
            {
                "id": "job2",
                "title": "Data Scientist",
                "description": "Looking for data analysis skills",
                "company": "Data Inc",
                "keywords": ["python", "data", "analysis"]
            }
        ]
        
        mock_resume = {
            "id": resume_id,
            "skills": ["python", "django", "javascript"],
            "experience_keywords": ["development", "web"],
            "contact_info": {"name": "John Doe"}
        }
        
        mock_ranked_jobs = [
            (job_listings[0], 75.0),
            (job_listings[1], 50.0)
        ]
        
        mock_top_matches = [
            {
                "id": "job1",
                "title": "Python Developer",
                "description": "Need Python and Django skills",
                "company": "Tech Co",
                "keywords": ["python", "django", "development"],
                "match_percentage": 75.0,
                "rank": 1
            },
            {
                "id": "job2",
                "title": "Data Scientist",
                "description": "Looking for data analysis skills",
                "company": "Data Inc",
                "keywords": ["python", "data", "analysis"],
                "match_percentage": 50.0,
                "rank": 2
            }
        ]
        
        # Configure mocks
        self.mock_dynamodb_service.get_resume.return_value = mock_resume
        self.mock_rank_jobs.return_value = mock_ranked_jobs
        self.mock_get_top_matches.return_value = mock_top_matches
        
        # Call the method being tested
        result = self.agent.match_jobs_to_resume(job_listings, resume_id)
        
        # Verify interactions and result
        self.mock_dynamodb_service.get_resume.assert_called_once_with(resume_id)
        self.mock_rank_jobs.assert_called_once_with(job_listings, mock_resume)
        self.mock_get_top_matches.assert_called_once()
        
        self.assertEqual(result, mock_top_matches)
    
    def test_match_jobs_to_resume_no_resume(self):
        """Test matching jobs when resume is not found."""
        # Mock data
        resume_id = "nonexistent"
        job_listings = [{"id": "job1", "title": "Python Developer"}]
        
        # Configure mocks
        self.mock_dynamodb_service.get_resume.return_value = None
        
        # Call the method being tested
        result = self.agent.match_jobs_to_resume(job_listings, resume_id)
        
        # Verify interactions and result
        self.mock_dynamodb_service.get_resume.assert_called_once_with(resume_id)
        self.mock_rank_jobs.assert_not_called()
        self.mock_get_top_matches.assert_not_called()
        
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()