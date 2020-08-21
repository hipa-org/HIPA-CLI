import logging


class DatabaseConfiguration:
    HOST = ''
    PORT = 0
    USER = ''
    PASSWORD = ''
    DATABASE = ''


def load_database_config(database_config):
    try:
        DatabaseConfiguration.HOST = database_config['HOST']
        DatabaseConfiguration.PORT = database_config['PORT']

    except KeyError as ex:
        logging.warning(f"Key not found!")
        logging.warning(ex)
