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


def delete_table_alias(database, name):
    meta_conn = get_connection()
    meta_cursor = meta_conn.cursor(dictionary=True)

    alias_conn = get_connection("query_aliases")
    alias_cursor = alias_conn.cursor(dictionary=True)

    meta_cursor.execute(
        "SELECT table_id FROM db_tables AS t "
        "JOIN dbs ON t.db_id = dbs.db_id "
        "WHERE dbs.db_name = %s AND t.table_name = %s;",
        (database, name, ))

    # если alias есть - удаляем
    try:
        row = meta_cursor.fetchone()
        if row["table_id"] is not None:
            alias_cursor.execute("SELECT table_meta_id FROM table_aliases WHERE table_meta_id = %s", (row["table_id"], ))
            if alias_cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail=f"Table '{name}' does not have alias")

            alias_cursor.execute("DELETE FROM table_aliases WHERE table_meta_id = %s", (row["table_id"], ))
            alias_conn.commit()

    # если нет - выкидываем ошибку
    except TypeError:
        raise HTTPException(status_code=404, detail=f"Table '{name}' does not exist")

    meta_cursor.close()
    alias_cursor.close()
    meta_conn.close()
    alias_conn.close()

def delete_database_alias(name):
    meta_conn = get_connection()
    meta_cursor = meta_conn.cursor(dictionary=True)

    alias_conn = get_connection("query_aliases")
    alias_cursor = alias_conn.cursor(dictionary=True)

    meta_cursor.execute(
        "SELECT db_id FROM dbs WHERE db_name = %s;",
        (name, ))

    # если alias есть - удаляем
    try:
        row = meta_cursor.fetchone()
        if row["db_id"] is not None:
            alias_cursor.execute("SELECT db_meta_id FROM db_aliases WHERE db_meta_id = %s", (row["db_id"], ))
            if not alias_cursor.fetchall():
                raise HTTPException(status_code=404, detail=f"Database '{name}' does not have alias")

            alias_cursor.execute("DELETE FROM db_aliases WHERE db_meta_id = %s", (row["db_id"], ))
            alias_conn.commit()

    # если нет - выкидываем ошибку
    except TypeError:
        raise HTTPException(status_code=404, detail=f"Database '{name}' does not exist")

    meta_cursor.close()
    alias_cursor.close()
    meta_conn.close()
    alias_conn.close()


def delete_column_alias(database, table, name):
    meta_conn = get_connection()
    meta_cursor = meta_conn.cursor(dictionary=True)

    alias_conn = get_connection("query_aliases")
    alias_cursor = alias_conn.cursor(dictionary=True)

    meta_cursor.execute(
        "SELECT c.column_id FROM db_columns AS c "
        "JOIN db_tables as t ON c.table_id = t.table_id "
        "JOIN dbs ON t.db_id = dbs.db_id "
        "WHERE dbs.db_name = %s AND t.table_name = %s AND c.column_name = %s;",
        (database, table, name, ))
    # если alias есть - удаляем
    try:
        row = meta_cursor.fetchone()
        if row["column_id"] is not None:
            alias_cursor.execute("SELECT column_meta_id FROM column_aliases WHERE column_meta_id = %s", (row["column_id"], ))
            if not alias_cursor.fetchall():
                raise HTTPException(status_code=404, detail=f"Column '{name}' does not have alias")

            alias_cursor.execute("DELETE FROM column_aliases WHERE column_meta_id = %s", (row["column_id"], ))
            alias_conn.commit()

    # если нет - выкидываем ошибку
    except TypeError:
        raise HTTPException(status_code=404, detail=f"Column '{name}' does not exist")

    meta_cursor.close()
    alias_cursor.close()
    meta_conn.close()
    alias_conn.close()


def delete_alias(ar: AliasRequest) -> AliasResponse:
    """
    Deletes db/table alias
    """

    if ar.database != "" and ar.table != "" and ar.column != "":
        delete_column_alias(ar.database, ar.table, ar.column)
        return AliasResponse(message=(
            f"Column alias deleted: database='{ar.column}'"
        ))

    elif ar.table == "" and ar.column == "":
        delete_database_alias(ar.database)
        return AliasResponse(message=(
            f"Database alias deleted: database='{ar.database}'"
        ))

    elif ar.column == "":
        delete_table_alias(ar.database, ar.table)
        return AliasResponse(message=(
            f"Table alias deleted: database='{ar.database}', table='{ar.table}"
        ))

    else:
        return AliasResponse(message=(
            f"Please specify database, table and column correctly"
        ))
