import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3"

import queue
import threading
import config_manager as config
import search
import time
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

search_thread = threading.Thread(
    target=search.search_dir,
    daemon=True, args=(config, search_queue))

search_thread.start()

while search_thread.isAlive():
    time.sleep(5)

print("loop done")
