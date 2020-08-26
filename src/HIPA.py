import sys
from Shared.Services.Configuration.Parser import Configuration_Parser, Argument_Parser
import os
import logging
from CLI import CLI
from Web import WebServer
import traceback

logging.basicConfig(filename='log.log', level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(handler)

if __name__ == "__main__":
    try:
        Argument_Parser.load_args()
        Configuration_Parser.load_configuration()

        if Argument_Parser.CLIArguments.start_web_server:
            WebServer.start()
        else:
            CLI.start_cli_tool()


    except KeyboardInterrupt:
        print('\n')
        try:
            sys.exit(0)

        except SystemExit:
            os._exit(0)
            track = traceback.format_exc()
            logging.error(track)
