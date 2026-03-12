# ai-test-generator

An AI-powered test generation framework that uses **Groq (LLaMA 3.3-70b)** via **LangChain** to autonomously generate pytest + Playwright test suites targeting **Open Library** — a production website and public REST API.

> **David Odidi — QA Automation Engineer | Java • Selenium • Playwright • Cypress • RestAssured • Python • CI/CD (GitHub Actions and Jenkins) | github.com/davidodidi**

---

## Why Open Library?

[Open Library](https://openlibrary.org) provides both a real production UI and a documented REST API at the same domain — ideal for demonstrating full-stack QA coverage without any paid credentials or mocking.

---

## Architecture

```
ai-test-generator/
├── src/ai_generator/
│   ├── gemini_client.py        # LangChain ChatGroq wrapper (LLaMA 3.3-70b)
│   ├── api_test_generator.py   # Prompt → Groq → API test code
│   └── e2e_test_generator.py   # Prompt → Groq → Playwright test code
├── tests/
│   ├── api/test_openlibrary_api.py   # API integration tests (requests)
│   └── e2e/test_openlibrary_ui.py    # E2E UI tests (Playwright)
├── scripts/
│   └── generate_tests.py       # CLI: regenerate tests via Groq
├── conftest.py
├── pytest.ini
└── .github/workflows/ci.yml
```

### How AI generation works

1. `scripts/generate_tests.py` is called (manually or in CI)
2. LangChain constructs a detailed prompt describing the desired test coverage, selectors, and Playwright rules
3. Groq (`llama-3.3-70b-versatile`, free tier) returns raw Python test code
4. Code fences are stripped programmatically in case the LLM includes them
5. The output is written to `tests/api/` or `tests/e2e/`
6. pytest runs the generated files immediately to validate them

---

## Prerequisites

- Python 3.11+
- A **free** Groq API key from [console.groq.com](https://console.groq.com/keys)

---

## Setup

```bash
git clone https://github.com/davidodidi/ai-test-generator.git
cd ai-test-generator

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium

cp .env.example .env
# Edit .env and set GROQ_API_KEY=<your key>
```

---

## Usage

### Run the baseline tests (no Groq key needed)

```bash
# API tests only
pytest tests/api/ -m api -v

# E2E tests only
pytest tests/e2e/ -m e2e -v --browser chromium

# All tests
pytest
```

### Regenerate tests via Groq

```bash
# Regenerate both API and E2E tests
python scripts/generate_tests.py

# Regenerate API tests only
python scripts/generate_tests.py --api

# Regenerate E2E tests only
python scripts/generate_tests.py --e2e
```

After generation, run pytest normally — the generated files replace the baselines.

---

## CI (GitHub Actions)

Three jobs run on every push to `main`:

| Job | Trigger | What it does |
|---|---|---|
| `api-tests` | Always | Runs `tests/api/` against live Open Library API |
| `e2e-tests` | Always | Runs `tests/e2e/` headless via Playwright/Chromium |
| `generate-tests` | When `GROQ_API_KEY` secret is set | Calls Groq, writes generated tests, runs them |

To enable AI generation in CI:

1. Go to **Settings → Secrets and variables → Actions** in your GitHub repo
2. Add secret: `GROQ_API_KEY` = your Groq API key
3. Add variable: `GROQ_API_KEY_AVAILABLE` = `true`

---

## API Test Coverage

| Area | Endpoint | Test |
|---|---|---|
| Happy path | `GET /search.json?title=Dune` | HTTP 200, numFound > 0 |
| Happy path | `GET /works/OL45804W.json` | HTTP 200, correct title |
| Validation | `GET /search.json?title=` | HTTP 500 (known Open Library API bug) |
| Validation | `GET /works/OL00000000INVALID.json` | HTTP 404 |
| Schema | `/search.json` response | `numFound`, `docs` keys present |
| Schema | Work detail response | `title`, `key` keys present |
| Response time | `/search.json` | < 5 seconds |
| Response time | `/works/<olid>.json` | < 5 seconds |

## E2E Test Coverage

| Area | Flow |
|---|---|
| Homepage | Title contains "Open Library", search input visible |
| Header | Logo/nav is visible |
| Search | Enter "Dune" → submit → URL contains `/search` |
| Search results | Result items visible, page contains "Dune" |
| Book detail | Click first result → navigate to `/works/` URL |
| Book detail | h1 heading is visible and non-empty |

---

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| AI / LLM | Groq (`llama-3.3-70b-versatile`) — free tier |
| LLM framework | LangChain (`langchain`, `langchain-groq`) |
| API testing | pytest + requests |
| E2E testing | pytest + Playwright (Python) |
| CI | GitHub Actions (Ubuntu 24.04) |
