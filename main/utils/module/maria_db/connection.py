from .config import MARIA_DB_CONFIG
import pymysql


def get_maria_connection(db_config):
    return pymysql.connect(**db_config)


def connect_to_maria_database(db_config=None):
    if db_config is None:
        db_config = MARIA_DB_CONFIG()
    try:
        connection = get_maria_connection(db_config)
        return connection, None
    except pymysql.MySQLError as e:
        return None, str(e)
