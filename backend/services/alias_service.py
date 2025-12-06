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
    db_name = ""
    table_name = ""
    db_id = 0
    
    if ar.table == None:
        # Если поле table пустое, то создаем псевдоним для имени бд
        try:
            # Проверка существования псевдонима
            query = f"""
            SELECT db_alias
            FROM dbs
            WHERE db_name = `{ar.database}`;
            """
            cursor.execute(query)
            db_alias = cursor.fetchone()['db_alias']
            # (todo) raise Exception!
        except TypeError as e:
            # Если нет, то создаем новый
            try:
                query = f"""
                UPDATE dbs
                SET db_alias = `{ar.alias}`
                WHERE db_name = `{ar.database}`;
                """
                cursor.execute(query)
            except Error as e:
                raise HTTPException(status_code=404, detail=str(e))
    else:
        # Если поле table не пустое, то создаем псевдоним для имени таблицы бд
        try:
            # Проверка существования псевдонима
            query = f"""
            SELECT table_alias
            FROM db_tables
            WHERE db_name = `{ar.database}` AND table_name = `{ar.table}`;
            """
            cursor.execute(query)
            table_alias = cursor.fetchone()['table_alias']
            # (todo) raise Exception!
        except TypeError as e:
            # Если нет, создаем новый
            try:
                query = f"""
                UPDATE db_tables
                SET table_alias = `{ar.alias}`
                WHERE db_name = `{ar.database}` AND table_name = `{ar.table}`;
                """
                cursor.execute(query)
            except Error as e:
                raise HTTPException(status_code=404, detail=str(e))

    cursor.close()
    conn.close()

    return AliasResponse('OK')
