"""
This module is the custom logger the only purpose of which is to customize the
output of the logged messages
"""
import logging


def get_logger():
    """
    This function creates a custom logger, handler and formatter for this
    logger and returns it for use
    """
    logger =  logging.getLogger('pipelines_logger')
    handler = logging.StreamHandler()
    formatter =  logging.Formatter('%(asctime)s: %(levelname)s -- logged by: \
%(filename)s -- %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

