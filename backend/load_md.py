import mysql.connector
from mysql.connector import errorcode

CONFIG = {
    "user": "root",
    "password": "1q2w3e4r5t",
    "host": "localhost",
}

METADATA_DB = "metadata"


def create_metadata_schema(cursor):
    schema_sql = """

    DROP SCHEMA IF EXISTS metadata;
    CREATE DATABASE IF NOT EXISTS metadata
      DEFAULT CHARACTER SET utf8mb4
      COLLATE utf8mb4_0900_ai_ci;
    USE metadata;

    CREATE TABLE IF NOT EXISTS dbs (
        db_id INT AUTO_INCREMENT PRIMARY KEY,
        db_name VARCHAR(64) NOT NULL UNIQUE,
        db_alias VARCHAR(64) UNIQUE
    ) ENGINE=InnoDB;

    CREATE TABLE IF NOT EXISTS db_tables (
        table_id INT AUTO_INCREMENT PRIMARY KEY,
        db_id INT NOT NULL,
        table_name VARCHAR(64) NOT NULL,
        table_alias VARCHAR(64) NULL,
        FOREIGN KEY (db_id) REFERENCES dbs(db_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB;

    CREATE TABLE IF NOT EXISTS db_columns (
        column_id INT AUTO_INCREMENT PRIMARY KEY,
        table_id INT NOT NULL,
        column_name VARCHAR(64) NOT NULL,
        FOREIGN KEY (table_id) REFERENCES db_tables(table_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB;

    CREATE TABLE IF NOT EXISTS key_names (
        key_id INT AUTO_INCREMENT PRIMARY KEY,
        table_id INT NOT NULL,
        key_name VARCHAR(64) NOT NULL,
        type ENUM('PRIMARY', 'UNIQUE', 'FOREIGN', 'INDEX') NOT NULL,
        FOREIGN KEY (table_id) REFERENCES db_tables(table_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB;

    CREATE TABLE IF NOT EXISTS key_columns (
        kc_id INT AUTO_INCREMENT PRIMARY KEY,
        key_id INT NOT NULL,
        column_id INT NOT NULL,
        position INT NOT NULL,
        FOREIGN KEY (kc_id) REFERENCES key_names(key_id)  -- ошибка схемы
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (column_id) REFERENCES db_columns(column_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB;

    CREATE TABLE IF NOT EXISTS foreign_keys (
        fk_id INT AUTO_INCREMENT PRIMARY KEY,
        pk_id INT NOT NULL,
        referenced_key_id INT NOT NULL,
        FOREIGN KEY (fk_id) REFERENCES key_names(key_id)  -- ошибка схемы
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (pk_id) REFERENCES key_names(key_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB;
    """

    for stmt in schema_sql.split(";"):
        if stmt.strip():
            cursor.execute(stmt)


def load_metadata():
    cnx = mysql.connector.connect(**CONFIG)
    cursor = cnx.cursor(buffered=True)

    create_metadata_schema(cursor)
    cursor.execute(f"USE {METADATA_DB}")

    cursor.execute("SHOW DATABASES")
    databases = [
        row[0]
        for row in cursor.fetchall()
        if row[0] not in ("mysql", "performance_schema", "sys", METADATA_DB)
    ]

    for db_name in databases:
        print("Обработка БД:", db_name)

        cursor.execute(
            "INSERT INTO dbs (db_name) VALUES (%s)",
            (db_name,)
        )
        cnx.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        db_id = cursor.fetchone()[0]

        cursor.execute(
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s",
            (db_name,)
        )
        for (table_name,) in cursor.fetchall():

            cursor.execute(
                "INSERT INTO db_tables (db_id, table_name) VALUES (%s, %s)",
                (db_id, table_name)
            )
            cnx.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            table_id = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                """,
                (db_name, table_name)
            )
            for (column_name,) in cursor.fetchall():
                cursor.execute(
                    "INSERT INTO db_columns (table_id, column_name) VALUES (%s, %s)",
                    (table_id, column_name)
                )

            cursor.execute(
                """
                SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE
                FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                """,
                (db_name, table_name)
            )

            mapping = {
                "PRIMARY KEY": "PRIMARY",
                "UNIQUE": "UNIQUE",
                "FOREIGN KEY": "FOREIGN",
            }

            for key_name, key_type in cursor.fetchall():
                type_mapped = mapping.get(key_type, "INDEX")
                cursor.execute(
                    "INSERT INTO key_names (key_name, type, table_id) VALUES (%s, %s, %s)",
                    (key_name, type_mapped, table_id),
                )
                cnx.commit()
                cursor.execute("SELECT LAST_INSERT_ID()")
                key_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    SELECT COLUMN_NAME, SEQ_IN_INDEX
                    FROM INFORMATION_SCHEMA.STATISTICS
                    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND INDEX_NAME = %s
                    """,
                    (db_name, table_name, key_name)
                )
                for column_name, pos in cursor.fetchall():
                    cursor.execute(
                        """
                        INSERT INTO key_columns (key_id, column_id, position)
                        SELECT %s, c.column_id, %s
                        FROM db_columns c
                        JOIN db_tables t ON t.table_id = c.table_id
                        WHERE t.table_id = %s AND c.column_name = %s
                        """,
                        (key_id, pos, table_id, column_name)
                    )

            cursor.execute(
                """
                SELECT CONSTRAINT_NAME, REFERENCED_TABLE_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND REFERENCED_TABLE_NAME IS NOT NULL
                """,
                (db_name, table_name)
            )
            for fk_name, ref_table in cursor.fetchall():

                cursor.execute(
                    "SELECT key_id FROM key_names WHERE key_name = %s AND table_id = %s",
                    (fk_name, table_id)
                )
                fk_res = cursor.fetchone()
                if not fk_res:
                    continue

                fk_key_id = fk_res[0]

                cursor.execute(
                    """
                    SELECT kn.key_id
                    FROM key_names kn
                    JOIN db_tables t ON kn.table_id = t.table_id
                    WHERE t.table_name = %s AND t.db_id = %s AND kn.type='PRIMARY'
                    """,
                    (ref_table, db_id)
                )
                ref_pk = cursor.fetchone()
                if ref_pk:
                    cursor.execute(
                        "INSERT INTO foreign_keys (pk_id, referenced_key_id) VALUES (%s, %s)",
                        (fk_key_id, ref_pk[0])
                    )

        cnx.commit()

    print("Метаданные загружены.")
    cursor.close()
    cnx.close()


try:
    load_metadata()
except mysql.connector.Error as err:
    print("Ошибка:", err)
