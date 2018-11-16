import configparser
import os.path



def create_config():
    config = configparser.ConfigParser()
    config['DEFAULT_NAMES'] = {'input_file_name': 'time_traces'}
    config['SETTINGS'] = {
        'debug_mode': 0,
        'verbose': 0
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    configs = config.sections()
    print('COnfigs {0}'.format(configs))
   # print(configs['SETTINGS']['debug_mode'])
    print(config['SETTINGS']['debug_mode'])


def check_config():
    file_exists = os.path.exists("config.ini")
    print(file_exists)
    if file_exists:
        read_config()
    else:
        create_config()
        read_config()
