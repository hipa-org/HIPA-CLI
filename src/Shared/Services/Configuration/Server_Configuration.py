from pathlib import Path
from Shared.Services.Configuration.Parser.Argument_Parser import CLIArguments
import logging
import sys
from enum import Enum


class DBSystem(Enum):
    MYSQL = 0


class ServerConfig:
    class GeneralConfig:
        DEBUG = False
        NORMALIZATION_METHOD = 'Baseline'
        DATABASE_SYSTEM = 0

    class DataConfig:
        # Folder
        WORKING_DIRECTORY = 'Data/'

        # File names
        OUTPUT_FILE_NAME_HIGH_STIMULUS = 'High-Stimulus'
        OUTPUT_FILE_NAME_NORMALIZED_DATA = 'Normalized-Data'
        OUTPUT_FILE_NAME_SPIKES_PER_MINUTE = 'Spikes_Per_Minute'

        # Data
        DATA_ROOT_DIRECTORY = Path()
        DATA_RAW_DIRECTORY = Path()
        DATA_RESULTS_DIRECTORY = Path()

    class MySqlConfiguration:
        HOST = ''
        PORT = 0
        USER = ''
        PASSWORD = ''
        DATABASE = ''
        POOL_SIZE = 0


def load_server_config(config):
    __load_general_config(config['general'])
    __load_data_config(config['data'])
    __load_database_config(config)
    pass


def __load_database_config(config):
    try:
        if ServerConfig.GeneralConfig.DATABASE_SYSTEM == DBSystem.MYSQL.value:
            ServerConfig.MySqlConfiguration.HOST = config['mysql'].get('HOST', "127.0.0.1")
            ServerConfig.MySqlConfiguration.PORT = config['mysql'].getint('PORT', 3306)
            ServerConfig.MySqlConfiguration.USER = config['mysql'].get('USER', 'root')
            ServerConfig.MySqlConfiguration.PASSWORD = config['mysql'].get('PASSWORD', 'root')
            ServerConfig.MySqlConfiguration.DATABASE = config['mysql'].get('DATABASE', "hipa")
            ServerConfig.MySqlConfiguration.POOL_SIZE = config['mysql'].getint('POOL_SIZE', 10)

    except KeyError as ex:
        __key_not_found_err(ex)


def __load_data_config(data_config):
    """
    Loads the data configuration for files and folder management
    Parameters
    ----------
    data_config

    Returns
    -------

    """
    try:

        # Directories
        ServerConfig.DataConfig.DATA_ROOT_DIRECTORY = Path(data_config['ROOT_DIRECTORY'])
        ServerConfig.DataConfig.DATA_RAW_DIRECTORY = Path(ServerConfig.DataConfig.DATA_ROOT_DIRECTORY,
                                                          data_config['RAW_DIRECTORY'])
        ServerConfig.DataConfig.DATA_RESULTS_DIRECTORY = Path(ServerConfig.DataConfig.DATA_ROOT_DIRECTORY,
                                                              data_config['RESULTS_DIRECTORY'])

        # File Names
        ServerConfig.DataConfig.OUTPUT_FILE_NAME_HIGH_STIMULUS = data_config[
            'OUTPUT_FILE_NAME_HIGH_STIMULUS']
        ServerConfig.DataConfig.OUTPUT_FILE_NAME_NORMALIZED_DATA = data_config[
            'OUTPUT_FILE_NAME_NORMALIZED_DATA']
        # ServerConfig.DataConfig.NORMALIZATION_METHOD = data_config['normalization_method']

    except KeyError as ex:
        __key_not_found_err(ex)


def __load_general_config(general_config):
    try:
        ServerConfig.GeneralConfig.DEBUG = general_config.getboolean('DEBUG_MODE', False)
        ServerConfig.GeneralConfig.DATABASE_SYSTEM = general_config.getint('DB_SYSTEM', 0)

        if CLIArguments.debug:
            ServerConfig.GeneralConfig.DEBUG = True
            logging.debug('IMPORTANT NOTICE: DEBUG MODE IS ACTIVE!')

    except KeyError as ex:
        __key_not_found_err(ex)


def __key_not_found_err(ex):
    logging.error(f"Error occurred while reading server-config.ini.")
    logging.error(f"Key: {ex} not found!")
    logging.error(f"Make sure the file server-config.ini exists in your Config directory!")
    sys.exit()
