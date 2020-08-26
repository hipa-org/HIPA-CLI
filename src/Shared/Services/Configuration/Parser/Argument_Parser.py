import argparse
import logging


class CLIArguments:
    start_high_intensity_calculations = None
    debug = None
    restore_settings = None
    start_web_server = None


def load_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", required=False,
                        action='store_true',
                        help="Activate verbose Output")
    parser.add_argument("-high", "--highintensity", required=False,
                        action='store_true',
                        help='Direct call of calculation')
    parser.add_argument("-d", "--debug", required=False,
                        action='store_true',
                        help="Starts the program in Debug Mode")
    parser.add_argument("-r", "--restore", required=False,
                        action='store_true',
                        help="Restores the default Configuration.ini")
    parser.add_argument("-s", "--server", required=False, action='store_true',
                        help="Starts the webserver version of the tool")

    args = parser.parse_args()
    CLIArguments.debug = args.debug
    CLIArguments.start_high_intensity_calculations = args.highintensity
    CLIArguments.restore_settings = args.restore
    CLIArguments.start_web_server = args.server
