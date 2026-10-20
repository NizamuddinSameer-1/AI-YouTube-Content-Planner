# YT Content Planner Pro

**AI-powered YouTube planning workspace** to go from a topic idea to a structured content plan, script outline, and export-ready assets in minutes.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C)
![Google%20Gemini](https://img.shields.io/badge/Google%20Gemini-GenAI-4285F4)

## Demo / Screenshot

> Replace this section with a real screenshot or GIF.

- Suggested file path: `docs/demo.png`
- Then update this Markdown:

```md
![YT Content Planner Pro Demo](docs/demo.png)
```

---

## What This App Does

`YT Content Planner Pro` is a Streamlit app (`app.py`) that helps creators:

- Enter a YouTube topic and configure:
  - Niche
  - Target audience
  - Video format
  - Tone
- Generate a structured content plan with:
  - 10 video ideas
  - 5 SEO-friendly titles
  - 1 ready-to-use video description
  - 10 hashtags
  - Thumbnail concept (text, visual concept, mood)
  - Suggested upload days/time
- Select one idea and generate:
  - Timestamped script outline sections
  - 3 retention hooks (Visual, Verbal, Text-on-Screen)
- Export results as:
  - Markdown
  - CSV
  - Plain text

---

## Architecture / Workflow Overview

1. **Input Layer (Streamlit UI):** User enters topic + creative settings.
2. **Config/Auth Layer:** App reads `GOOGLE_API_KEY` from `st.secrets` or sidebar input.
3. **AI Generation Layer (LangChain + Gemini):**
   - Chain 1: content plan generation
   - Chain 2: script outline + retention hooks
4. **Validation Layer (Pydantic):** Structured responses are parsed/validated into typed models.
5. **Output Layer:** Results are displayed in tabs and exported to Markdown/CSV/text.

---

## Tech Stack

- **Python**
- **Streamlit**
- **LangChain**
- **langchain-google-genai**
- **Pydantic**
- **Google Gemini**

---

## Prerequisites

- Python **3.11+**
- A Google AI API key for Gemini (`GOOGLE_API_KEY`)
- `pip`

---

## Local Setup

### 1) Clone the repository

```bash
git clone https://github.com/NizamuddinSameer-1/AI-YouTube-Content-Planner.git
cd AI-YouTube-Content-Planner
```

### 2) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

> On Windows (PowerShell):
>
> ```powershell
> .venv\Scripts\Activate.ps1
> ```

### 3) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4) Configure `GOOGLE_API_KEY`

You can use either method:

#### Option A: Streamlit secrets (recommended)
Create `.streamlit/secrets.toml` in the project root:

```toml
GOOGLE_API_KEY = "your_api_key_here"
```

#### Option B: Enter key in the app sidebar
Run the app and paste your key in the sidebar input.

⚠️ **Security warning:** Never commit API keys to Git. Keep `secrets.toml` local and ensure secrets are ignored.

### 5) Run the app

```bash
streamlit run app.py
```

Open: `http://localhost:8501`

---

## GitHub Codespaces / Dev Container

This repository includes `.devcontainer/devcontainer.json` configured for:

- Python 3.11 dev container image
- Dependency install via `requirements.txt`
- Streamlit auto-run command
- Port forwarding for **8501**

### Using Codespaces

1. Open the repository on GitHub.
2. Click **Code → Codespaces → Create codespace on main** (or your branch).
3. Wait for setup to complete.
4. Open the forwarded Streamlit port (8501) in preview/browser.

### Using VS Code Dev Containers

1. Install the **Dev Containers** extension.
2. Open the repo in VS Code.
3. Run: **Dev Containers: Reopen in Container**.
4. Start app (if not already running):

```bash
streamlit run app.py
```

---

## How to Use

1. Launch the app.
2. Provide your `GOOGLE_API_KEY` (secrets or sidebar).
3. Enter a YouTube topic.
4. Choose niche, target audience, video format, and tone.
5. Click **Generate Content Plan**.
6. Review ideas, SEO titles, description, hashtags, thumbnail concept, and schedule.
7. Pick one idea and click **Generate Script + Hooks**.
8. Export plan/script as Markdown, CSV, or text.

---

## Suggested Project Structure (Known Files)

```text
AI-YouTube-Content-Planner/
├─ app.py
├─ requirements.txt
└─ .devcontainer/
   └─ devcontainer.json
```

---

## Troubleshooting

### 1) Missing API key / auth issues
- Ensure `GOOGLE_API_KEY` is set in `.streamlit/secrets.toml` **or** entered in sidebar.
- Restart Streamlit after updating secrets.

### 2) Dependency installation failures
- Upgrade pip: `pip install --upgrade pip`
- Reinstall from `requirements.txt`
- Confirm you are in the active virtual environment.

### 3) Invalid model/API responses
- Retry generation (temporary model/network issues can occur).
- Verify your API key is valid and has Gemini access.
- Check for API quota/rate-limit issues in your Google account.

### 4) Port 8501 not accessible
- Ensure Streamlit is running: `streamlit run app.py`
- Check if another process is using port 8501.
- In Codespaces/devcontainer, ensure port **8501** is forwarded.

---

## Responsible Use & Security Notes

- AI-generated outputs may contain inaccuracies; review before publishing.
- Validate SEO claims, factual statements, and audience-sensitive content manually.
- Do not expose or commit API keys in source code, commits, issues, or screenshots.
- Treat exported content as drafts that require editorial and brand review.

---

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make focused changes.
4. Open a pull request with a clear description.

---

## License

No license file is currently specified in this repository.

If you are the maintainer, consider adding a `LICENSE` file to define usage permissions.

---

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [langchain-google-genai](https://python.langchain.com/docs/integrations/chat/google_generative_ai/)
- [Pydantic](https://docs.pydantic.dev/)
- [Google Gemini](https://ai.google.dev/)
