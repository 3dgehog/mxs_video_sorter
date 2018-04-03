import logging
import difflib
import os
import re

logger = logging.getLogger('main')

DIFF_CUTOFF = 0.7


# Before Matching
def before_index_match(config, fse):
	if 'alternative_title' in fse.gtmatch:
		fse.vfile.title = fse.gtmatch['title'] + " - " + fse.gtmatch['alternative_title']
	return fse


def valid_title(config, fse):
	if not difflib.get_close_matches(fse.vfile.title, config.rule_book.options('rules'), n=1, cutoff=DIFF_CUTOFF):
		logger.warning('NOT IN LIST')
		if config.args.review:
			return True
		return False
	return True


# Before Transfering
def transfer_rules(config, fse):
	fse.transfer_to = None
	diffmatch = difflib.get_close_matches(fse.vfile.title, config.rule_book.options('rules'), n=1, cutoff=DIFF_CUTOFF)
	if diffmatch:
		rules = config.rule_book.get('rules', diffmatch[0])
		if rules:
			rules = rules.split(' ')
			fse = rule_commands(fse, rules)
	else:
		logger.log(15, "rule None")
	return fse


def rule_commands(fse, rules):
	logger.debug("rules = {}".format(rules))
	invalid_rule_patterns(rules)
	if 'episode-only' in rules:
		try:
			fse.gtmatch['episode'] = int(str(fse.gtmatch['season']) + str(fse.gtmatch['episode']))
		except KeyError:
			pass
		fse.gtmatch.pop('season', None)
		logger.log(15, "rule 'episode-only' OK")

	if 'parent-dir' in rules:
		fse.transfer_to = fse.matched_dirpath
		logger.log(15, "rule 'parent-dir' OK")

	if 'subdir-only' in rules:
		subdir_index = rules.index('subdir-only') + 1
		subdir = rules[subdir_index].replace(':', ' ')
		if subdir not in fse.matched_subdirs:
			raise KeyError("Subdir '{}' doesn't exists".format(subdir))
		fse.transfer_to = os.path.join(fse.matched_dirpath, subdir)
		logger.log(15, "rule 'subdir-only' OK")

	if 'season' in rules:
		if 'season' not in fse.gtmatch:
			logger.warning("rule 'season' WARN > Couldn't find Season from filename")
		else:
			season = str(fse.gtmatch['season'])
			for subdir in fse.matched_subdirs:
				search = re.search("^Season {}".format(season), subdir, re.IGNORECASE)
				if search:
					fse.transfer_to = os.path.join(fse.matched_dirpath, subdir)
					logger.log(15, "rule 'season' OK")
			if not search:
				logger.warning("rule 'season' WARN > Couldn't find Season {} folder".format(season))
	return fse


def invalid_rule_patterns(rules):
	invalid_matches = [
		['subdir-only', 'parent-dir'],
		['season', 'subdir-only'],
		['season', 'parent-dir']
	]
	for invalid_match in invalid_matches:
		if all(item in rules for item in invalid_match):
			raise KeyError("Invalid rule pairing: {}".format(rules))
