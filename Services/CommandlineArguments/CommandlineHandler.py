from Services.Config.Config import Config, read_conf, reset_config
from Services.Logger.Log import write_message, LogLevel
from Actions import High_intensity_calculations


def handle_args(arguments):

    if arguments['verbose']:
        Config.VERBOSE = 1

    if arguments['highintense']:
        High_intensity_calculations.start_high_intensity_calculations()
        sys.exit(21)

    if arguments['debug']:
        Config.DEBUG = 1
        write_message('IMPORTANT NOTICE: DEBUG MODE IS ACTIVE!', LogLevel.Info)

    if arguments['restore']:
        success = reset_config()
        if success is not True:
            write_message(success, LogLevel.Error)
        else:
            write_message('Restored Config.ini', LogLevel.Info)

    write_message('Arguments {0}'.format(arguments), LogLevel.Verbose)
