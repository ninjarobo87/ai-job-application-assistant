# 🤖 AI Job Application Assistant
**Built with CrewAI + Python | Portfolio Project**

A multi-agent AI system that takes a job description and your resume, then automatically generates a full application package — in under 3 minutes.

---

## What It Does

| Agent | Role | Output |
|-------|------|--------|
| 🔍 Job Analyst | Parses and structures the JD | Skills, responsibilities, keywords |
| 📊 Resume Strategist | Matches your resume to the role | Match score, gaps, reframing advice |
| ✍️ Cover Letter Writer | Writes a tailored cover letter | Ready-to-send cover letter |
| 🎤 Interview Coach | Prepares you for the interview | Questions + strong sample answers |

---

## Setup (5 minutes)

### 1. Clone / download the project
```bash
git clone https://github.com/yourusername/ai-job-assistant
cd ai_job_assistant
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
```bash
cp .env.example .env
# Open .env and add your OPENAI_API_KEY
```
Get your OpenAI key at: https://platform.openai.com/api-keys

### 5. Add your resume
Replace the contents of `resume.txt` with your actual resume in plain text format.

---

## Run It
```bash
python main.py
```

You'll be prompted to enter:
- Your name
- A job posting URL or paste the full JD
- Path to your resume file

All output is saved to the `outputs/` folder.

---

## Project Structure
```
ai_job_assistant/
├── main.py              # Entry point — run this
├── resume.txt           # Your resume (plain text)
├── requirements.txt     # Python dependencies
├── .env.example         # API key template
├── outputs/             # Generated application packages (auto-created)
└── src/
    ├── agents.py        # The 4 AI agents and their personas
    ├── tasks.py         # What each agent does, step by step
    ├── crew.py          # Assembles agents + tasks into a pipeline
    └── tools.py         # Custom tools (web scraper, resume reader)
```

---

## Tech Stack
- **[CrewAI](https://github.com/joaomdmoura/crewAI)** — Multi-agent orchestration framework
- **Python 3.10+**
- **OpenAI GPT-4o** — The LLM powering all agents
- **BeautifulSoup4** — Web scraping for job URLs
- **python-dotenv** — API key management

---

## Why This Project Demonstrates Agentic AI Skills

| Concept | How it appears in this project |
|---------|-------------------------------|
| Multi-agent orchestration | 4 specialized agents with distinct roles |
| Agent task decomposition | Complex job = 4 sequential focused tasks |
| Context passing between agents | Each agent's output feeds the next |
| Tool use | Agents call scraping + file reading tools |
| LLM integration | OpenAI API via LangChain abstraction |
| Pipeline design | Sequential process with dependency management |

This is conceptually identical to the multi-bot orchestration patterns from RPA — evolved for the LLM era.

---

## Next Steps / Improvements
- [ ] Add a Streamlit web UI (no terminal required)
- [ ] Support PDF resume input
- [ ] Add Hierarchical process with a Manager agent
- [ ] Integrate vector DB to store past job analyses
- [ ] Add email draft as a 5th agent output
- [ ] Deploy to cloud (FastAPI + Docker)

---

*Built by AJ as part of a career transition from RPA Development to Agentic AI Engineering.*
