# src/crew.py
# This is where the Crew is assembled.
# A Crew combines agents + tasks and decides HOW they run (Sequential vs Hierarchical).
# Sequential = tasks run one after another, in order (simplest and best for beginners).

from crewai import Crew, Process
from src.agents import create_agents
from src.tasks import create_tasks


def build_crew(llm, job_input: str, resume_path: str, candidate_name: str) -> Crew:
    """
    Assembles the full crew with agents and tasks wired together.

    Args:
        llm: The language model instance (OpenAI or Anthropic)
        job_input: Job URL or full JD text
        resume_path: Path to resume .txt file
        candidate_name: Candidate's full name

    Returns:
        A configured Crew object, ready to run with crew.kickoff()
    """

    # Step 1: Create agents
    agents = create_agents(llm)

    # Step 2: Create tasks, wiring them to agents and passing user inputs
    tasks = create_tasks(agents, job_input, resume_path, candidate_name)

    # Step 3: Build the Crew
    crew = Crew(
        agents=list(agents),
        tasks=list(tasks),
        process=Process.sequential,  # Tasks run in order: analyze job → analyze resume → cover letter → interview prep
        verbose=2,                   # Verbose=2 shows detailed agent thinking (great for learning!)
    )

    return crew
