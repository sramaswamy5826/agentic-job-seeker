import unittest
from unittest.mock import patch, MagicMock
from src.agents.job_search_agent import JobSearchAgent

class TestJobSearchAgent(unittest.TestCase):
    """Tests for the Job Search Agent."""
    
    @patch('src.agents.job_search_agent.AdzunaService')
    def setUp(self, mock_adzuna_service):
        """Set up test fixtures."""
        self.mock_adzuna_service = mock_adzuna_service.return_value
        self.agent = JobSearchAgent()
    
    def test_agent_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.get_agent())
        
    def test_search_jobs(self):
        """Test the search_jobs method."""
        # Mock data
        keywords = ["python", "developer"]
        location = "London"
        country = "gb"
        results_per_page = 5
        
        # Mock response data
        mock_raw_response = {
            "results": [
                {
                    "id": "job1",
                    "title": "Python Developer",
                    "description": "We need a Python developer with Django experience",
                    "company": {"display_name": "Tech Co"},
                    "location": {"display_name": "London"},
                    "redirect_url": "https://example.com/job1",
                    "salary_min": 40000,
                    "salary_max": 60000,
                    "created": "2025-01-01T12:00:00Z",
                    "category": {"label": "IT Jobs"}
                }
            ]
        }
        
        mock_parsed_jobs = [
            {
                "id": "job1",
                "title": "Python Developer",
                "description": "We need a Python developer with Django experience",
                "company": "Tech Co",
                "location": "London",
                "url": "https://example.com/job1",
                "salary_min": 40000,
                "salary_max": 60000,
                "created": "2025-01-01T12:00:00Z",
                "category": "IT Jobs",
                "keywords": ["python", "developer", "django", "experience"]
            }
        ]
        
        # Configure mocks
        self.mock_adzuna_service.search_jobs.return_value = mock_raw_response
        self.mock_adzuna_service.parse_job_results.return_value = mock_parsed_jobs
        
        # Call the method being tested
        result = self.agent.search_jobs(keywords, location, country, results_per_page)
        
        # Verify interactions and result
        self.mock_adzuna_service.search_jobs.assert_called_once_with(
            country=country,
            keywords=keywords,
            location=location,
            results_per_page=results_per_page
        )
        
        self.mock_adzuna_service.parse_job_results.assert_called_once_with(mock_raw_response)
        
        self.assertEqual(result, mock_parsed_jobs)

if __name__ == '__main__':
    unittest.main()