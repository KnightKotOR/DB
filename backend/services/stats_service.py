from utils.db import get_connection
from models.stats_model import StatCount

def get_table_count_by_db(db_id: int) -> StatCount:
    """
    Returns number of tables in database with provided db_id.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT COUNT(*) AS table_count
        FROM db_tables
        WHERE db_id = %s;
        """,
        (db_id,)
    )

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    # if no database then table_count = 0
    count = row["table_count"] if row and "table_count" in row else 0
    return StatCount(db_id=db_id, count=count)

def get_column_count_by_db(db_id: int):
    """
    Returns the number of columns in database with provided db_id.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT COUNT(*) AS column_count
        FROM db_columns
        JOIN db_tables ON db_columns.table_id = db_tables.table_id
        WHERE db_tables.db_id = %s;
        """,
        (db_id,)
    )

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    count = row["column_count"] if row and "column_count" in row else 0
    return StatCount(db_id=db_id, count=count)

def get_primary_key_count_by_db(db_id: int):
    """
    Returns the number of primary keys (constraints) in database with provided db_id.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT COUNT(*) AS key_count
        FROM constraints
        JOIN db_tables ON constraints.table_id = db_tables.table_id
        WHERE constraints.type = "PRIMARY" AND db_tables.db_id = %s;
        """,
        (db_id,)
    )

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    count = row["key_count"] if row and "key_count" in row else 0
    return StatCount(db_id=db_id, count=count)

def get_foreign_key_count_by_db(db_id: int):
    """
    Returns the number of foreign keys (constraints) in database with provided db_id.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT COUNT(*) AS key_count
        FROM constraints
        JOIN db_tables ON constraints.table_id = db_tables.table_id
        WHERE constraints.type = "FOREIGN" AND db_tables.db_id = %s;
        """,
        (db_id,)
    )

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    count = row["key_count"] if row and "key_count" in row else 0
    return StatCount(db_id=db_id, count=count)

def get_unique_key_count_by_db(db_id: int):
    """
    Returns the number of unique keys (constraints) in database with provided db_id.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT COUNT(*) AS key_count
        FROM constraints
        JOIN db_tables ON constraints.table_id = db_tables.table_id
        WHERE constraints.type = "UNIQUE" AND db_tables.db_id = %s;
        """,
        (db_id,)
    )

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    count = row["key_count"] if row and "key_count" in row else 0
    return StatCount(db_id=db_id, count=count)

def get_record_count_by_db(db_id: int) -> StatCount:
    """
    Returns the total number of records (rows) across all tables in the database with the provided db_id.
    """
    # get db name
    meta_conn = get_connection()
    meta_cursor = meta_conn.cursor(dictionary=True)

    meta_cursor.execute("SELECT db_name FROM dbs WHERE db_id = %s;", (db_id,))
    db_row = meta_cursor.fetchone()

    if not db_row:
        meta_cursor.close()
        meta_conn.close()
        return StatCount(db_id=db_id, count=0)

    db_name = db_row["db_name"]

    # get list of tables
    meta_cursor.execute("SELECT table_name FROM db_tables WHERE db_id = %s;", (db_id,))
    tables = [row["table_name"] for row in meta_cursor.fetchall()]

    meta_cursor.close()
    meta_conn.close()

    if not tables:
        return StatCount(db_id=db_id, count=0)

    # connect to db and count
    total_records = 0
    db_conn = get_connection(db_name)
    db_cursor = db_conn.cursor()

    for table in tables:
        try:
            db_cursor.execute(f"SELECT COUNT(*) FROM `{table}`;")
            (count,) = db_cursor.fetchone()
            total_records += count
        except Exception as e:
            # ignore if no table/access
            print(f"Warning: couldn't count rows in table {table}: {e}")
            continue

    db_cursor.close()
    db_conn.close()

    return StatCount(db_id=db_id, count=total_records)