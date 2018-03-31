import logging
import os
import guessit

logger = logging.getLogger('main')


def match(config, search_queue, match_queue):
	output_index = _index_output_file(config)
	while True:
		fse = search_queue.get()

		if fse == "end":
			logger.debug("received 'end' signal, breaking the match loop")
			break

		match = guessit.guessit(fse.vfile)


def _index_output_file(config):
	"""returns {"foldername": "path", ...} of all output folder in config.yaml"""
	tempdict = {}
	for dir in config.output_dirs:
		dir = os.path.abspath(dir)
		for folder in os.listdir(dir):
			if not os.path.isdir(os.path.join(dir, folder)):
				logging.debug("skipped '{}' because its not a directory".format(folder))
				continue
			if folder in tempdict:
				raise KeyError("Duplicate name {}".format(folder))
			tempdict[folder] = os.path.join(dir, folder)
	return tempdict
