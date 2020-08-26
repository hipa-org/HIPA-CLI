from Shared.Services.Configuration.Parser.Argument_Parser import CLIArguments
from Shared.Services.Configuration import Server_Configuration, CLI_Configuration


def get_config():
    """
    Returns the configuration for the appropriate situationx
    Returns
    -------

    """
    if CLIArguments.start_web_server:
        return Server_Configuration.ServerConfig
    else:
        return CLI_Configuration.CliConfiguration
