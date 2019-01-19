from Services.Logger.log import write_message, LogLevel
import sys
from Services.Config.Config import Config
from GlobalData.Statics import input_files


def read_time_traces_file():
        for file in input_files:
            try:
                file_content = open('{0}{1}'.format(Config.WORKING_DIRECTORY, file.name), "r")
                rows = (row.strip().split() for row in file_content)
                content = zip(*(row for row in rows if row))
                file.content = content
                file_content.close()
            except FileNotFoundError as ex:
                write_message('Could not locate File {0}{1}'.format(Config.WORKING_DIRECTORY, file),
                              LogLevel.Error)
                write_message('More Information in Log', LogLevel.Error)
                write_message(ex, LogLevel.Verbose)
                input()
                sys.exit(21)




