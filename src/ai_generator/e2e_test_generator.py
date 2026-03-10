"""
src/ai_generator/e2e_test_generator.py

Uses LangChain + Gemini to generate Playwright (Python) E2E test code
targeting the Open Library UI at https://openlibrary.org.

Coverage areas generated:
  - Homepage loads and key elements are visible
  - Search flow: enter query, submit, verify results page
  - Book detail navigation: click a result, verify title on detail page
  - Author page navigation from a book detail page
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
- Use `expect` from `playwright.sync_api` for assertions.
- Use explicit waits: page.wait_for_selector(), expect(locator).to_be_visible(), etc.
  Do NOT use time.sleep() anywhere.
- Include these exact test cases:
    1. Homepage loads: verify the page title contains "Open Library" and the search input is visible.
    2. Search flow: type "Dune" into the search bar, submit the form, and assert the results
       page URL contains "/search" and at least one result item is visible.
    3. Book detail: from search results for "Dune", click the first result link, then assert
       the detail page has a heading (h1) visible containing text.
    4. Navigation sanity: verify the site header/logo is visible on the homepage.
- Add a module-level docstring.
- Do NOT wrap output in markdown code fences. Output only raw Python code.

Generate the complete test file now.
"""
)


def generate_e2e_tests() -> str:
    """
    Invoke Gemini via LangChain to generate Playwright E2E test source code.

    Returns:
        str: Raw Python source code for the generated test file.
    """
    chain = E2E_TEST_PROMPT | get_llm() | StrOutputParser()
    return chain.invoke({})
