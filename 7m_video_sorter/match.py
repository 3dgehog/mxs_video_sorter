import logging
import os
import guessit
import difflib

import rules

logger = logging.getLogger('main')


def matcher(config, search_queue, match_queue):
	logger.info("Matcher Running")
	series_dirs_index = _index_series_dirs(config)

	while True:
		print('')

		if search_queue.qsize() == 0:
			logger.debug("end of search queue")
			break

		fse = search_queue.get()

		gtmatch = guessit.guessit(fse.vfile.filename)
		fse.vfile.gtmatch = gtmatch
		fse.vfile.title = gtmatch['title']

		if fse.vfile.gtmatch['type'] == 'episode':
			series_matcher(config, fse, series_dirs_index)
			if not fse.valid:
				continue

		logger.log(15, "{}".format(fse.vfile.gtmatch))

		if not fse.transfer_to:
			logger.warn("No folder to transfer to")
			logger.warn("IGNORED")
			continue

		logger.log(15, "transfer_to = '{}'".format(fse.transfer_to))
		logger.info("MATCHED")

		logger.debug("fse '{}' added".format(fse.vfile.title))
		match_queue.put(fse)

	logger.info("Matcher Done")


def series_matcher(config, fse, series_dirs_index):
	rules.get_series_rules(config, fse)
	rules.series_matching_rules(config, fse)

	_header_with_title(fse)

	if not rules.series_valid_title(config, fse):
		fse.valid = False

	index_match = difflib.get_close_matches(
		fse.vfile.title, series_dirs_index.keys(), n=1, cutoff=0.6)

	if not index_match:
		logger.warning("NO MATCH")
		fse.valid = False
	else:
		fse.matched_dirpath = series_dirs_index[index_match[0]]['path']
		fse.matched_dirname = index_match[0]
		fse.matched_subdirs = series_dirs_index[index_match[0]]['subdirs']

	rules.series_transfer_rules(config, fse, series_dirs_index)


def _header_with_title(fse):
	logger.info('---' + fse.vfile.title + '---')
	logger.log(15, "{}".format(fse.vfile.filename))


def _index_series_dirs(config):
	logger.debug("indexing output directories")
	"""returns {"foldername": {"path": "...", "subdirs": [..., ...]}} of all
	output folder in config.yaml"""
	tempdict = {}
	# List through listed output dirs
	for dir in config.series_dirs:
		dir = os.path.abspath(dir)

		# list through output dir
		for folder in os.listdir(dir):
			# Ignore not folders
			if not os.path.isdir(os.path.join(dir, folder)):
				logger.debug("skipped '{}' because its not a directory".format(folder))
				continue

			# Check incase duplicates found in series dirs
			if folder in tempdict:
				raise KeyError("Duplicate name {}".format(folder))

			# Adds to path
			tempdict[folder] = {}
			tempdict[folder]['path'] = os.path.join(dir, folder)
			path = tempdict[folder]['path']

			# list though current dir to get subdir
			tempdict[folder]['subdirs'] = []
			for subfolder in os.listdir(path):
				if not os.path.isdir(os.path.join(path, subfolder)):
					continue

				# Adds to subdir
				tempdict[folder]['subdirs'].append(subfolder)
	logger.debug("indexing done")
	return tempdict
