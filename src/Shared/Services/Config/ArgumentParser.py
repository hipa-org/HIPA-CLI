import argparse
import logging


class CLIArguments:
    high = None
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
                        help="Restores the default Config.ini")
    parser.add_argument("-w", "--web", required=False, action='store_true',
                        help="Starts the webserver version of the tool")

    args = parser.parse_args()
    CLIArguments.debug = args.debug
    CLIArguments.high = args.highintensity
    CLIArguments.restore_settings = args.restore
    CLIArguments.start_web_server = args.web


def handle_args():
    """
    Handles the parsed arguments and overrides default behaviour
    """

    if cli_args.web:
        Config.START_WEB_SERVER = True

    if cli_args.verbose:
        Config.VERBOSE = True

    if cli_args.highintensity and not Config.START_WEB_SERVER:
        Config.START_HIGH_INTENSITY_CALCULATION = True

    if cli_args.debug:
        Config.DEBUG = True
        logging.debug('IMPORTANT NOTICE: DEBUG MODE IS ACTIVE!')

    if cli_args.restore:
        success = reset_config()
        if success is not True:
            logging.error("Could not reset config!")
        else:
            logging.info('Restored Configuration.')
