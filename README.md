# Job Matching Agents

A job search and recommendation system built with CrewAI that uses agents to search for jobs and match them to a candidate's resume.

## Overview

This project implements an agentic framework using CrewAI with two specialized agents:

1. **Job Search Agent**: Searches for job listings by location and keywords using the Adzuna API.
2. **Job Matcher Agent**: Reads a resume from a DynamoDB table and matches it against job listings, ranking them by relevance.

The agents work together to provide personalized job recommendations based on a candidate's skills and experience.

## Features

- Search for jobs by keywords and location using the Adzuna API
- Retrieve resume data from AWS DynamoDB
- Calculate match percentages between job listings and resumes
- Rank job listings based on match percentage
- Return top job matches with detailed information

## Prerequisites

- Python 3.8+
- AWS account with DynamoDB access
- Adzuna API credentials
- OpenAI API key for CrewAI

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/<yourusername>/agentic-job-seeker.git
   cd agentic-job-seeker
   ```

2. Create a virtual environment:
   ```
   python3.11 -m venv venv #crewai is compatile with python3.11
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file from the example:
   ```
   cp .env.example .env
   ```

6. Fill in your API keys and AWS credentials in the `.env` file.

## DynamoDB Setup

The project expects a DynamoDB table named "ResumeData" with the following schema:

```json
{
  "id": "string",
  "skills": ["skill1", "skill2", ...],
  "education": ["degree1", "degree2", ...],
  "experience_keywords": ["keyword1", "keyword2", ...],
  "contact_info": {
    "name": "Full Name",
    "email": "email@example.com",
    "phone": "phone number if available"
  }
}
```

## Usage

Run the application with the required parameters:

```
python src/main.py --resume-id "resume123" --keywords python javascript "data science" --location "London" --country "gb"
```

### Command Line Arguments

- `--resume-id`: ID of the resume to match jobs against (required)
- `--keywords`: Space-separated list of job keywords to search for (required)
- `--location`: Location for job search (required)
- `--country`: Country code for job search (default: "gb")
- `--results`: Number of job results to fetch (default: 10)
- `--top`: Number of top matches to display (default: 5)

## How It Works

1. The Job Search Agent fetches job listings from the Adzuna API based on the specified keywords and location.
2. The job listings are passed to the Job Matcher Agent.
3. The Job Matcher Agent retrieves the resume data from DynamoDB using the provided resume ID.
4. The agent then calculates match percentages between each job listing and the resume.
5. The job listings are ranked by match percentage, and the top matches are returned.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing

Run the tests with pytest:

```
pytest
```

## Future Enhancements

- Add more advanced matching algorithms using NLP
- Implement resume parsing for PDF and Word documents
- Add support for more job board APIs
- Develop a web interface for easier interaction
- Implement user feedback to improve matching over time
- Add more agents for specialized tasks like resume improvement suggestions

## License


## Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewai) for the agent framework
- [Adzuna](https://developer.adzuna.com/) for the job API
- AWS for DynamoDB service