import logging
import os
import guessit
import difflib

import rules

logger = logging.getLogger('main')


def matcher(config, search_queue, match_queue):
	logger.debug("Matcher Running")
	output_index = _index_output_dirs(config)
	# search_queue.qsize()
	while True:
		if search_queue.qsize() == 0:
			logger.debug("end of search queue")
			break

		fse = search_queue.get()

		match = guessit.guessit(fse.vfile.filename)
		fse.vfile.title = match['title']

		fse = rules.before_matching(config, match, fse)

		logger.debug('---' + fse.vfile.title + '---')

		if not fse.vfile.title.upper() in config.valid_list:
			logger.debug('***NOT IN LIST***')
			if not config.args.review:
				continue

		diffmatch = difflib.get_close_matches(fse.vfile.title, output_index.keys(), n=1)
		if not diffmatch:
			logger.debug("***NO MATCH***")
			continue

		logger.debug(fse.vfile.title + " >>> " + diffmatch[0])
	logger.info("Matcher Done")


def _index_output_dirs(config):
	"""returns {"foldername": {"path": "...", "subdirs": [..., ...]}} of all
	output folder in config.yaml"""
	tempdict = {}
	# List through listed output dirs
	for dir in config.output_dirs:
		dir = os.path.abspath(dir)

		# list through output dir
		for folder in os.listdir(dir):
			# Ignore not folders
			if not os.path.isdir(os.path.join(dir, folder)):
				logger.debug("skipped '{}' because its not a directory".format(folder))
				continue

			# Check incase duplicates found in output dirs
			if folder in tempdict:
				raise KeyError("Duplicate name {}".format(folder))

			# Adds to path
			tempdict[folder] = {}
			tempdict[folder]['path'] = os.path.join(dir, folder)
			path = tempdict[folder]['path']

			# list though current dir to get subdir
			tempdict[folder]['subdir'] = []
			for subfolder in os.listdir(path):
				if not os.path.isdir(os.path.join(path, subfolder)):
					continue

				# Adds to subdir
				tempdict[folder]['subdir'].append(subfolder)

	return tempdict
