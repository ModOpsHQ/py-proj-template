# /*===================================
#     Stock Imports
# ====================================*/

import logging
import os
import requests
import sys

# /*===================================
#     Set Current Working Dir
# ====================================*/

CWD: str
if getattr(sys, 'frozen', False):
    CWD = os.path.join(os.path.dirname(sys.executable), '_internal')
else:
    CWD = os.getcwd()

# /*===================================
#     Add src dir to python path
# ====================================*/

sys.path.insert(0, os.path.join(CWD, 'src'))

# /*===================================
#     Configure Logger
# ====================================*/

logger = logging.getLogger(__name__)

# /*===================================
#     Main
# ====================================*/

LOADED: bool = False

LOG_LEVEL: int

# /*===================================
#     Set Logging
# ====================================*/

def set_logging_level(log_level: str) -> None:
    global LOG_LEVEL

    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    level = log_level_map.get(log_level, logging.DEBUG)
    
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Find and update the console handler
    for handler in root_logger.handlers:
        if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
            handler.setLevel(level)
            break
    
    LOG_LEVEL = level

    logger.setLevel(level)
    logger.info(f"Logging set to: {log_level}")

# /*===================================
#     Initialize Config
# ====================================*/

def initialize(log_level: str) -> None:
    global LOADED

    load_hq()  # must be first

    _map = {
        set_logging_level: log_level
    }
    
    for func, arg in _map.items():
        try:
            func() if arg is None else func(arg)
        except Exception as e:
            logger.error(f"An error occurred in '{func.__name__}', error: {e}")
            return

    LOADED = True
    logger.info("Config successfully loaded")