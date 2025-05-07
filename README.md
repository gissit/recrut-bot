# RecrutBot

When a Gemini bot tries to recrut an OpenAI bot.

## Local setup

Install virtual environment and dependencies

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Miscellaneous commands

```bash
rd .venv -Recurse -Force
flake8 . --exclude=.venv --max-line-length=120
```

Create `.env` file at the root of the repository
```dotenv
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIz...
```

Launch RecrutBot

```bash
python src/main.py --max-turns 5      # default value is 4
```

## AI Differences: Gemini vs OpenAI

- **Gemini Chat Session** automatically tracks conversation history.
- **OpenAI Chat Completion**, by contrast, requires that **the full conversation history be included with every request**.

OpenAI is currently developing the **Assistants API v2**, which supports persistent threads and conversation context — but it's still in **beta**.


## Workflow Overview

1. **Initialize Context**  
   We start by preparing a simple initial prompt from `config.json > prompt.initial`, which includes:
   - the candidate's **resume** file `docs/candidates_resume.pdf`
   - the **job description** file `docs/job_description.pdf`

2. **Pass Initial Context to Both Bots**  
   This prompt is sent to both Gemini and OpenAI.

   > ⚠️ **Note**: Including full files in the prompt consumes a lot of tokens — but this is just a POC.

3. **Inject Role-Specific Prompts**:
   - `prompts/recruiter.txt` is passed to **Gemini** as a **user message** (⚠️ Gemini does not support `system` role).
   - `prompts/candidate.txt` is passed to **OpenAI** as a **system prompt**.

4. **Run the Interview**
   - The conversation begins with **Gemini acting as the recruiter**.
   - It will ask questions for **4 turns by default**.
   - At the end, it gives a **score** and a **GO/NOGO decision**.


## Goal of the POC

Try to **recruit an IT engineer for a babysitting job** — and have fun experimenting with the results!

Sample of a [GO](./chats/babysitter_fr_go.md) and a [NOGO](./chats/babysitter_fr_nogo.md), both are in french language.
