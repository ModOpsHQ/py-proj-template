# /*===================================
#     Stock Imports
# ====================================*/

import colorlog
import logging

# /*===================================
#     Configure Logging (intially set log level here, then update the level in config.py)
# ====================================*/

# Set a log format
log_format = (
    '%(log_color)s%(asctime)s%(reset)s - '
    # '%(name)s - '
    '%(log_color)s%(name)s%(reset)s - '
    '%(log_color)s%(levelname)s%(reset)s - '
    '%(message)s'
)

# Configure the stream handler
handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        log_format, 
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'purple',
            'INFO': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[handler]
)

asyncio_logger = logging.getLogger('asyncio')
asyncio_logger.setLevel(logging.INFO)

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
config.initialize(
    args.log_level
)

# raise RuntimeError("End of script")

# /*===================================
#     Main
# ====================================*/

async def main() -> None:

    pass

# /*===================================
#     Run
# ====================================*/

main()