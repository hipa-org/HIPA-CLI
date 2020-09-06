import mysql.connector
import mysql.connector.pooling
from Shared.Services.Configuration.Server_Configuration import ServerConfig
from Shared.Database import Database_Updater
import logging

databasePool = None
databaseConnection = None


def start_db():
    """
    Handles the database start up
    Returns
    -------

    """
    __connect_db()
    Database_Updater.create_db()
    Database_Updater.update_db()
    __connect_to_schema()
    pass


def __connect_db():
    try:
        global databaseConnection
        databaseConnection = mysql.connector.connect(pool_name="hipaPool",
                                                     pool_size=ServerConfig.MySqlConfiguration.POOL_SIZE,
                                                     autocommit=True,
                                                     user=ServerConfig.MySqlConfiguration.USER,
                                                     password=ServerConfig.MySqlConfiguration.PASSWORD,
                                                     host=ServerConfig.MySqlConfiguration.HOST,
                                                     )
        logging.info("Database connection established.")
    except ConnectionError as ex:
        logging.exception(ex)


def __connect_to_schema():
    try:
        global databasePool
        databasePool = mysql.connector.pooling.MySQLConnectionPool(pool_name="hipaPool",
                                                                   pool_size=ServerConfig.MySqlConfiguration.POOL_SIZE,
                                                                   autocommit=True,
                                                                   user=ServerConfig.MySqlConfiguration.USER,
                                                                   password=ServerConfig.MySqlConfiguration.PASSWORD,
                                                                   host=ServerConfig.MySqlConfiguration.HOST,
                                                                   database=ServerConfig.MySqlConfiguration.DATABASE)
    except ConnectionError as ex:
        logging.exception(ex)
