import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("LM_STUDIO_BASE_URL"),
    api_key=os.getenv("LM_STUDIO_API_KEY")
)

MODEL_NAME = os.getenv("LM_STUDIO_MODEL")


def generate_sql(question: str) -> str:

    schema = """
    Table: students

    Columns:
    - id INTEGER
    - name STRING
    - age INTEGER
    - marks INTEGER
    """

    prompt = f"""
You are a SQL query generator.

Convert the user's natural language question into a SQLite SQL query.

Database schema:
{schema}

Rules:
- Generate only SQL.
- Do not use markdown.
- Only generate SELECT queries.
- Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE.
- Use only the tables and columns provided in the schema.

User question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()