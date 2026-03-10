# ai-test-generator

An AI-powered test generation framework that uses **Google Gemini (free tier)** via **LangChain** to generate pytest + Playwright test suites targeting **Open Library** — a production website and public REST API.

> **David Odidi — QA Automation Engineer | Java • Selenium • Playwright • Cypress • RestAssured • Python • CI/CD (GitHub Actions and Jenkins) | github.com/davidodidi**

---

## Why Open Library?

[Open Library](https://openlibrary.org) provides both a real production UI and a documented REST API at the same domain — ideal for demonstrating full-stack QA coverage without any paid credentials or mocking.

---

## Architecture

```
ai-test-generator/
├── src/ai_generator/
│   ├── gemini_client.py        # LangChain ChatGoogleGenerativeAI wrapper
│   ├── api_test_generator.py   # Prompt → Gemini → API test code
│   └── e2e_test_generator.py   # Prompt → Gemini → Playwright test code
├── tests/
│   ├── api/test_openlibrary_api.py   # API integration tests (requests)
│   └── e2e/test_openlibrary_ui.py    # E2E UI tests (Playwright)
├── scripts/
│   └── generate_tests.py       # CLI: regenerate tests via Gemini
├── conftest.py
├── pytest.ini
└── .github/workflows/ci.yml
```

### How AI generation works

1. `scripts/generate_tests.py` is called (manually or in CI)
2. LangChain constructs a prompt describing the desired test coverage
3. Gemini (`gemini-1.5-flash`, free tier) returns raw Python test code
4. The output is written to `tests/api/` or `tests/e2e/`
5. pytest runs the generated files as normal

---

## Prerequisites

- Python 3.11+
- A **free** Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

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
# Edit .env and set GEMINI_API_KEY=<your key>
```

---

## Usage

### Run the baseline tests (no Gemini key needed)

```bash
# API tests only
pytest tests/api/ -m api -v

# E2E tests only
pytest tests/e2e/ -m e2e -v --browser chromium

# All tests
pytest
```

### Regenerate tests via Gemini

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
| `generate-tests` | When `GEMINI_API_KEY` secret is set | Calls Gemini, writes generated tests, runs them |

To enable AI generation in CI:

1. Go to **Settings → Secrets → Actions** in your GitHub repo
2. Add secret: `GEMINI_API_KEY` = your Gemini API key
3. Add variable: `GEMINI_API_KEY_AVAILABLE` = `true`

---

## API Test Coverage

| Area | Endpoint | Test |
|---|---|---|
| Happy path | `GET /search.json?title=Dune` | HTTP 200, numFound > 0 |
| Happy path | `GET /works/OL45804W.json` | HTTP 200, correct title |
| Validation | `GET /search.json?title=` | Graceful 200 response |
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
| AI / LLM | Google Gemini (`gemini-1.5-flash`) — free tier |
| LLM framework | LangChain (`langchain`, `langchain-google-genai`) |
| API testing | pytest + requests |
| E2E testing | pytest + Playwright (Python) |
| CI | GitHub Actions |
