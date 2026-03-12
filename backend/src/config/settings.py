"""
Class meant for storing settings for different modules.
"""
import os


class Settings(object):
    dir_name = os.path.dirname(__file__)
    
    @staticmethod
    def logger_config_file() -> str:
        file_name = "logger_config.json"
        return os.path.join(Settings.dir_name, file_name)

    # @staticmethod
    # def api_config_file() -> str:
    #     file_name = "api.json"
    #     return os.path.join(Settings.dir_name, file_name)

    @staticmethod
    def db_config_file() -> str:
        file_name = "db_credentials.json"
        return os.path.join(Settings.dir_name, file_name)

"""
TO USE:

from src.config.settings import Settings

config_name = Settings.api_config_file()
with open(config_name, "r") as file:
    config = json.load(file)

Then use config variable.
"""