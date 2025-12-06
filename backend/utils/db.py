import mysql.connector
from utils import mysql_config

def get_connection(database: str = "metadata"):
    """Create MySQL connection"""
    return mysql.connector.connect(
        host=mysql_config.MYSQL_HOST,
        user=mysql_config.MYSQL_USER,
        password=mysql_config.MYSQL_PASSWORD,
        database=database
    )