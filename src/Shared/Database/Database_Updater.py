from Services.DB import DatabaseLoader, Database
import os
from Shared.Database.PreparedStatement import PreparedStatement
from Shared.Database.Implementation import Queries
import datetime
import logging


def update_db():
    """
    Updates the database
    :return:
    """
    logging.info("Updating database....")
    for filename in os.listdir("statistics-server/SQL/Updates"):
        if filename.endswith(".sql") and not update_already_applied(filename):
            execute_file(filename)
        else:
            continue
    logging.info("Database up to date!")


def execute_file(filename: str):
    """
    Reads the file and execute its queries
    :param filename:
    :return:
    """
    # Open and read the file as a single buffer
    fd = open(f"statistics-server/SQL/Updates/{filename}", 'r')
    sql_content = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sql_commands = sql_content.split(';')

    # create db cursor
    connection = DatabaseLoader.databasePool.get_connection()
    cursor = connection.cursor(prepared=False)
    error_count: int = 0
    # Execute every command from the input file
    for command in sql_commands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cursor.execute(command)
        except BaseException as msg:
            print(f"Command skipped: {msg}")
            error_count += 1

    connection.commit()
    if error_count == 0:
        update_successful_applied(filename)


def update_already_applied(filename):
    statement = PreparedStatement(Queries.DB_SEL_UPDATE)
    statement.add_param(0, filename)
    data = Database.select(statement)
    if data[0][0] == 1:
        return True
    else:
        return False


def update_successful_applied(filename: str):
    """
    Adds an successful update file to the updates table
    :param filename:
    :return:
    """
    statement = PreparedStatement(Queries.DB_INS_UPDATE)
    statement.add_param(0, filename)
    statement.add_param(1, 0)
    statement.add_param(2, "RELEASED")
    statement.add_param(3, datetime.datetime.utcnow())
    statement.add_param(4, 0)
    Database.insert(statement)
