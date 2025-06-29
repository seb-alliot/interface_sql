from psycopg2 import OperationalError
from .config import config
import psycopg2



def get_connection_sql(db_config):
    return psycopg2.connect(**db_config)


def connect(db_config=None):
    if db_config is None:
        db_config = config()
    try:
        connection = psycopg2.connect(**db_config)
        return connection, None
    except OperationalError as e:
        return None, str(e)
