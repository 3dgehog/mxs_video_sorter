import logging
import guessit
import difflib

from mxs_video_sorter.rules import series, movies

logger = logging.getLogger('main')


def matcher(config, search_queue, match_queue):
	logger.info("Matcher Running")

	while True:
		print('')

		if search_queue.qsize() == 0:
			logger.debug("end of search queue")
			break

		fse = search_queue.get()

		get_guessitmatch(fse)
		if not fse.valid:
			continue

		if fse.guessitmatch['type'] == 'episode':
			series_matcher(config, fse)
			if not fse.valid:
				continue

		if fse.guessitmatch['type'] == 'movie':
			movies_matcher(config, fse)
			if not fse.valid:
				continue

		logger.log(15, "{}".format(fse.guessitmatch))

		if not fse.transfer_to:
			logger.warn("No folder to transfer to")
			logger.warn("IGNORED")
			continue

		logger.log(15, "transfer_to = '{}'".format(fse.transfer_to))
		logger.info("MATCHED")

		logger.debug("fse '{}' added".format(fse.vfile.title))
		match_queue.put(fse)

	logger.info("Matcher Done")


def get_guessitmatch(fse):
	guessitmatch = guessit.guessit(fse.vfile.filename)
	if fse.isdir:
		guessitmatch_foldername = guessit.guessit(fse.fse)
		if len(guessitmatch_foldername) > len(guessitmatch):
			guessitmatch = guessitmatch_foldername
			logging.debug(
				"used foldername instead of filename for guessit match. \
				filename match = '{}' \nfoldername match = '{}'".format(
					guessitmatch, guessitmatch_foldername))
	fse.guessitmatch = guessitmatch
	try:
		fse.vfile.title = guessitmatch['title']
	except KeyError:
		logging.warning("error trying to find title for '{}'".format(fse.vfile.filename))
		logging.debug("error guessit match dict '{}'".format(fse.guessitmatch))
		fse.valid = False


def movies_matcher(config, fse):
	_header_with_title(fse)
	movies.get_sections(config, fse)
	# fse.transfer_to = config.movies_dir


def series_matcher(config, fse):
	series.get_rules(config, fse)
	series.matching_rules(config, fse)

	_header_with_title(fse)

	if not series.valid_title(config, fse):
		fse.valid = False

	index_match = difflib.get_close_matches(
		fse.vfile.title, config.series_dirs_index.keys(), n=1, cutoff=0.6)

	if not index_match:
		logger.warning("NO MATCH")
		fse.valid = False
	else:
		fse.matched_dirpath = config.series_dirs_index[index_match[0]]['path']
		fse.matched_dirname = index_match[0]
		fse.matched_subdirs = config.series_dirs_index[index_match[0]]['subdirs']

	series.transfer_rules(config, fse)


def _header_with_title(fse):
	logger.info('---' + fse.vfile.title + '---')
	logger.log(15, "{}".format(fse.vfile.filename))
