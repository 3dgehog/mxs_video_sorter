import os
import logging
from mxs_video_sorter.file_system_entry import FileSystemEntry

logger = logging.getLogger('main')


def searcher(config, search_queue):
    logger.info("Searcher Running")
    for item in os.listdir(config.input_dir):

        # Ignore config ignore files
        if item in config.ignore:
            logger.debug("fse '{}' ignored".format(item))
            continue

        # Create File System Entry
        fse = FileSystemEntry(config, item)

        # Add FSE to queue is its valid
        if fse.valid:
            logger.debug("fse '{}' added".format(item))
            search_queue.put(fse)
        else:
            logger.debug("invalid fse {}".format(fse.fse))

    logger.info("Searcher Done")
