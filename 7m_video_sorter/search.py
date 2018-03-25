import os
import logging
# import re

logger = logging.getLogger('main')


def search_dir(config, search_queue):
    for item in os.listdir(config.input_dir):
        if item in config.file_ignore:
            logger.debug("ignored item {}".format(item))
            continue
        logger.debug("working on item {}".format(item))
        seaobj = SearchObject(os.path.join(config, item))
        if seaobj.valid:
            logger.debug("item {} added to search queue".format(item))
            search_queue.put(seaobj)


class SearchObject:
    def __init__(self, config, item):
        self.config = config
        self.path = os.path.join(config.input_dir, item)
        self.item = item
        self.dirname = config.input_dir
        self.get_info()

    def get_info(self):
        """Attributes are:
        - valid (if its a valid file)
        - isdir (if its a directory)
        - vfile (video files)
        """
        self.valid = False
        self.isdir = os.path.isdir(self.path)

        if self.isdir:
            for item in os.listdir(self.path):
                # if secondary directory, ignore
                if os.path.join(self.item, item):
                    continue

                # if file has file extension
                if self.config.regex_file_extensions_pattern.match(self.item):
                    # if file was already valid, break and set to not valid
                    # reason: does not support multiple files right now!!
                    if self.valid:
                        self.valid = False
                        break
                    self.vfile = item
                    self.valid = True

        else:
            # check if the file found has a valid file extension
            if self.config.regex_file_extensions_pattern.match(self.item):
                self.vfile = self.item
                self.valid = True
