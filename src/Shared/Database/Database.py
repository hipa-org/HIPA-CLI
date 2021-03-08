import mysql.connector
import mysql.connector.pooling
from Shared.Database import Database_Loader, PreparedStatement


def insert(prepared_statement: PreparedStatement):
    """
    Insert command for a db query
    Parameters
    ----------
    prepared_statement

    Returns
    -------

    """

    connection = Database_Loader.database_pool.get_connection()
    cursor = connection.cursor(prepared=True)

    try:
        cursor.execute(prepared_statement.query, prepared_statement.parameters)
        connection.commit()

    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def select(prepared_statement: PreparedStatement):
    """
    Select query
    Parameters
    ----------
    prepared_statement

    Returns
    -------

    """

    connection = Database_Loader.database_pool.get_connection()
    cursor = connection.cursor(prepared=True)

    try:

        cursor.execute(prepared_statement.query, prepared_statement.parameters)
        return cursor.fetchall()

    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))
        return {}

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def update(prepared_statement: PreparedStatement):
    """
    Update query
    Parameters
    ----------
    prepared_statement

    Returns
    -------

    """

    connection = Database_Loader.database_pool.get_connection()
    cursor = connection.cursor(prepared=True)
    try:

        cursor.execute(prepared_statement.query, prepared_statement.parameters)
        connection.commit()

    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
