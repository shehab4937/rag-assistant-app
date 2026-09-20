import os

import requests
from dotenv import load_dotenv


load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")


def ask_backend(question: str):
    response = requests.post(
        f"{API_BASE_URL}/query",
        json={
            "question": question
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()
