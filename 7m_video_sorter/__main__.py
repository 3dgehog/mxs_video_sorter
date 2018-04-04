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

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--transfer",
                    help="Pass this argument to make the transfer",
                    action="store_true")
parser.add_argument("-r", "--review",
                    help="Runs through all files in output dir for review, doesn't transfer anything",
                    action="store_true")
parser.add_argument("-c", "--create-dir",
                    help="Creates Season # dir if it doesn't exists",
                    action="store_true")
parser.add_argument("-d", "--debug",
                    help="Run all debug logs",
                    action="store_true")
parser.add_argument("-p", "--prevent-delete",
                    help="Doesn't delete file after being transfered",
                    action="store_true")
args = parser.parse_args()

# fix progressbar with logging
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

# Configs
config = config.ConfigManager()
config.args = args
logger.debug("args passed: {}".format(args))

# Queues
match_queue = queue.Queue()
search_queue = queue.Queue()

# Searcher, Matcher, Trasnferer
search.searcher(config, search_queue)
if not search_queue.qsize() == 0:
    match.matcher(config, search_queue, match_queue)
    transfer.transferer(config, match_queue)
else:
    logger.info("No File System Entry detected")

if args.review:
    logger.info("Review Done")
else:
    logger.info("App Done")
