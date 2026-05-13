# src/tools.py
# Custom tools that our agents will use to do their work.
# CrewAI tools follow a simple pattern: a function + a decorator.

import requests
from bs4 import BeautifulSoup
from crewai_tools import tool


@tool("Job Description Scraper")
def scrape_job_description(url: str) -> str:
    """
    Scrapes a job posting from a URL and returns the raw text.
    Use this when the user provides a job posting URL instead of pasting the JD manually.
    Input: A valid job posting URL (e.g. LinkedIn, Naukri, Indeed, company website).
    Output: The cleaned text content of the job posting.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style tags (noise)
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        # Clean up excessive whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines[:300])  # Cap at 300 lines to stay within token limits

    except Exception as e:
        return f"Could not scrape URL: {str(e)}. Please paste the job description manually."


@tool("Resume Reader")
def read_resume(file_path: str) -> str:
    """
    Reads a plain-text resume file from disk.
    Input: Absolute or relative path to a .txt resume file (e.g. 'resume.txt').
    Output: The full text content of the resume.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Resume file not found at '{file_path}'. Please check the path."
    except Exception as e:
        return f"Error reading resume: {str(e)}"
