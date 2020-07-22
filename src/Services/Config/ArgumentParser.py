from Services.Config.Configuration import Config, read_conf, reset_config
from Actions import High_Intensity_Calculations
import sys
import argparse
import logging


def handle_args():
    """
    Handles the parsed arguments and overrides default behaviour
    """
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

    args = parser.parse_args()

    if args.verbose:
        Config.VERBOSE = True

    if args.highintensity:
        Config.START_HIGH_INTENSITY_CALCULATION = True

    if args.debug:
        Config.DEBUG = True
        logging.debug('IMPORTANT NOTICE: DEBUG MODE IS ACTIVE!')

    if args.restore:
        success = reset_config()
        if success is not True:
            logging.error("Could not reset config!")
        else:
            logging.info('Restored Configuration.')
