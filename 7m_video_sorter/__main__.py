import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3"

import queue
import config.config_manager as config
import logging
import logging.config
import yaml

import search
import match

# load logging configs
with open('7m_video_sorter/config/logging.yaml', 'r') as ymlfile:
    yamlconfig = yaml.load(ymlfile)
logging.config.dictConfig(yamlconfig)

# Logging
logger = logging.getLogger('main')
logger.setLevel(10)


config = config.ConfigManager()

match_queue = queue.Queue()
search_queue = queue.Queue()


search.search(config, search_queue)
match.match(config, search_queue, match_queue)

logger.info("App done")
