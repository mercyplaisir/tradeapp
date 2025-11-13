""" logging tools"""
import logging
import pathlib


LOG_PATH = pathlib.Path('app.log')

def create_logger(class_name:str):
    """ logger creator """
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
    fl = logging.FileHandler(filename = LOG_PATH,)
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
    """logger wrapper decorator"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            log =  create_logger(class_name)
            log.info("starting %s",message)
            res  = func(*args, **kwargs)
            log.info("ending %s",message)
            return res
        return wrapper
    return decorator
