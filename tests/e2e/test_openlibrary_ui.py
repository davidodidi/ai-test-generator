"""
tests/e2e/test_openlibrary_ui.py

Baseline Playwright E2E tests for the Open Library UI.
Target: https://openlibrary.org

These tests are hand-authored as the stable suite.
AI-generated versions (via scripts/generate_tests.py) will overwrite
this file -- this baseline exists so CI never has an empty test run.

Coverage:
  - Homepage load and key element visibility
  - Search flow: query submission and results page
  - Book detail navigation from search results
  - Header/logo navigation sanity
"""

import re
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
class TestHomepage:
    def test_homepage_title_contains_open_library(self, page: Page):
        page.goto("https://openlibrary.org")
        expect(page).to_have_title(re.compile("Open Library"))

    def test_search_input_is_visible_on_homepage(self, page: Page):
        page.goto("https://openlibrary.org")
        search_input = page.locator("input[name='q']")
        expect(search_input).to_be_visible()

    def test_header_logo_is_visible(self, page: Page):
        page.goto("https://openlibrary.org")
        logo = page.locator("a.logoLink, #header-logo, a[href='/'] img").first
        expect(logo).to_be_visible()


@pytest.mark.e2e
class TestSearchFlow:
    def test_search_for_dune_navigates_to_results(self, page: Page):
        page.goto("https://openlibrary.org")
        page.fill("input[name='q']", "Dune")
        page.press("input[name='q']", "Enter")
        page.wait_for_url("**/search**", timeout=30_000)
        assert "/search" in page.url, (
            f"Expected URL to contain '/search' after search, got: {page.url}"
        )

    def test_search_results_list_is_visible(self, page: Page):
        page.goto("https://openlibrary.org/search?q=Dune")
        results = page.locator("li.searchResultItem")
        results.first.wait_for(timeout=30_000)
        expect(results.first).to_be_visible()

    def test_search_results_contain_expected_keyword(self, page: Page):
        page.goto("https://openlibrary.org/search?q=Dune&title=Dune")
        page.wait_for_selector("li.searchResultItem", timeout=30_000)
        page_content = page.content()
        assert "Dune" in page_content, (
            "Expected 'Dune' to appear somewhere in search results page content"
        )


@pytest.mark.e2e
class TestBookDetailNavigation:
    def test_clicking_first_result_navigates_to_detail_page(self, page: Page):
        page.goto("https://openlibrary.org/search?q=Dune")
        page.wait_for_selector("li.searchResultItem a.results", timeout=30_000)
        first_link = page.locator("li.searchResultItem a.results").nth(0)
        first_link.click()
        page.wait_for_url("**/works/**", timeout=30_000)
        assert "/works/" in page.url, (
            f"Expected to navigate to a /works/ URL, got: {page.url}"
        )

    def test_book_detail_page_has_visible_heading(self, page: Page):
        page.goto("https://openlibrary.org/works/OL893415W/Dune")
        page.wait_for_selector("h1.work-title", state="attached", timeout=30_000)
        heading_text = page.locator("h1.work-title").nth(0).inner_text()
        assert len(heading_text.strip()) > 0, (
            "Expected h1.work-title on book detail page to have non-empty text"
        )
