from utils.db import get_connection
from mysql.connector import Error
from fastapi import HTTPException
from models.query_model import QueryRequest, QueryResponse


def execute_query(qr: QueryRequest) -> QueryResponse:
    """
    Returns response from the db
    """
    db_name = qr.database
    table_name = qr.table
    column_name = qr.column

    meta_conn = get_connection()
    meta_cursor = meta_conn.cursor(dictionary=True)

    alias_conn = get_connection("query_aliases")
    alias_cursor = alias_conn.cursor(dictionary=True)

    # getting true db_name
    try:
        meta_cursor.execute(
        """
        SELECT db_name, db_id
        FROM dbs
        WHERE db_name = %s;
        """,
        (qr.database,)
        )
        result = meta_cursor.fetchone()
        db_name, db_id = result['db_name'], result['db_id']
    except TypeError:
        try:
            alias_cursor.execute(
            """
            SELECT db_meta_id
            FROM db_aliases
            WHERE db_alias_name = %s;
            """,
            (qr.database,)
            )
            result = alias_cursor.fetchone()
            db_id = result['db_meta_id']

            meta_cursor.execute("SELECT db_name FROM dbs WHERE db_id = %s", (db_id, ))
            db_name = meta_cursor.fetchone()["db_name"]

        except TypeError:
            raise HTTPException(status_code=404, detail=f"Database '{qr.database}' does not exist")

    # getting true table name
    try:
        meta_cursor.execute(
        """
        SELECT table_id, table_name
        FROM db_tables
        WHERE table_name = %s AND db_id = %s;
        """,
        (qr.table, db_id)
        )
        row = meta_cursor.fetchone()
        print("table row: ", row)
        table_id, table_name = row['table_id'], row['table_name']

    except TypeError:
        try:
            alias_cursor.execute(
            """
            SELECT table_meta_id
            FROM table_aliases
            WHERE table_alias_name = %s;
            """,
            (qr.table, )
            )
            row = alias_cursor.fetchone()
            table_id = row['table_meta_id']

            meta_cursor.execute(
                """
                SELECT table_name
                FROM db_tables
                WHERE table_id = %s AND db_id = %s;
                """,
                (table_id, db_id, )
            )
            table_name = meta_cursor.fetchone()['table_name']

        except:
            raise HTTPException(status_code=404, detail=f"Table '{qr.table}' does not exist")

    # getting true column name
    try:
        meta_cursor.execute(
            """
            SELECT column_name
            FROM db_columns AS c
            WHERE column_name = %s AND table_id = %s;
            """,
            (qr.column, table_id)
        )
        column_name = meta_cursor.fetchone()['column_name']
    except TypeError:
        try:
            alias_cursor.execute(
                """
                SELECT column_meta_id
                FROM column_aliases
                WHERE column_alias_name = %s;
                """,
                (qr.column, )
            )
            column_id = alias_cursor.fetchone()['column_meta_id']

            meta_cursor.execute(
                """
                SELECT column_name
                FROM db_columns
                WHERE column_id = %s AND table_id = %s;
                """,
                (column_id, table_id, )
            )
            column_name = meta_cursor.fetchone()['column_name']

        except:
            raise HTTPException(status_code=404, detail=f"Column '{qr.column}' does not exist")

    meta_cursor.close()
    meta_conn.close()

    alias_cursor.close()
    alias_conn.close()

    target_conn = get_connection(db_name)
    target_cursor = target_conn.cursor(dictionary=True)

    try:
        query = f"""
        SELECT `{column_name}`
        FROM `{table_name}`;
        """
        target_cursor.execute(query)
        res = target_cursor.fetchall()
    except Error as e:
        raise HTTPException(status_code=404, detail=str(e))

    # if no database then table_count = 0
    return QueryResponse(column=column_name, info=[r[column_name] for r in res])
