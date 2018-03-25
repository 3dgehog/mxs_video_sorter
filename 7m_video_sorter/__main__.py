import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3"

import queue
import threading
import config
import search

config = config.Config()

match_queue = queue.Queue()
search_queue = queue.Queue()

search_thread = threading.Thread(
    target=search.search_dir,
    daemon=True, args=(config.input_dir, search_queue))
