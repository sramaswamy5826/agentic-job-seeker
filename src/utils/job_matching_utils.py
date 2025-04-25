from typing import Dict, List, Any, Tuple
import re

def calculate_match_percentage(job: Dict[str, Any], resume: Dict[str, Any]) -> float:
    """
    Calculate the match percentage between a job listing and a resume.
    
    Args:
        job: Job listing data
        resume: Resume data
        
    Returns:
        Match percentage as a float (0-100)
    """
    # Extract job skills from description and title
    job_skills = set(job.get("keywords", []))
    job_title_words = set(tokenize_text(job.get("title", "")))
    job_skills.update(job_title_words)
    
    # Get resume skills
    resume_skills = set(resume.get("skills", []))
    resume_keywords = set(resume.get("experience_keywords", []))
    
    # Combine all resume skills and keywords
    all_resume_keywords = resume_skills.union(resume_keywords)
    
    # Calculate matches
    matching_skills = job_skills.intersection(all_resume_keywords)
    
    # Calculate match percentage
    if not job_skills:
        return 0.0
    
    match_percentage = (len(matching_skills) / len(job_skills)) * 100
    return min(match_percentage, 100.0)  # Cap at 100%

def tokenize_text(text: str) -> List[str]:
    """
    Convert text to lowercase tokens, removing punctuation.
    
    Args:
        text: Input text string
        
    Returns:
        List of tokens
    """
    if not text:
        return []
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation and split
    tokens = re.sub(r'[^\w\s]', ' ', text).split()
    
    # Remove common words and short tokens
    stop_words = {'and', 'the', 'for', 'to', 'in', 'of', 'a', 'with'}
    tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    
    return tokens

def rank_jobs(jobs: List[Dict[str, Any]], resume: Dict[str, Any]) -> List[Tuple[Dict[str, Any], float]]:
    """
    Rank jobs based on match percentage with resume.
    
    Args:
        jobs: List of job listings
        resume: Resume data
        
    Returns:
        List of tuples containing (job, match_percentage), sorted by match percentage
    """
    ranked_jobs = []
    
    for job in jobs:
        match_percentage = calculate_match_percentage(job, resume)
        ranked_jobs.append((job, match_percentage))
    
    # Sort by match percentage (descending)
    ranked_jobs.sort(key=lambda x: x[1], reverse=True)
    
    return ranked_jobs

def get_top_matches(ranked_jobs: List[Tuple[Dict[str, Any], float]], top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Get the top N job matches with their match percentages.
    
    Args:
        ranked_jobs: List of (job, match_percentage) tuples
        top_n: Number of top matches to return
        
    Returns:
        List of job dictionaries with added match_percentage field
    """
    top_matches = []
    
    for i, (job, match_percentage) in enumerate(ranked_jobs[:top_n]):
        # Create a copy of the job dictionary and add the match percentage
        job_with_match = job.copy()
        job_with_match["match_percentage"] = round(match_percentage, 2)
        job_with_match["rank"] = i + 1
        
        top_matches.append(job_with_match)
    
    return top_matches