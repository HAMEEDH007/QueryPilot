import re


def validate_sql(sql: str) -> bool:
    sql = sql.strip().lower()

    # Only allow SELECT queries
    if not sql.startswith("select"):
        return False

    # Block dangerous SQL operations
    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "replace",
        "attach",
        "detach",
    ]

    for keyword in forbidden_keywords:
        if re.search(rf"\b{keyword}\b", sql):
            return False

    return True