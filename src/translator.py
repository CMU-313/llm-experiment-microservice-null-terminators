import os
import re
from ollama import Client

# Configuration
MODEL_NAME = "mistral:7b"
OLLAMA_URL = os.getenv("OLLAMA_HOST", "localhost:11434")
client = Client(host=OLLAMA_URL)

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
Could you answer, in one English word, what language the input message is in? Don't provide any additional information.
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

    cleaned_translation = clean_response(llm_translation)
    cleaned_lang_detection = clean_response(llm_lang_detection)

    return (cleaned_lang_detection.lower() == "english", cleaned_translation)
