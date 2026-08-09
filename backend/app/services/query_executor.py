from sqlalchemy import text
from sqlalchemy.orm import Session


def execute_query(db: Session, sql: str):
    result = db.execute(text(sql))

    rows = result.mappings().all()

    return [dict(row) for row in rows]