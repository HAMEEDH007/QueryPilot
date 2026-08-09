# QueryPilot

**AI-powered natural language interface for SQL databases.**

QueryPilot lets you query a SQLite database using plain English. Type a question, and the API converts it into a safe SQL query using a local LLM (via LM Studio), executes it, and returns the results — no SQL knowledge required.

---

## Features

- **Natural language to SQL** — Converts plain English questions into valid SQLite `SELECT` queries using an LLM.
- **Local LLM support** — Integrates with [LM Studio](https://lmstudio.ai/) via an OpenAI-compatible API, so your data never leaves your machine.
- **SQL safety validation** — Every generated query is validated before execution. Only `SELECT` statements are allowed; dangerous operations (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `CREATE`, `REPLACE`, `ATTACH`, `DETACH`) are blocked.
- **REST API** — Built with [FastAPI](https://fastapi.tiangolo.com/), providing fast, async endpoints with automatic interactive docs.
- **SQLite database** — Lightweight, file-based database with [SQLAlchemy](https://www.sqlalchemy.org/) ORM. No external database server needed.
- **Auto schema creation** — Database tables are created automatically on startup from SQLAlchemy models.
- **Seed data support** — Includes a seed script to populate the database with sample student records for testing.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite |
| AI / LLM | LM Studio (OpenAI-compatible) |
| LLM client | openai Python SDK |
| Validation | Pydantic |
| Server | Uvicorn |

---

## Project Structure

```
QueryPilot/
└── backend/
    ├── app/
    │   ├── main.py               # FastAPI app and route definitions
    │   ├── database.py           # SQLAlchemy engine and session setup
    │   ├── models.py             # Database models (Student)
    │   ├── schemas.py            # Pydantic schemas
    │   ├── seed.py               # Database seeding script
    │   ├── ai/
    │   │   └── text_to_sql.py    # AI module (text-to-SQL logic)
    │   └── services/
    │       ├── sql_generator.py  # Calls LLM to generate SQL from a question
    │       ├── sql_validator.py  # Validates SQL for safety before execution
    │       └── query_executor.py # Executes the SQL query against the database
    ├── requirements.txt
    ├── .env                      # Environment variables (LM Studio config)
    └── querypilot.db             # SQLite database file
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- [LM Studio](https://lmstudio.ai/) running locally with a model loaded and the local server enabled

### 1. Clone the repository

```bash
git clone https://github.com/your-username/QueryPilot.git
cd QueryPilot/backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv myenv
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the `backend/` directory (or update the existing one):

```env
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_API_KEY=lm-studio
LM_STUDIO_MODEL=your-model-name
```

Replace `your-model-name` with the exact model identifier shown in LM Studio.

### 5. Seed the database (optional)

```bash
python -m app.seed
```

### 6. Start the API server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## API Endpoints

### `GET /`
Health check. Returns a confirmation that the API is running.

**Response:**
```json
{ "message": "QueryPilot API is running" }
```

---

### `GET /students`
Returns all student records from the database.

**Response:**
```json
[
  { "id": 1, "name": "Alice", "age": 20, "marks": 88 },
  { "id": 2, "name": "Bob",   "age": 22, "marks": 74 }
]
```

---

### `POST /query`
Accepts a natural language question, generates a SQL query via the LLM, validates it, executes it, and returns the results.

**Request body:**
```json
{ "question": "Who are the top 3 students by marks?" }
```

**Response:**
```json
{
  "question": "Who are the top 3 students by marks?",
  "sql": "SELECT * FROM students ORDER BY marks DESC LIMIT 3;",
  "results": [
    { "id": 5, "name": "Sara", "age": 21, "marks": 95 },
    { "id": 1, "name": "Alice", "age": 20, "marks": 88 },
    { "id": 3, "name": "Carol", "age": 23, "marks": 82 }
  ]
}
```

If the generated SQL fails validation, the response includes an error instead of results:
```json
{
  "question": "...",
  "sql": "...",
  "error": "Unsafe SQL query rejected"
}
```

---

## Interactive API Docs

FastAPI provides built-in docs at:

- **Swagger UI** → `http://localhost:8000/docs`
- **ReDoc** → `http://localhost:8000/redoc`

---

## Database Schema

### `students` table

| Column | Type    | Description         |
|--------|---------|---------------------|
| id     | INTEGER | Primary key         |
| name   | STRING  | Student's full name |
| age    | INTEGER | Student's age       |
| marks  | INTEGER | Student's marks     |

---

## Example Questions You Can Ask

- `"Show all students"`
- `"Who has the highest marks?"`
- `"List students older than 20"`
- `"How many students scored more than 80?"`
- `"Show students sorted by age"`

---

## Security

- Only `SELECT` queries are permitted. The validator explicitly blocks all write and destructive SQL operations.
- The LLM prompt instructs the model to generate only `SELECT` queries, and the validator enforces this as a second layer of protection.
- The LLM runs locally via LM Studio — no data is sent to external APIs.
