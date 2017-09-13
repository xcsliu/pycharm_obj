import logging.handlers
import os
import time
from pypinyin import lazy_pinyin

from util import is_windows_system


class FinalLogger:
    logger = None
    levels = {"n": logging.NOTSET,
              "d": logging.DEBUG,
              "i": logging.INFO,
              "w": logging.WARN,
              "e": logging.ERROR,
              "c": logging.CRITICAL}

    log_level = "i"
    log_file_name = "crawler.log"
    log_max_byte = 10 * 1024 * 1024
    log_backup_count = 5


    @staticmethod
    def getLogger():
        if FinalLogger.logger is not None:
            return FinalLogger.logger

        # base info
        date = time.strftime("%Y_%m_%d", time.localtime())
        # city_name_pinyin = ''.join(lazy_pinyin(city_name))
        path = os.path.join(os.path.dirname(os.getcwd()), 'poi', 'poi_data', date)
        if not os.path.exists(path):
            os.makedirs(path)
        log_file_path = os.path.join(path, FinalLogger.log_file_name)
        # log conf
        FinalLogger.log_file = log_file_path if is_windows_system() else log_file_path.replace('\\', '/')
        FinalLogger.logger = logging.Logger("poi_log")
        # backup nothing mush
        log_handler = logging.handlers.RotatingFileHandler(filename=FinalLogger.log_file,
                                                           maxBytes=FinalLogger.log_max_byte,
                                                           backupCount=FinalLogger.log_backup_count)
        # format
        log_fmt = logging.Formatter("[%(asctime)s][%(levelname)s][%(name)s][%(funcName)s][%(message)s]")
        log_handler.setFormatter(log_fmt)
        FinalLogger.logger.addHandler(log_handler)
        FinalLogger.logger.setLevel(FinalLogger.levels.get(FinalLogger.log_level))
        return FinalLogger.logger
