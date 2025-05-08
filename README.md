# RecrutBot

RecrutBot is a playful experimental project designed to explore and compare how different AI APIs (Gemini, OpenAI, Mistral) handle multi-turn conversation, persona prompting, and context management.


## Local setup

Install [Visual Studio Code](https://code.visualstudio.com/) or another IDE.

Install [Python](https://www.python.org/downloads/) latest version, everything by default.

Install virtual environment and dependencies.

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
MISTRAL_API_KEY=AIz...
```

Launch RecrutBot

```bash
python src/main.py --max-turns 5      # default value is 4
```

## AI Differences: Gemini vs OpenAI

- **Gemini Chat Session API** automatically tracks conversation history.
- **OpenAI Assistant API**, also tracks conversation history but requires to create **an assistant**.
   > ⚠️ The script creates assistants that are visible in the OpenAI API Platform Dashboard. These assistants are automatically deleted at the end of the script or on CTRL+C, but they may persist if the Python process is terminated abruptly (e.g., kill -9).
- **OpenAI Completion API** and **Mistral Chat Completion API**, by contrast, requires that **the full conversation history be included with every request**.

## Workflow Overview

1. **Initialize Context**  
   We start by preparing a simple initial prompt from `config.json > prompt.initial`, which includes:
   - the candidate's **resume** file `docs/candidates_resume.pdf`
   - the **job description** file `docs/job_description.pdf`


2. **Pass Initial Context to Both Bots**  
   This prompt is sent to both Gemini and OpenAI.

   > ⚠️ **Note**: Including full files in the prompt consumes a large number of tokens, do not use too large files — this is just a POC.


4. **Run the Interview**
   - The conversation begins with the **recruiter**.
   - It will ask questions for **4 turns by default**.
   - At the end, it gives a **score** and a **GO/NOGO decision**.


## Settings file (`src/config.json`)

### IA section

| Setting | Description
|-|-
| `geminiModel`           | [Gemini Model](https://ai.google.dev/gemini-api/docs/models)
| `openAiModel`           | [OpenAI Model](https://platform.openai.com/docs/models)
| `temperature`           | Number which indicates how creative the models will be (0.0 = less creative, 1.0 = more creative)

### Recruiter in persona section

| Setting | Description
|-|-
| `recruiter`             | String which indicates the bot to use as recruiter. Accepted values: `gemini`, `mistral`, `openai_completion`, `openai_assistant`
| `recruiterPrefix`       | String which indicates the recruiter answers in the discussion
| `recruiterContextFile`  | String which indicates the path to the job description
| `recruiterPromptFile`   | String which indicates the path to the prompt of the recruiter

### Candidate in persona section

| Setting | Description
|-|-
| `candidate`             | String which indicates the bot to use as candidate. Accepted values: `gemini`, `mistral`, `openai_completion`, `openai_assistant`
| `candidatePrefix`       | String which indicates the candidate answers in the discussion
| `candidateContextFile`  | String which indicates the path to the candidate's resume
| `candidatePromptFile`   | String which indicates the path to the prompt of the candidate

### Prompts persona section

| Setting | Description
|-|-
| `initial`               | String used to create initial context in which job description and candidate's resume are included
| `recruiterStart`        | String used to start the interview
| `recruiterEnd`          | String used to end the interview on the recruiter side and give a recommendation
| `candidateEnd`          | String used to end the interview on the candidate side


## Sample interviews

Tries to **recruit an IT engineer for a babysitting job** — and have fun experimenting with the results!

| Langage | GO | NOGO
|-|-|-
| English | [`chats/babysitter_GO_EN.md`](./chats/babysitter_GO_EN.md) | [`chats/babysitter_NOGO_EN.md`](./chats/babysitter_NOGO_EN.md)
| French  | [`chats/babysitter_GO_FR.md`](./chats/babysitter_GO_FR.md) | [`chats/babysitter_NOGO_FR.md`](./chats/babysitter_NOGO_FR.md)
