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
- **OpenAI Assistant API**, also tracks conversation history but requires to create **an assistant**.
- **OpenAI Completion API**, by contrast, requires that **the full conversation history be included with every request**.


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


## Settings file (`src/config.json`)

| Section | Setting | Description
|-|-|-
| `ia`      | `geminiModel`           | [Gemini Model](https://ai.google.dev/gemini-api/docs/models)
| `ia`      | `openAiModel`           | [OpenAI Model](https://platform.openai.com/docs/models)
| `ia`      | `useOpenAiAssistantApi` | Boolean which indicates to use OpenAI Assistant API instead of Completion API
| `ia`      | `temperature`           | Number which indicates how creative the models will be (0.0 = less creative, 1.0 = more creative)
| `persona` | `recruiter`             | String which indicates the recruiter answers
| `persona` | `recruiterContextFile`  | String which indicates the path to the job description
| `persona` | `recruiterPromptFile`   | String which indicates the path to the prompt of the recruiter
| `persona` | `candidate`             | String which indicates the candidate answers
| `persona` | `candidateContextFile`  | String which indicates the path to the candidate's resume
| `persona` | `candidatePromptFile`   | String which indicates the path to the prompt of the candidate
| `prompt`  | `initial`               | String used to create initial context in which job description and candidate's resume are included
| `prompt`  | `recruiterStart`        | String used to start the interview
| `prompt`  | `recruiterEnd`          | String used to end the interview on the recruiter side and give a recommendation
| `prompt`  | `candidateEnd`          | String used to end the interview on the candidate side


## Sample interviews

Tries to **recruit an IT engineer for a babysitting job** — and have fun experimenting with the results!

| Langage | GO | NOGO
|-|-|-
| English | [`chats/babysitter_GO_EN.md`](./chats/babysitter_GO_EN.md) | [`chats/babysitter_NOGO_EN.md`](./chats/babysitter_NOGO_EN.md)
| French  | [`chats/babysitter_GO_FR.md`](./chats/babysitter_GO_FR.md) | [`chats/babysitter_NOGO_FR.md`](./chats/babysitter_NOGO_FR.md)
