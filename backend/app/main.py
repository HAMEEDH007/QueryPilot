from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .services.sql_generator import generate_sql
from .services.query_executor import execute_query
from .services.sql_validator import validate_sql

from .database import engine, SessionLocal, Base
from .models import Student

app = FastAPI(
    title="QueryPilot",
    description="AI-powered natural language to SQL query system",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "QueryPilot API is running"
    }


@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()

    return students

class QueryRequest(BaseModel):
    question: str


@app.post("/query")
def query_database(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    sql = generate_sql(request.question)

    if not validate_sql(sql):
        return {
            "question": request.question,
            "sql": sql,
            "error": "Unsafe SQL query rejected"
        }

    results = execute_query(db, sql)

    return {
        "question": request.question,
        "sql": sql,
        "results": results
    }