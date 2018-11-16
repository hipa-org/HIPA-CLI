import os


def create_log_file():
    os.makedirs("Log")
    log_file = open("Log/log.txt", "w")
    log_file.write('Created Log\n')
    log_file.close()
