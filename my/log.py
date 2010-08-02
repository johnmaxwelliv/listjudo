import logging
import sys

def set_up(log_file, log_level=logging.NOTSET):
    logger = logging.getLogger()
    if len(logger.handlers) > 2:
        return
    hdlr = logging.FileHandler(log_file)
    formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s"%(message)s"','%Y-%m-%d %a %H:%M:%S')

    hdlr.setFormatter(formatter)
    logger.addHandler(logging.StreamHandler(sys.stderr))
    logger.addHandler(hdlr)
    logger.setLevel(log_level)
    return logger
