"""
Gemini LLM configuration using .env
Uses gemini-flash-latest with latest LangChain syntax
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


def load_gemini():
    """
    Load Gemini Flash model securely from environment variables
    """

    # Load .env variables
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY not found in .env")

    # Latest Gemini Flash model
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0.3,
        google_api_key=api_key
    )

    return llm
