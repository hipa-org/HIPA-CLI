import mysql.connector
import mysql.connector.pooling

databasePool = None
databaseConnection = None


def connect_db(database=None):
    try:
        if database is None:
            global databaseConnection
            databaseConnection = mysql.connector.connect(pool_name="websitePool",
                                                         pool_size=10,
                                                         autocommit=True,
                                                         user="root",
                                                         password="raphaelk1",
                                                         host="127.0.0.1",
                                                         )
        else:
            global databasePool
            databasePool = mysql.connector.pooling.MySQLConnectionPool(pool_name="websitePool",
                                                                       pool_size=10,
                                                                       autocommit=True,
                                                                       user="root",
                                                                       password="raphaelk1",
                                                                       host="127.0.0.1",
                                                                       database="hipacli")
            print("Database connection established.")
    except ConnectionError:
        print("Oops! Error connecting to the database")
