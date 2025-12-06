from typing import List
from utils.db import get_connection
from models.db_model import DatabaseItem

def get_all_databases() -> List[DatabaseItem]:
    """Returns list of all databases from metadata_catalog.dbs."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT db_id, db_name FROM dbs ORDER BY db_name;")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [DatabaseItem(**row) for row in rows]

def get_database_by_id(db_id: int) -> DatabaseItem:
    """Returns database with specified id"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT db_id, db_name FROM dbs WHERE db_id = %s;", (db_id, ))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return DatabaseItem(**row)