from utils.db import get_connection
from mysql.connector import Error, InterfaceError
from fastapi import HTTPException
from models.alias_model import AliasRequest, AliasResponse


def create_db_alias(name, alias):
    meta_conn = get_connection()
    meta_cursor = meta_conn.cursor(dictionary=True)

    alias_conn = get_connection("query_aliases")
    alias_cursor = alias_conn.cursor(dictionary=True)


    # Проверить, есть ли alias в query_aliases
    alias_cursor.execute(
        "SELECT db_meta_id, db_alias_name FROM db_aliases WHERE db_alias_name = %s;",
        (alias,)
    )

    # если есть запись в alias_db - смотрим на alias, если он null - обновляем, иначе - ошибка
    try:
        row = alias_cursor.fetchone()
        print(row)
        if row["db_alias_name"] is not None:
            raise HTTPException(status_code=400, detail="Alias already exists")
        else:
            alias_cursor.execute(
                "UPDATE db_aliases SET db_alias_name = %s WHERE db_meta_id = %s;",
                (alias, row["db_meta_id"],)
            )
            alias_conn.commit()

    # если нет такой базы в alias_db - лезем в meta_db, ищем базу по имени
    except TypeError:
        meta_cursor.execute(
            "SELECT db_id FROM dbs WHERE db_name = %s",
            (name, )
        )

        db_row = meta_cursor.fetchone()
        if db_row:
            alias_cursor.execute(
                "INSERT INTO db_aliases (db_meta_id, db_alias_name) VALUES (%s, %s);",
                (db_row["db_id"], alias, )
            )
            alias_conn.commit()
        else:
            raise HTTPException(status_code=404, detail="Database does not exist")

    meta_cursor.close()
    alias_cursor.close()
    meta_conn.close()
    alias_conn.close()


def create_alias(ar: AliasRequest) -> AliasResponse:
    """
    Creates db/table alias
    """

    # --Создание alias для БД--
    if ar.table == "":
        create_db_alias(ar.database, ar.alias)

        return AliasResponse(message=(
                f"Database alias created: database='{ar.database}', alias='{ar.alias}'"
            ))
    return AliasResponse(message=(
        f"Something went wrong"
    ))


    # # --Создание alias для таблицы БД--
    # meta_cursor.execute(
    #     "SELECT db_id FROM dbs WHERE db_name = %s OR db_alias = %s;",
    #     (ar.database,ar.database,)
    # )
    # row = meta_cursor.fetchone()
    # if not row:
    #     raise HTTPException(status_code=404, detail="Database not found")
    #
    # db_id = row["db_id"]
    #
    # # Поиск таблицы
    # meta_cursor.execute(
    #     "SELECT table_id, table_alias FROM db_tables WHERE db_id = %s AND table_name = %s;",
    #     (db_id, ar.table)
    # )
    # row = meta_cursor.fetchone()
    # if not row:
    #     raise HTTPException(status_code=404, detail="Table not found")
    #
    # table_id = row["table_id"]
    # table_alias = row["table_alias"]
    #
    # # Проверка существования alias таблицы
    # if table_alias:
    #     raise HTTPException(status_code=400, detail="Alias already exists")
    #
    # # Создание alias таблицы
    # meta_cursor.execute(
    #     "UPDATE db_tables SET table_alias = %s WHERE table_id = %s;",
    #     (ar.alias, table_id)
    # )
    # meta_conn.commit()
    #
    # meta_cursor.close()
    # meta_conn.close()
    #
    # return AliasResponse(message=(
    #         f"Table alias created: database='{ar.database}', "
    #         f"table='{ar.table}', alias='{ar.alias}'"
    #     ))

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
            "SELECT db_name, db_alias FROM dbs WHERE db_name = %s OR db_alias = %s;",
            (ar.database,ar.database,)
        )
        row = cursor.fetchone()
        db_name, old_alias = row["db_name"], row["db_alias"]

        if not old_alias:
            raise HTTPException(status_code=404, detail="Database not found")

        if old_alias is None:
            raise HTTPException(status_code=400, detail="Alias does not exist")

        # Удаление alias
        cursor.execute(
            "UPDATE dbs SET db_alias = NULL WHERE db_name = %s;",
            (db_name,)
        )
        conn.commit()

        cursor.close()
        conn.close()
        return AliasResponse(message=(
                f"Database alias deleted: database='{db_name}', "
                f"old_alias='{old_alias}'"
            ))

    # Удаление alias таблицы
    # Проверка существования БД, таблицы и alias
    cursor.execute(
        "SELECT db_name, db_id FROM dbs WHERE db_name = %s OR db_alias = %s;",
        (ar.database,ar.database,)
    )
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Database not found")

    db_id, db_name = row["db_id"], row["db_name"]

    cursor.execute(
        "SELECT table_id, table_alias, table_name FROM db_tables WHERE db_id = %s AND (table_name = %s OR table_alias = %s);",
        (db_id, ar.table, ar.table,)
    )
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Table not found")

    table_id = row["table_id"]
    table_alias = row["table_alias"]
    table_name = row["table_name"]

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
            f"Table alias deleted: database='{db_name}', "
            f"table='{table_name}', old_alias='{table_alias}'"
        ))
