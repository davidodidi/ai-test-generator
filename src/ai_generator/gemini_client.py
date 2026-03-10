"""
src/ai_generator/gemini_client.py

LangChain wrapper around Google Gemini (free tier).
Provides a single reusable LLM instance for all generators.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm() -> ChatGoogleGenerativeAI:
    """
    Return a configured LangChain ChatGoogleGenerativeAI instance.

    Uses gemini-1.5-flash — the free-tier model.
    Temperature 0 ensures deterministic, consistent test output.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY is not set. "
            "Copy .env.example to .env and add your key from "
            "https://makersuite.google.com/app/apikey"
        )

    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0,
    )
