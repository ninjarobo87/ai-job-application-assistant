# src/tasks.py
# Tasks are the actual jobs each agent performs.
# Each task has: a description (what to do), an expected_output (what to return), and an assigned agent.
# In a Sequential process, tasks run one after another — each task can use the output of the previous one.

from crewai import Task


def create_tasks(agents, job_input: str, resume_path: str, candidate_name: str):
    """
    Creates the four tasks for the pipeline.

    Args:
        agents: Tuple of (job_analyst, resume_strategist, cover_letter_writer, interview_coach)
        job_input: Either a job posting URL or the full job description text
        resume_path: Path to the candidate's resume .txt file
        candidate_name: The candidate's name for personalization
    """
    job_analyst, resume_strategist, cover_letter_writer, interview_coach = agents

    # ─────────────────────────────────────────────
    # TASK 1: Analyze the Job Description
    # ─────────────────────────────────────────────
    analyze_job_task = Task(
        description=(
            f"Analyze the following job input thoroughly:\n\n{job_input}\n\n"
            "If this is a URL, use the Job Description Scraper tool to fetch the content first. "
            "Then extract and structure:\n"
            "1. Job title and company name\n"
            "2. Must-have technical skills (hard requirements)\n"
            "3. Nice-to-have skills (preferred)\n"
            "4. Key responsibilities (top 5-7)\n"
            "5. Seniority level and expected experience\n"
            "6. Any culture or soft-skill signals\n"
            "7. Keywords that should appear in a strong application"
        ),
        expected_output=(
            "A clean, structured breakdown of the job description with clearly labeled sections: "
            "Job Title, Company, Must-Have Skills, Nice-to-Have Skills, Key Responsibilities, "
            "Seniority Level, Culture Signals, and Target Keywords."
        ),
        agent=job_analyst,
    )

    # ─────────────────────────────────────────────
    # TASK 2: Analyze Resume Against the Job
    # ─────────────────────────────────────────────
    analyze_resume_task = Task(
        description=(
            f"Read the resume from this file path: {resume_path}\n\n"
            f"The candidate's name is: {candidate_name}\n\n"
            "Use the Resume Reader tool to load the resume. "
            "Then compare it against the job analysis from the previous task and produce:\n"
            "1. A match score (0-100) with brief justification\n"
            "2. Top 3-5 strengths — where the candidate's background aligns well\n"
            "3. Top 2-3 gaps — skills or experience that are missing or weak\n"
            "4. Reframing suggestions — how to present existing experience in job-relevant language\n"
            "5. One key narrative the candidate should lead with in their application"
        ),
        expected_output=(
            "A structured resume analysis report with: Match Score, Strengths, Gaps, "
            "Reframing Suggestions, and a recommended Application Narrative."
        ),
        agent=resume_strategist,
        context=[analyze_job_task],  # This task receives output from Task 1
    )

    # ─────────────────────────────────────────────
    # TASK 3: Write the Cover Letter
    # ─────────────────────────────────────────────
    write_cover_letter_task = Task(
        description=(
            f"Write a tailored cover letter for {candidate_name} applying to this role.\n\n"
            "Use the job analysis and resume analysis from previous tasks as your input.\n"
            "Requirements:\n"
            "- 3-4 paragraphs, under 400 words\n"
            "- Opening: Hook with a specific reason why this role/company excites the candidate\n"
            "- Middle: Connect 2-3 concrete past experiences to the job's key requirements\n"
            "- Closing: Confident call to action, not desperate\n"
            "- Tone: Professional but human — avoid buzzwords and clichés\n"
            "- Use the candidate's reframing narrative from the resume analysis"
        ),
        expected_output=(
            "A complete, ready-to-send cover letter addressed 'Dear Hiring Manager,' "
            "with a subject line suggestion at the top. Under 400 words. No placeholder text."
        ),
        agent=cover_letter_writer,
        context=[analyze_job_task, analyze_resume_task],  # Uses output from Tasks 1 and 2
    )

    # ─────────────────────────────────────────────
    # TASK 4: Generate Interview Preparation
    # ─────────────────────────────────────────────
    interview_prep_task = Task(
        description=(
            f"Generate interview preparation material for {candidate_name} for this role.\n\n"
            "Based on the job requirements and the candidate's background from previous tasks, create:\n"
            "1. 3 Technical questions likely to be asked (with strong sample answers)\n"
            "2. 2 Behavioral questions using the STAR format (with sample answers)\n"
            "3. 1 'Why are you switching roles?' question with a strong, honest answer "
            "   that turns the career pivot into a strength\n"
            "4. 2 Smart questions the candidate should ask the interviewer\n"
            "All sample answers should be grounded in the candidate's actual background."
        ),
        expected_output=(
            "A structured interview prep guide with clearly labeled sections for each question type, "
            "including both the question and a tailored sample answer."
        ),
        agent=interview_coach,
        context=[analyze_job_task, analyze_resume_task],
    )

    return analyze_job_task, analyze_resume_task, write_cover_letter_task, interview_prep_task
