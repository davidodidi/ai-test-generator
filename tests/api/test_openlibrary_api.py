"""
tests/api/test_openlibrary_api.py

Baseline API integration tests for the Open Library REST API.
Target: https://openlibrary.org/dev/docs/api

These tests are hand-authored as the stable suite.
AI-generated versions (via scripts/generate_tests.py) will overwrite
this file — this baseline exists so CI never has an empty test run.

Coverage:
  - Happy path: book search and work detail
  - Validation: graceful handling of edge-case queries
  - Schema: required keys present in responses
  - Response time: latency under acceptable threshold
"""

import time
import pytest
import requests

BASE_URL = "https://openlibrary.org"
KNOWN_WORK_OLID = "OL45804W"  # "Fantastic Mr Fox" by Roald Dahl
RESPONSE_TIME_THRESHOLD_SECONDS = 5


@pytest.mark.api
class TestBookSearchHappyPath:
    def test_search_by_title_returns_200(self):
        response = requests.get(f"{BASE_URL}/search.json", params={"title": "Dune"})
        assert response.status_code == 200, (
            f"Expected HTTP 200 for valid title search, got {response.status_code}"
        )

    def test_search_by_title_returns_results(self):
        response = requests.get(f"{BASE_URL}/search.json", params={"title": "Dune"})
        data = response.json()
        assert data.get("numFound", 0) > 0, (
            "Expected at least one result for 'Dune', got numFound=0"
        )

    def test_search_by_author_returns_200(self):
        response = requests.get(
            f"{BASE_URL}/search.json", params={"author": "Frank Herbert"}
        )
        assert response.status_code == 200, (
            f"Expected HTTP 200 for author search, got {response.status_code}"
        )


@pytest.mark.api
class TestWorkDetailHappyPath:
    def test_known_work_returns_200(self):
        response = requests.get(f"{BASE_URL}/works/{KNOWN_WORK_OLID}.json")
        assert response.status_code == 200, (
            f"Expected HTTP 200 for known OLID {KNOWN_WORK_OLID}, "
            f"got {response.status_code}"
        )

    def test_known_work_has_expected_title(self):
        response = requests.get(f"{BASE_URL}/works/{KNOWN_WORK_OLID}.json")
        data = response.json()
        title = data.get("title", "")
        assert "Fantastic Mr" in title, (
            f"Expected title to contain 'Fantastic Mr', got: '{title}'"
        )


@pytest.mark.api
class TestSearchValidation:
    def test_empty_title_query_returns_500(self):
        """
        Open Library returns HTTP 500 for an empty title= parameter.
        This is a confirmed server-side bug in their API. We assert the
        exact observed status code so that if Open Library fixes this
        (returning 200 or 400), the test fails and gets consciously updated
        to reflect the new correct behaviour.
        """
        response = requests.get(f"{BASE_URL}/search.json", params={"title": ""})
        assert response.status_code == 500, (
            f"Expected HTTP 500 for empty title query (known Open Library API bug), "
            f"got {response.status_code}"
        )

    def test_nonexistent_work_olid_returns_404(self):
        response = requests.get(f"{BASE_URL}/works/OL00000000INVALID.json")
        assert response.status_code == 404, (
            f"Expected HTTP 404 for invalid OLID, got {response.status_code}"
        )


@pytest.mark.api
class TestSearchSchema:
    def test_search_response_has_required_top_level_keys(self):
        response = requests.get(f"{BASE_URL}/search.json", params={"title": "1984"})
        data = response.json()
        required_keys = {"numFound", "docs"}
        missing = required_keys - data.keys()
        assert not missing, (
            f"Search response missing required keys: {missing}"
        )

    def test_search_result_doc_has_required_keys(self):
        response = requests.get(f"{BASE_URL}/search.json", params={"title": "1984"})
        data = response.json()
        docs = data.get("docs", [])
        assert len(docs) > 0, "Expected at least one doc in search results for '1984'"
        first_doc = docs[0]
        required_keys = {"title", "key"}
        missing = required_keys - first_doc.keys()
        assert not missing, (
            f"First result doc missing required keys: {missing}"
        )

    def test_work_detail_response_has_required_keys(self):
        response = requests.get(f"{BASE_URL}/works/{KNOWN_WORK_OLID}.json")
        data = response.json()
        required_keys = {"title", "key"}
        missing = required_keys - data.keys()
        assert not missing, (
            f"Work detail response missing required keys: {missing}"
        )


@pytest.mark.api
class TestResponseTime:
    def test_search_endpoint_responds_within_threshold(self):
        start = time.monotonic()
        requests.get(f"{BASE_URL}/search.json", params={"title": "Python"})
        elapsed = time.monotonic() - start
        assert elapsed < RESPONSE_TIME_THRESHOLD_SECONDS, (
            f"Search endpoint took {elapsed:.2f}s — exceeded threshold of "
            f"{RESPONSE_TIME_THRESHOLD_SECONDS}s"
        )

    def test_work_detail_endpoint_responds_within_threshold(self):
        start = time.monotonic()
        requests.get(f"{BASE_URL}/works/{KNOWN_WORK_OLID}.json")
        elapsed = time.monotonic() - start
        assert elapsed < RESPONSE_TIME_THRESHOLD_SECONDS, (
            f"Work detail endpoint took {elapsed:.2f}s — exceeded threshold of "
            f"{RESPONSE_TIME_THRESHOLD_SECONDS}s"
        )
