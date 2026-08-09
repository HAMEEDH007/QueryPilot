from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

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