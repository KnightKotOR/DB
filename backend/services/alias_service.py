from utils.db import get_connection
from mysql.connector import Error
from fastapi import HTTPException
from models.alias_model import AliasRequest, AliasResponse


def create_alias(ar: AliasRequest) -> AliasResponse:
    """
    Creates db/table alias
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Создание alias для БД
    if ar.table == "":
        # Проверить, есть ли alias
        cursor.execute(
            "SELECT db_alias FROM dbs WHERE db_name = %s;",
            (ar.database,)
        )
        row = cursor.fetchone()

        if row and row["db_alias"] is not None:
            raise HTTPException(status_code=400, detail="Alias already exists")

        # Создать alias БД
        cursor.execute(
            "UPDATE dbs SET db_alias = %s WHERE db_name = %s;",
            (ar.alias, ar.database)
        )
        conn.commit()

        cursor.close()
        conn.close()
        return AliasResponse(message="OK")

    # Создание alias для таблицы БД
    cursor.execute(
        "SELECT db_id FROM dbs WHERE db_name = %s;",
        (ar.database,)
    )
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Database not found")

    db_id = row["db_id"]

    # Поиск таблицы
    cursor.execute(
        "SELECT table_id, table_alias FROM db_tables WHERE db_id = %s AND table_name = %s;",
        (db_id, ar.table)
    )
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Table not found")

    table_id = row["table_id"]
    table_alias = row["table_alias"]

    # Проверка существования alias таблицы
    if table_alias:
        raise HTTPException(status_code=400, detail="Alias already exists")

    # Создание alias таблицы
    cursor.execute(
        "UPDATE db_tables SET table_alias = %s WHERE table_id = %s;",
        (ar.alias, table_id)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return AliasResponse(message="OK")
