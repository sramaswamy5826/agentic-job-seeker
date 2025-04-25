import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Adzuna API Configuration
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY")
ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# DynamoDB Configuration
RESUME_TABLE_NAME = "ResumeData"

# CrewAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = "gpt-4"

# Application Configuration
DEFAULT_NUM_RESULTS = 10
TOP_MATCHES = 5