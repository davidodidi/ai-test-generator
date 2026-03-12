"""
src/ai_generator/api_test_generator.py

Uses LangChain + Groq to generate pytest API test code targeting
the Open Library REST API (https://openlibrary.org/dev/docs/api).

Coverage areas generated:
  - Happy path (valid search and book detail)
  - Validation (empty/invalid query handling)
  - Schema (required fields present in response)
  - Response time (latency under threshold)
"""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .gemini_client import get_llm

API_TEST_PROMPT = PromptTemplate.from_template(
    """
You are a senior QA automation engineer. Generate a complete, runnable pytest test file
for the Open Library REST API (base URL: https://openlibrary.org).

Requirements:
- Use the `requests` library for HTTP calls. Do NOT use httpx.
- Do NOT define any pytest fixture named `base_url` — this name is reserved by
  pytest-playwright and will cause a ScopeMismatch error. Instead define a
  module-level constant: BASE_URL = "https://openlibrary.org"
- Use pytest parametrize where appropriate.
- Include these exact test coverage areas:
    1. Happy path: search for books by title (GET /search.json?title=<query>)
    2. Happy path: fetch a specific work by known OLID (GET /works/OL45804W.json — "Fantastic Mr Fox")
    3. Validation: search with an empty query string should return HTTP 200 with numFound=0 or handled gracefully
    4. Schema: verify required keys (numFound, docs) exist in search response JSON
    5. Schema: verify required keys (title, key) exist in a work detail response
    6. Response time: assert search endpoint responds in under 5 seconds
- Add a module-level docstring explaining what is being tested.
- Use explicit assert statements with descriptive messages.
- No mocking — these are live integration tests against the real API.
- Do NOT wrap output in markdown code fences. Output only raw Python code.

Generate the complete test file now.
"""
)


def generate_api_tests() -> str:
    """
    Invoke Groq via LangChain to generate API test source code.

    Returns:
        str: Raw Python source code for the generated test file.
    """
    chain = API_TEST_PROMPT | get_llm() | StrOutputParser()
    return chain.invoke({})
