import logging.config
import pathlib
import json

from enum import Enum
from inspect import getframeinfo, stack
from src.config.settings import Settings


class Level(Enum):
    """
    Enum for storing logger levels, in order of increasing severity.
    """
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

class _Logger(object):
    """
    The class that handles logging.
    """
    
    def __init__(self) -> None:
        """
        Constructor. Loads logger settings JSON file from config folder to initialize logger.
        """
        config_path = Settings.logger_config_file()

        with open(config_path, "r") as file:
            config_json = json.load(file)

        logging.config.dictConfig(config_json)

        
        self.logger = logging.getLogger()

    
    def log(self, level: Level, msg: str) -> None:
        """
        Method for writing to logs. 

        Log levels are (in order of increasing severity):
            DEBUG

            INFO

            WARNING

            ERROR

            CRITICAL

        Levels stored in Level enum. Default level is INFO.

        :param level: Level of the input log
        :param msg: The message to display in the log.
        :type msg: str
        :return: None
        """
        # GET FRAME INFO? ASK LATER
        # FRAME INFO USED TO DISPLAY WHERE IN CODE LOG COMES FROM
        caller = getframeinfo(stack()[1][0]) # The path in the project where the call came from
        path = pathlib.PurePath(caller.filename)
        parts = path.parts # Split filepath into list of directories
        packageName = "/".join(parts[-2:-1].reverse())
        output = "{}/{}/{}:{} - {}".format(packageName, path.stem, caller.function, caller.lineno, msg)
        

        if level == Level.DEBUG.name:
            self.logger.debug(output)
        elif level == Level.INFO.name:
            self.logger.info(output)
        elif level == Level.WARNING.name:
            self.logger.warning(output)
        elif level == Level.ERROR.name:
            self.logger.error(output)
        elif level == Level.CRITICAL.name:
            self.logger.critical(output)
        else:
            self.logger.info(output)