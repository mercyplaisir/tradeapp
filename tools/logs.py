
import logging
import pathlib

from telegram.telegram import Telegram

LOG_PATH = pathlib.Path('app.log')

def create_logger(class_name:str):
    
    # create logger
    logger = logging.getLogger(class_name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    fl = logging.FileHandler(
        filename = LOG_PATH,
        
        )
    # format the file
    fl.setFormatter(formatter)
    
    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    # add fl to logger
    logger.addHandler(fl)
    
    
    return logger

def logger_wrapper(class_name:str,message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            log =  create_logger(class_name)
            Telegram.send_message(message=message)
            log.info(f"starting {message}")
            res  = func(*args, **kwargs)
            log.info(f"ending {message}")
            return res
        return wrapper
    return decorator