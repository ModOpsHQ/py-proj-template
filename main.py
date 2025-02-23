# /*===================================
#     Stock Imports
# ====================================*/

import argparse
import colorlog
import logging
import os
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

# /*===================================
#     Configure Logging
# ====================================*/

def configure_logging() -> None:
    # Format strings
    fmt_str = '%(log_color)s%(asctime)s%(reset)s - %(log_color)s%(name)s%(reset)s - %(log_color)s%(levelname)s%(reset)s - %(message)s'
    timefmt_str = '%H:%M:%S'
    datefmt_str = '%Y-%m-%d'
    datetimefmt_str = f"{datefmt_str} {timefmt_str}"

    # Basic logging config
    logging.basicConfig(
        level=logging.DEBUG,
        format=fmt_str,
        datefmt=datetimefmt_str,
        handlers=[]  # Clear default handlers
    )
    
    # Get the logs directory
    logs_dir = os.path.join(os.getcwd(), 'logs')

    # Create logs directory
    os.makedirs(logs_dir, exist_ok=True)

    # Create file handler
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(logs_dir, f'app_{datetime.now().strftime(datefmt_str)}.log'),
        when='midnight',
        interval=1,
        backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)

    # Create console handler with color
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Create formatters
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=datetimefmt_str)
    console_formatter = colorlog.ColoredFormatter(
        fmt_str, 
        datefmt=datetimefmt_str,
        log_colors={
            'DEBUG': 'purple',
            'INFO': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    # Add formatters to handlers
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)

    # Get the root logger and add handlers
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Configure asyncio logging
    asyncio_logger = logging.getLogger('asyncio')
    asyncio_logger.setLevel(logging.INFO)

configure_logging()

# /*===================================
#     Parse Arguments
# ====================================*/

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Process configuration arguments')
    
    # Define expected arguments
    parser.add_argument('--log_level', default='DEBUG',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        required=True,
                        help='Logging level')

    return parser.parse_args()

args = parse_arguments()

# /*===================================
#     Initialize Config
# ====================================*/

import src.core.config as config

def init_config() -> None:
    config.initialize(log_level=args.log_level)
    if not config.LOADED:
        logger.error("Failed to load config, check logs for more information")
        sys.exit(1)

# raise RuntimeError("End of script")

# /*===================================
#     Main
# ====================================*/

async def main() -> None:
    # do something..
    pass

# /*===================================
#     Run
# ====================================*/

main()