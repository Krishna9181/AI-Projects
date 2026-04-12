from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

_ENV_PATH = Path(__file__).resolve().parent / ".env"


def main():
    load_dotenv(_ENV_PATH)
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4o-mini",
        input="Tell me a fun fact about data engineering",
    )
    print(response.output)


if __name__ == "__main__":
    main()
