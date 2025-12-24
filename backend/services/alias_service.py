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
            alias_cursor.execute("SELECT db_meta_id "
                                 "FROM db_aliases "
                                 "WHERE db_meta_id = %s",
                                 (db_row["db_id"], ) )

            if alias_cursor.fetchone():
                raise HTTPException(status_code=400, detail="Database already has alias")

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



def create_table_alias(database, name, alias):
    meta_conn = get_connection()
    meta_cursor = meta_conn.cursor(dictionary=True)

    alias_conn = get_connection("query_aliases")
    alias_cursor = alias_conn.cursor(dictionary=True)

    # Проверить, есть ли alias в query_aliases
    alias_cursor.execute(
        "SELECT table_meta_id, table_alias_name FROM table_aliases WHERE table_alias_name = %s;",
        (alias,)
    )

    # если есть запись в alias_table - смотрим на alias, если он null - обновляем, иначе - ошибка
    try:
        row = alias_cursor.fetchone()
        if row["table_alias_name"] is not None:
            raise HTTPException(status_code=400, detail="Alias already exists")
        else:
            alias_cursor.execute(
                "UPDATE table_aliases SET table_alias_name = %s WHERE table_meta_id = %s;",
                (alias, row["table_meta_id"],)
            )
            alias_conn.commit()

    # если нет такой таблицы в alias_db - лезем в meta, ищем таблицу по имени и имени базы
    except TypeError:
        meta_cursor.execute(
            "SELECT t.table_id FROM db_tables AS t "
            "JOIN dbs ON dbs.db_id = t.db_id "
            "WHERE t.table_name = %s AND dbs.db_name = %s;",
            (name, database, )
        )

        db_row = meta_cursor.fetchone()
        if db_row:
            alias_cursor.execute("SELECT table_meta_id "
                                 "FROM table_aliases "
                                 "WHERE table_meta_id = %s",
                                 (db_row["table_id"], ) )

            if alias_cursor.fetchone():
                raise HTTPException(status_code=400, detail="Column already has alias")

            alias_cursor.execute(
                "INSERT INTO table_aliases (table_meta_id, table_alias_name) VALUES (%s, %s);",
                (db_row["table_id"], alias, )
            )
            alias_conn.commit()
        else:
            raise HTTPException(status_code=404, detail="Table does not exist")

    meta_cursor.close()
    alias_cursor.close()
    meta_conn.close()
    alias_conn.close()


def create_column_alias(database, table, name, alias):
    meta_conn = get_connection()
    meta_cursor = meta_conn.cursor(dictionary=True)

    alias_conn = get_connection("query_aliases")
    alias_cursor = alias_conn.cursor(dictionary=True)

    # Проверить, есть ли alias в query_aliases
    alias_cursor.execute(
        "SELECT column_meta_id, column_alias_name FROM column_aliases WHERE column_alias_name = %s;",
        (alias,)
    )

    # если есть запись в alias_column - смотрим на alias, если он null - обновляем, иначе - ошибка
    try:
        row = alias_cursor.fetchone()
        if row["column_alias_name"] is not None:
            raise HTTPException(status_code=400, detail="Alias already exists")
        else:
            alias_cursor.execute(
                "UPDATE column_aliases SET column_alias_name = %s WHERE column_meta_id = %s;",
                (alias, row["column_meta_id"],)
            )
            alias_conn.commit()

    # если нет такой колонки в alias_db - лезем в meta, ищем таблицу по имени и имени базы
    except TypeError:
        meta_cursor.execute(
            "SELECT c.column_id FROM db_columns AS c "
            "JOIN db_tables AS t ON t.table_id = c.table_id "
            "JOIN dbs ON dbs.db_id = t.db_id "
            "WHERE c.column_name = %s AND t.table_name = %s AND dbs.db_name = %s;",
            (name, table, database, )
        )

        db_row = meta_cursor.fetchone()
        if db_row:
            alias_cursor.execute("SELECT column_meta_id "
                                 "FROM column_aliases "
                                 "WHERE column_meta_id = %s",
                                 (db_row["column_id"], ) )

            if alias_cursor.fetchone():
                raise HTTPException(status_code=400, detail="Column already has alias")

            alias_cursor.execute(
                "INSERT INTO column_aliases (column_meta_id, column_alias_name) VALUES (%s, %s);",
                (db_row["column_id"], alias, )
            )
            alias_conn.commit()
        else:
            raise HTTPException(status_code=404, detail="Column does not exist")

    meta_cursor.close()
    alias_cursor.close()
    meta_conn.close()
    alias_conn.close()

def create_alias(ar: AliasRequest) -> AliasResponse:
    """
    Creates db/table alias
    """
    if ar.database != "" and ar.table != "" and ar.column != "":
        create_column_alias(ar.database, ar.table, ar.column, ar.alias)
        return AliasResponse(message=(
            f"Column alias created: database='{ar.database}', table='{ar.table}', column='{ar.column}' alias='{ar.alias}'"
        ))

    # --Создание alias для БД--
    if ar.table == "" and ar.column == "":
        create_db_alias(ar.database, ar.alias)
        return AliasResponse(message=(
            f"Database alias created: database='{ar.database}', alias='{ar.alias}'"
        ))

    elif ar.column == "":
        create_table_alias(ar.database, ar.table, ar.alias)
        return AliasResponse(message=(
            f"Table alias created: database='{ar.database}', table='{ar.table}', alias='{ar.alias}'"
        ))

    else:
        return AliasResponse(message=(
            f"Please specify database, table and column correctly"
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
