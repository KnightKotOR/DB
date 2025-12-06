from utils.db import get_connection
from mysql.connector import Error
from fastapi import HTTPException
from models.query_model import QueryRequest, QueryResponse


def execute_query(qr: QueryRequest) -> QueryResponse:
    """
    Returns response from the db
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    db_name = ""
    db_id = 0
    
    try:
        cursor.execute(
        """
        SELECT db_name, db_id
        FROM dbs
        WHERE db_name = %s;
        """,
        (qr.database,)
        )
        result = cursor.fetchone()
        db_name, db_id = result['db_name'], result['db_id']
    except TypeError as e:
        try:
            cursor.execute(
            """
            SELECT db_name, db_id
            FROM dbs
            WHERE db_alias = %s;
            """,
            (qr.database,)
            )
            result = cursor.fetchone()
            db_name, db_id = result['db_name'], result['db_id']
        except Error as e:
            raise HTTPException(status_code=404, detail=str(e))

    try:
        cursor.execute(
        """
        SELECT table_name
        FROM db_tables
        WHERE table_name = %s AND db_id = %s;
        """,
        (qr.table, db_id)
        )
        table_name = cursor.fetchone()['table_name']
    except TypeError as e:
        try:
            cursor.execute(
            """
            SELECT table_name
            FROM db_tables
            WHERE table_alias = %s AND db_id = %s;
            """,
            (qr.table, db_id)
            )
            table_name = cursor.fetchone()['table_name']
        except:
            raise HTTPException(status_code=404)

    cursor.close()
    conn.close()

    target_conn = get_connection(db_name)
    target_cursor = target_conn.cursor(dictionary=True)

    print(qr.column, type(qr.column))
    print(table_name, type(table_name))

    try:
        query = f"""
        SELECT `{qr.column}`
        FROM `{table_name}`;
        """
        target_cursor.execute(query)
        res = target_cursor.fetchall()
        print(res)
    except Error as e:
        raise HTTPException(status_code=404, detail=str(e))

    # if no database then table_count = 0
    return QueryResponse(column=qr.column, info=[r[qr.column] for r in res])

