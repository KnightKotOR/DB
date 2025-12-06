from utils.db import get_connection
from mysql.connector import Error

from models.md_model import MetadataResponse


def collect_metadata(database: str) -> MetadataResponse:
    """Extract metadata from INFORMATION_SCHEMA for the source DB and store it in metadata_catalog."""
    try:
        src_conn = get_connection("information_schema")
        meta_conn = get_connection()
        src_cursor = src_conn.cursor(dictionary=True)
        meta_cursor = meta_conn.cursor()

        # Check if database already in metadata_catalog
        meta_cursor.execute("SELECT db_id FROM dbs WHERE db_name=%s", (database,))
        res = meta_cursor.fetchone()
        if res:
            return MetadataResponse(status="exists", message=f"Database '{database}' already exists.")

        src_cursor.execute(
            "SELECT SCHEMA_NAME FROM SCHEMATA WHERE SCHEMA_NAME = %s", (database,)
        )
        db_row = src_cursor.fetchone()
        if not db_row:
            return MetadataResponse(status="not_found", message=f"Database '{database}' not found.")

        # insert database
        meta_cursor.execute("INSERT INTO dbs (db_name) VALUES (%s)", (database,))
        meta_conn.commit()
        meta_cursor.execute("SELECT db_id FROM dbs WHERE db_name=%s", (database,))
        db_id = meta_cursor.fetchone()[0]

        # tables
        src_cursor.execute("""
            SELECT TABLE_NAME FROM TABLES WHERE TABLE_SCHEMA = %s
        """, (database,))
        tables = src_cursor.fetchall()

        table_id_map = {}
        for t in tables:
            tname = t["TABLE_NAME"]
            meta_cursor.execute(
                "INSERT INTO db_tables (db_id, table_name) VALUES (%s, %s)",
                (db_id, tname)
            )
            table_id_map[tname] = meta_cursor.lastrowid
        meta_conn.commit()

        # columns
        src_cursor.execute("""
            SELECT TABLE_NAME, COLUMN_NAME
            FROM COLUMNS
            WHERE TABLE_SCHEMA = %s
            ORDER BY TABLE_NAME, ORDINAL_POSITION
        """, (database,))
        columns = src_cursor.fetchall()

        column_id_map = {}
        for col in columns:
            tname = col["TABLE_NAME"]
            cname = col["COLUMN_NAME"]
            if tname not in table_id_map:
                continue
            meta_cursor.execute(
                "INSERT INTO db_columns (table_id, column_name) VALUES (%s, %s)",
                (table_id_map[tname], cname)
            )
            column_id_map[(tname, cname)] = meta_cursor.lastrowid
        meta_conn.commit()

        # constraints
        src_cursor.execute("""
            SELECT TABLE_NAME, CONSTRAINT_NAME, CONSTRAINT_TYPE
            FROM TABLE_CONSTRAINTS
            WHERE TABLE_SCHEMA = %s
        """, (database,))
        constraints = src_cursor.fetchall()

        constraint_id_map = {}
        for c in constraints:
            tname, cname, ctype = c["TABLE_NAME"], c["CONSTRAINT_NAME"], c["CONSTRAINT_TYPE"]
            if ctype == "PRIMARY KEY":
                ctype = "PRIMARY"
            elif ctype == "UNIQUE":
                ctype = "UNIQUE"
            elif ctype == "FOREIGN KEY":
                ctype = "FOREIGN"
            else:
                ctype = "INDEX"
            meta_cursor.execute(
                "INSERT INTO constraints (table_id, constraint_name, type) VALUES (%s, %s, %s)",
                (table_id_map[tname], cname, ctype)
            )
            constraint_id_map[(tname, cname)] = meta_cursor.lastrowid
        meta_conn.commit()

        # Constraint Columns
        src_cursor.execute("""
            SELECT CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION
            FROM KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = %s
            ORDER BY CONSTRAINT_NAME, ORDINAL_POSITION
        """, (database,))
        kcols = src_cursor.fetchall()
        for kc in kcols:
            cname, tname, colname, pos = kc.values()
            if (tname, cname) in constraint_id_map and (tname, colname) in column_id_map:
                meta_cursor.execute("""
                    INSERT INTO constraint_columns (constraint_id, column_id, position)
                    VALUES (%s, %s, %s)
                """, (
                    constraint_id_map[(tname, cname)],
                    column_id_map[(tname, colname)],
                    pos
                ))
        meta_conn.commit()

        # foreign keys
        # Referential constraints (foreign key → primary key)
        # Get all foreign key relationships with referenced tables
        src_cursor.execute("""
                    SELECT
                        rc.CONSTRAINT_NAME AS fk_name,
                        rc.CONSTRAINT_SCHEMA AS fk_schema,
                        kcu.TABLE_NAME AS fk_table_name,
                        kcu.REFERENCED_TABLE_NAME AS referenced_table_name
                    FROM REFERENTIAL_CONSTRAINTS rc
                    JOIN KEY_COLUMN_USAGE kcu
                      ON rc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
                     AND rc.CONSTRAINT_SCHEMA = kcu.CONSTRAINT_SCHEMA
                    WHERE rc.CONSTRAINT_SCHEMA = %s
                    GROUP BY rc.CONSTRAINT_NAME, kcu.TABLE_NAME, kcu.REFERENCED_TABLE_NAME
                """, (database,))

        fks = src_cursor.fetchall()

        for fk in fks:
            fk_name = fk["fk_name"]
            fk_table = fk["fk_table_name"]
            ref_table = fk["referenced_table_name"]

            # Get foreign key constraint ID
            fk_id = constraint_id_map.get((fk_table, fk_name))
            if fk_id is None:
                continue

            # Get referenced table ID
            ref_table_id = table_id_map.get(ref_table)
            if ref_table_id is None:
                continue

            # Get primary key constraint ID for referenced table
            pk_id = None
            for (tname, cname), cid in constraint_id_map.items():
                if tname == ref_table and cname == "PRIMARY":
                    pk_id = cid
                    break

            if pk_id is None:
                continue

            # Insert into referential_constraints
            meta_cursor.execute("""
                        INSERT INTO referential_constraints (fk_constraint_id, pk_constraint_id)
                        VALUES (%s, %s)
                    """, (fk_id, pk_id))
            meta_conn.commit()

        return MetadataResponse(status="success", message=f"Metadata imported for {database}.")

    except Error as e:
        return MetadataResponse(status="error", message=f"MySQL Error: {e}")

    finally:
        for c in [src_cursor, meta_cursor]:
            if c:
                c.close()
        for conn in [src_conn, meta_conn]:
            if conn and conn.is_connected():
                conn.close()