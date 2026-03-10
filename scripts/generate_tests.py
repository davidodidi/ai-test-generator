"""
scripts/generate_tests.py

CLI entrypoint. Calls Gemini via LangChain to (re)generate test files
and writes them to tests/api/ and tests/e2e/.

Usage:
    python scripts/generate_tests.py --api     # regenerate API tests only
    python scripts/generate_tests.py --e2e     # regenerate E2E tests only
    python scripts/generate_tests.py           # regenerate both
"""

import argparse
import sys
from pathlib import Path

# Allow imports from src/ regardless of working directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ai_generator.api_test_generator import generate_api_tests
from ai_generator.e2e_test_generator import generate_e2e_tests

API_OUTPUT = Path("tests/api/test_openlibrary_api.py")
E2E_OUTPUT = Path("tests/e2e/test_openlibrary_ui.py")


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✅ Written: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Test Generator — Open Library")
    parser.add_argument("--api", action="store_true", help="Generate API tests")
    parser.add_argument("--e2e", action="store_true", help="Generate E2E tests")
    args = parser.parse_args()

    # Default: run both if neither flag provided
    run_api = args.api or not (args.api or args.e2e)
    run_e2e = args.e2e or not (args.api or args.e2e)

    if run_api:
        print("⚙️  Generating API tests via Gemini...")
        write_file(API_OUTPUT, generate_api_tests())

    if run_e2e:
        print("⚙️  Generating E2E tests via Gemini...")
        write_file(E2E_OUTPUT, generate_e2e_tests())

    print("\n🎉 Done. Run tests with: pytest")


if __name__ == "__main__":
    main()
