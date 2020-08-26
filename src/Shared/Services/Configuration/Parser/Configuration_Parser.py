import configparser
from Shared.Services.Configuration import CLI_Configuration, Server_Configuration
from Shared.Services.Configuration.Parser.Argument_Parser import CLIArguments


def load_configuration():
    """
    Loads the Configuration.ini File, and stores the values into the Configuration Class
    :return:
    """
    config = configparser.ConfigParser()

    # Load the web server config, otherwise load cli config
    if CLIArguments.start_web_server:
        config.read('Config/server-config.ini')
        Server_Configuration.load_server_config(config)
    else:
        config.read('Config/cli-config.ini')
        CLI_Configuration.load_cli_config(config)


def reset_config():
    """
    Resets the Configuration File. In fact the Configuration.ini file will be rewritten in total.
    :return:
    """
    config = configparser.ConfigParser()
    config['SETTINGS'] = {
        'input_file_name': 'time_traces',
        'working_directory': 'Data/',
        'output_file_name_high_stimulus': 'High-Stimulus',
        'output_file_name_normalized_data': 'Normalized-Data',
        'normalization_method': 'Baseline'
    }
    config['LOGS'] = {
        'logs_path': 'Logs/',
        'error_log': 'error-log.txt',
        'default_log': 'default-log.txt'
    }
    with open('Configuration.ini', 'w') as configfile:
        try:
            config.write(configfile)
            configfile.close()
            return True
        except FileNotFoundError as ex:
            return ex
