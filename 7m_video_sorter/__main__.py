import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3"

import queue
import config.config_manager as config
import search
import logging

logger = logging.getLogger('main')

logger.setLevel(10)

log_handler = logging.StreamHandler()
log_formatter = logging.Formatter()

log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

config = config.ConfigManager()

match_queue = queue.Queue()
search_queue = queue.Queue()


search.search_dir(config, search_queue)

logger.info("App done")
