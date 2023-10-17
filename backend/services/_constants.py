#!/usr/bin/env python3
"""
Constants used throughout app.
"""



import logzero
from logzero import logger

# variables
logging_dir = './logs/process.log'

# logging
logzero.loglevel(logzero.INFO)                                           #set a minimum log level: debug, info, warning, error
logzero.logfile(logging_dir, maxBytes=1000000, backupCount=3)            #set rotating log file
logger.info('logger created, constants initialized')
