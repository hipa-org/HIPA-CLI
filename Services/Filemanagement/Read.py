from Services.Logger import Log
import sys
from Services.Config.Config import Config
from GlobalData import Statics


def read_time_traces_file():
        for file in Statics.input_files:
            try:
                file_content = open('{0}{1}'.format(Config.WORKING_DIRECTORY, file.name), "r")
                rows = (row.strip().split() for row in file_content)
                content = zip(*(row for row in rows if row))
                file.content = content
                file_content.close()
            except FileNotFoundError as ex:
                Log.write_message('Could not locate File {0}{1}'.format(Config.WORKING_DIRECTORY, file),
                                  Log.LogLevel.Error)
                Log.write_message('More Information in Log', Log.LogLevel.Error)
                Log.write_message(ex, Log.LogLevel.Verbose)
                input()
                sys.exit(21)


