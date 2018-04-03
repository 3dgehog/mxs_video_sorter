import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3"

import queue
import config
import logging
import logging.config
import yaml
import argparse
import progressbar

import search
import match
import transfer

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--review",
                    help="Runs through all files in output dir for review, doesn't transfer anything",
                    action="store_true")
parser.add_argument("-c", "--create_dir",
                    help="Creates Season # dir if it doesn't exists",
                    action="store_true")
parser.add_argument("-d", "--debug",
                    help="Run all debug logs",
                    action="store_true")
args = parser.parse_args()

# fix logging with progressbar
progressbar.streams.wrap_stderr()

# load logging configs
with open('7m_video_sorter/logging.yaml', 'r') as ymlfile:
    yamlconfig = yaml.load(ymlfile)
logging.config.dictConfig(yamlconfig)

# Logging
logger = logging.getLogger('main')
logging.addLevelName(15, "REVIEW")

if args.review:
    logger.setLevel(15)
if args.debug:
    logger.setLevel(10)

config = config.ConfigManager()
config.args = args

# print(config.rule_book)
# raise

match_queue = queue.Queue()
search_queue = queue.Queue()


search.searcher(config, search_queue)
if not search_queue.qsize() == 0:
    match.matcher(config, search_queue, match_queue)
    transfer.transferer(config, match_queue)
else:
    logger.info("No File System Entry detected")

if args.review:
    logger.info("Review done")
else:
    logger.info("App done")
