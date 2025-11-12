import os
import re

# `ollama` is an optional dependency at import time for tests. If it's not
# available (for example in CI or a developer machine without the runtime
# client), fall back to None and create a no-op client variable. The
# functions that perform LLM calls will fail if actually invoked, but
# unit tests typically monkeypatch those functions.
try:
    from ollama import Client
except Exception:
    Client = None

# Configuration
MODEL_NAME = "mistral:7b"
OLLAMA_URL = os.getenv("OLLAMA_HOST", "localhost:11434")
client = Client(host=OLLAMA_URL) if Client is not None else None

def clean_response(llm_response: str) -> str:
    match = re.search(r'<OUTPUT>(.*?)</OUTPUT>', llm_response, re.DOTALL)
    extracted_response = match.group(1).strip() if match else llm_response.strip()
    return extracted_response

def get_translation(post: str) -> str:
    context = """
I will give you an input message that is in a non-english language, enclosed in <INPUT></INPUT> tags.
I want you to translate the input message into English. If it is already in English, return it as is in <OUTPUT></OUTPUT> tags.
Enclose your answer in <OUTPUT></OUTPUT> tags.
If you don't know how to translate it, return the word the same message enclosed in <OUTPUT></OUTPUT> tags.
"""

    prompt = "<INPUT>" + post + "</INPUT>"

    response = client.chat(
        model=MODEL_NAME,  # model name
        messages=[
            {
                "role": "user",
                "content": context
            },
            {
                "role": "assistant",
                "content": "I understand. I will translate the message inside the <INPUT></INPUT> tags to English and give my answer in <OUTPUT></OUTPUT> tags. What is my first input message?"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return clean_response(response.message.content).strip()

def get_language(post: str) -> str:
    context = """
    I am going to give you an input message enclosed in <INPUT></INPUT> tags.
Could you answer, in one English word, what language the input message is in? If there is no language or more than one, return "unknown". Don't provide any additional information.
Enclose your answer in <OUTPUT></OUTPUT> tags. Return English if you don't know."""
    
    response = client.chat(
        model=MODEL_NAME,  # model name
        messages=[
            {
                "role": "user",
                "content": context
            },
            {
                "role": "assistant",
                "content": "I understand. I will detect what language the message inside the <INPUT></INPUT> tags is in, and give the English name of the language in <OUTPUT></OUTPUT> tags. What is my first input message?"
            },
            {
                "role": "user",
                "content": "<INPUT>" + post + "</INPUT>"
            }
        ]
    )
    return clean_response(response.message.content).strip()

def translate_content(content: str) -> tuple[bool, str]:
    llm_translation = get_translation(content).strip()
    llm_lang_detection = get_language(content).strip()
    # debug information kept intentionally for local runs
    print(f"LLM Language Detection: {llm_lang_detection}")

    cleaned_translation = clean_response(llm_translation)
    cleaned_lang_detection = clean_response(llm_lang_detection).strip()

    lang_lower = cleaned_lang_detection.lower()

    # If the LLM explicitly says the input is English, return it as English
    if lang_lower == "english":
        return (True, cleaned_translation)

    # If language detection failed, returned an unknown value, or indicates
    # multiple languages, don't trust the translation; return the original
    # content unchanged.
    multiple_indicators = [",", ";", "/", "&", " and ", " & ", " and/or", "mixed", "multiple"]
    if (not lang_lower) or "unknown" in lang_lower or "emoji" in lang_lower or any(ind in lang_lower for ind in multiple_indicators):
        return (False,  content)

    # Otherwise we have a single non-English language; return the translation
    return (False, cleaned_translation)
