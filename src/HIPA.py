import sys
from Shared.Services.Config import Configuration, ArgumentParser
import os
import logging
from CLI import CLI
from Web import WebServer

logging.basicConfig(filename='log.log', level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(handler)

if __name__ == "__main__":
    try:
        Configuration.read_conf()
        ArgumentParser.handle_args()

        if Configuration.Config.START_WEB_SERVER:
            WebServer.start()
        else:
            CLI.start_cli_tool()


    except KeyboardInterrupt:
        print('\n')
        try:
            sys.exit(0)

        except SystemExit:
            sys.exit(0)
