# main.py
# ─────────────────────────────────────────────────────────────
# AI Job Application Assistant
# Built with: CrewAI + Python
# Author: AJ
# ─────────────────────────────────────────────────────────────
#
# HOW TO RUN:
#   1. pip install -r requirements.txt
#   2. cp .env.example .env  →  fill in your OPENAI_API_KEY
#   3. Put your resume as plain text in resume.txt
#   4. python main.py
#
# WHAT IT DOES:
#   Takes a job description (URL or text) + your resume
#   and runs 4 AI agents in sequence to produce:
#     ✅ Job breakdown & keyword extraction
#     ✅ Resume-to-JD match analysis
#     ✅ Tailored cover letter
#     ✅ Interview prep questions & answers
# ─────────────────────────────────────────────────────────────

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from src.crew import build_crew

# Load environment variables from .env file
load_dotenv()


def get_user_inputs() -> tuple[str, str, str]:
    """Collect inputs from the user via the terminal."""

    print("\n" + "=" * 60)
    print("  🤖 AI Job Application Assistant")
    print("=" * 60)

    candidate_name = input("\n👤 Your full name: ").strip()

    print("\n📋 Job Description Input")
    print("   Enter a job posting URL, OR paste the full JD.")
    print("   (If pasting, type END on a new line when done)\n")

    first_line = input("URL or first line of JD: ").strip()

    # If it looks like a URL, use it directly
    if first_line.startswith("http"):
        job_input = first_line
    else:
        # Multi-line paste mode
        lines = [first_line]
        print("   Continue pasting... (type END to finish)")
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        job_input = "\n".join(lines)

    resume_path = input("\n📄 Path to your resume .txt file (e.g. resume.txt): ").strip()
    if not resume_path:
        resume_path = "resume.txt"

    return candidate_name, job_input, resume_path


def save_output(result: str, candidate_name: str):
    """Save the crew's full output to a timestamped file."""
    from datetime import datetime

    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = candidate_name.replace(" ", "_").lower()
    filename = f"outputs/application_{safe_name}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"AI Job Application Assistant — Output\n")
        f.write(f"Candidate: {candidate_name}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(str(result))

    print(f"\n✅ Full output saved to: {filename}")
    return filename


def main():
    # ── Validate API key ──────────────────────────────────────
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "sk-your-key-here":
        print("❌ ERROR: OPENAI_API_KEY not set. Please fill in your .env file.")
        return

    # ── Collect user inputs ───────────────────────────────────
    candidate_name, job_input, resume_path = get_user_inputs()

    # ── Initialize the LLM ───────────────────────────────────
    # Using GPT-4o for best reasoning quality.
    # To use Anthropic Claude instead, swap this with:
    #   from langchain_anthropic import ChatAnthropic
    #   llm = ChatAnthropic(model="claude-sonnet-4-20250514", api_key=os.getenv("ANTHROPIC_API_KEY"))
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,  # Low temp = more consistent, focused outputs
        api_key=api_key,
    )

    # ── Build and run the crew ────────────────────────────────
    print("\n🚀 Starting AI agents... (this takes 1-3 minutes)\n")
    print("-" * 60)

    crew = build_crew(
        llm=llm,
        job_input=job_input,
        resume_path=resume_path,
        candidate_name=candidate_name,
    )

    result = crew.kickoff()

    # ── Display and save output ───────────────────────────────
    print("\n" + "=" * 60)
    print("  ✅ DONE — Here is your Application Package")
    print("=" * 60)
    print(result)

    save_output(result, candidate_name)


if __name__ == "__main__":
    main()
