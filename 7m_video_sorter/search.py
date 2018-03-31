import os
import logging
from file_system_entry import FileSystemEntry
# import re

logger = logging.getLogger('main')


def search(config, search_queue):
    for item in os.listdir(config.input_dir):

        # Ignore config ignore files
        if item in config.ignore:
            logger.debug("item {} ignored".format(item))
            continue

        # Create File System Entry
        fse = FileSystemEntry(config, item)

        # Add FSE to queue is its valid
        if fse.valid:
            logger.debug("item {} added to search queue".format(item))
            search_queue.put(fse)

    # Send 'end' signal
    search_queue.put("end")
    logger.info("Search Done")
