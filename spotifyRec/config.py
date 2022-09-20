import logging
from configparser import ConfigParser
import os

logger = logging.getLogger(__name__)

def load_config(config_file):
    """Function that reads the config file, that is expected to be in at ini format

    Args:
        config_file (str): file path and name of the config file

    Returns:
        ConfigParser: ConfigParser object obtained from the config file
    """
    config = ConfigParser()
    try:
        config.read(config_file)
        logger.info(f"Config file {config_file} read")
        return config
    except Exception as e:
        logger.error("Was unable to read config file")
        logger.exception(e)

config_file = "configs/config.ini"
config = load_config(config_file)

CLIENT_ID = config.get("api_settings", "client_id")
CLIENT_SECRET = config.get("api_settings", "client_secret")
REDIRECT_URI = "http://localhost:9001/callback"
