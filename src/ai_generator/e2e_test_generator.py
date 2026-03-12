"""
src/ai_generator/e2e_test_generator.py

Uses LangChain + Groq to generate Playwright (Python) E2E test code
targeting the Open Library UI at https://openlibrary.org.

Coverage areas generated:
  - Homepage loads and key elements are visible
  - Search flow: enter query, submit, verify results page
  - Book detail navigation: click a result, verify title on detail page
  - Navigation sanity: header/logo visible
"""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .gemini_client import get_llm

E2E_TEST_PROMPT = PromptTemplate.from_template(
    """
You are a senior QA automation engineer. Generate a complete, runnable pytest + Playwright
(Python) test file for the Open Library website at https://openlibrary.org.

Requirements:
- Use `playwright.sync_api` (sync Playwright, NOT async).
- Use a pytest fixture named `page` that is provided automatically by pytest-playwright.
  Do NOT define your own `page` fixture — pytest-playwright provides it.
- Do NOT define any fixture named `base_url` — this name is reserved by pytest-playwright
  and will cause a ScopeMismatch error. Use a module-level constant instead:
  BASE_URL = "https://openlibrary.org"
- Use `expect` from `playwright.sync_api` for assertions.
- Use explicit waits: page.wait_for_selector(), expect(locator).to_be_visible(), etc.
  Do NOT use time.sleep() anywhere.

CONFIRMED WORKING SELECTORS (use these exactly — do not invent alternatives):
- Search input: input[name='q']
- Logo/header link: a.logoLink
- Search result items: li.searchResultItem
- First result link: li.searchResultItem a.results
- Book detail heading: h1.work-title
- Search results URL pattern: /search

- Include these exact test cases:
    1. Homepage loads: navigate to BASE_URL, verify the page title contains "Open Library"
       and the search input (input[name='q']) is visible.
    2. Search flow: type "Dune" into input[name='q'], press Enter, wait for URL to contain
       "/search", then assert at least one li.searchResultItem is visible.
    3. Book detail: navigate to https://openlibrary.org/search?q=Dune, wait for
       li.searchResultItem a.results, click the first one (.nth(0)), wait for URL to
       contain "/works/", then assert h1.work-title is visible.
    4. Navigation sanity: navigate to BASE_URL, verify a.logoLink is visible.

- Add a module-level docstring.
- Use explicit assert statements with descriptive messages where expect() is not used.
- Do NOT wrap output in markdown code fences. Output only raw Python code.

Generate the complete test file now.
"""
)


def generate_e2e_tests() -> str:
    """
    Invoke Groq via LangChain to generate Playwright E2E test source code.

    Returns:
        str: Raw Python source code for the generated test file.
    """
    chain = E2E_TEST_PROMPT | get_llm() | StrOutputParser()
    return chain.invoke({})
