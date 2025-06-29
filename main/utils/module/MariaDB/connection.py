from .config import config
import pymysql


def get_maria_connection(db_config):
    return pymysql.connect(**db_config)


def connect(db_config=None):
    if db_config is None:
        db_config = config()
    try:
        connection = get_maria_connection(db_config)
        return connection, None
    except pymysql.MySQLError as e:
        return None, str(e)
