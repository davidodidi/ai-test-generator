"""
src/ai_generator/gemini_client.py

LangChain wrapper around Groq (free tier).
Provides a single reusable LLM instance for all generators.

Groq runs LLaMA 3 with extremely fast inference and a generous free tier
(14,400 requests/day, 30 requests/minute) — well within CI usage.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_llm() -> ChatGroq:
    """
    Return a configured LangChain ChatGroq instance.

    Uses llama-3.3-70b-versatile on Groq's free tier.
    Temperature 0 ensures deterministic, consistent test output.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. "
            "Copy .env.example to .env and add your free key from "
            "https://console.groq.com/keys"
        )

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=api_key,
        temperature=0,
        max_retries=0,
    )
