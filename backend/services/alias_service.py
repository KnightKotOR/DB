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
        return AliasResponse(message=f"Database alias created: database='{ar.database}', alias='{ar.alias}'")

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

    return AliasResponse(message=(
            f"Table alias created: database='{ar.database}', "
            f"table='{ar.table}', alias='{ar.alias}'"
        ))

def delete_alias(ar: AliasRequest) -> AliasResponse:
    """
    Deletes db/table alias
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Удаление alias БД
    if ar.table == "":
        # Проверка существования БД и alias
        cursor.execute(
            "SELECT db_alias FROM dbs WHERE db_name = %s;",
            (ar.database,)
        )
        row = cursor.fetchone()
        old_alias = row["db_alias"]

        if not row:
            raise HTTPException(status_code=404, detail="Database not found")

        if row["db_alias"] is None:
            raise HTTPException(status_code=400, detail="Alias does not exist")

        # Удаление alias
        cursor.execute(
            "UPDATE dbs SET db_alias = NULL WHERE db_name = %s;",
            (ar.database,)
        )
        conn.commit()

        cursor.close()
        conn.close()
        return AliasResponse(message=(
                f"Database alias deleted: database='{ar.database}', "
                f"old_alias='{old_alias}'"
            ))

    # Удаление alias таблицы
    # Проверка существования БД, таблицы и alias
    cursor.execute(
        "SELECT db_id FROM dbs WHERE db_name = %s;",
        (ar.database,)
    )
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Database not found")

    db_id = row["db_id"]

    cursor.execute(
        "SELECT table_id, table_alias FROM db_tables WHERE db_id = %s AND table_name = %s;",
        (db_id, ar.table)
    )
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Table not found")

    table_id = row["table_id"]
    table_alias = row["table_alias"]

    if table_alias is None:
        raise HTTPException(status_code=400, detail="Alias does not exist")

    # Удаление alias
    cursor.execute(
        "UPDATE db_tables SET table_alias = NULL WHERE table_id = %s;",
        (table_id,)
    )
    conn.commit()

    cursor.close()  
    conn.close()

    return AliasResponse(message=(
            f"Table alias deleted: database='{ar.database}', "
            f"table='{ar.table}', old_alias='{table_alias}'"
        ))
