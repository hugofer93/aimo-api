from peewee import SqliteDatabase

from utils.settings import load_module_as_dict


settings = load_module_as_dict('settings')

db_instance = SqliteDatabase(settings.get('DATABASE').get('NAME'))


def connect_db() -> None:
    """Create a database connection,
    before each request.
    """
    db_instance.connect()


def close_db() -> None:
    """Close the database connection,
    after each request.
    """
    if not db_instance.is_closed():
        db_instance.close()
