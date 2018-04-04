import logging
import difflib
import os
import re

logger = logging.getLogger('main')

available_rules = [
	'parent-dir',
	'subdir-only',
	'parent-dir',
	'season',
	'episode-only',
	'alt-title'
]

DIFF_CUTOFF = 0.7


def get_rules(config, fse):
	fse.rules = None
	diffmatch = difflib.get_close_matches(fse.vfile.title, config.rule_book.options('rules'), n=1, cutoff=DIFF_CUTOFF)
	regex_compile = re.compile("{}".format(fse.vfile.title), re.IGNORECASE)
	regexmatch = list(filter(regex_compile.match, config.rule_book.options('rules')))
	if diffmatch or regexmatch:
		if diffmatch:
			rules = config.rule_book.get('rules', diffmatch[0])
		if regexmatch:
			rules = config.rule_book.get('rules', regexmatch[0])
		if rules:
			rules = rules.split(' ')
			invalid_rule_patterns(rules)
			fse.rules = rules
		else:
			fse.rules = None
			logger.warning("No rules set")
	logger.debug("rules = {}".format(fse.rules))


# Before Matching
def matching_rules(config, fse):
	if not fse.rules:
		return
	if 'alt-title' in fse.rules:
		if 'alternative_title' in fse.gtmatch:  # REVIEW: Nonetype error
			try:
				separator = fse.rules[fse.rules.index('alt-title') + 1].replace(":", " ")
			except IndexError:
				raise KeyError("Missing separator for alt-title")
			if separator in available_rules:
				raise KeyError("Missing separator for alt-title")
			fse.vfile.title = \
				fse.gtmatch['title'] + separator + fse.gtmatch['alternative_title']
			logger.log(15, "rule 'alt-title' OK")
		else:
			logger.warning("rule 'alt-title' WARN, no alternative_title key found")


def valid_title(config, fse):
	if not difflib.get_close_matches(fse.vfile.title, config.rule_book.options('rules'), n=1, cutoff=DIFF_CUTOFF):
		logger.warning('NOT IN LIST')
		if config.args.review:
			return True
		return False
	return True


# Before Transfering
def transfer_rules(config, fse, output_index):
	fse.transfer_to = None
	fse = rule_commands(config, fse, output_index)


def rule_commands(config, fse, output_index):
	if not fse.rules:
		return
	if 'episode-only' in fse.rules:
		try:
			fse.gtmatch['episode'] = int(str(fse.gtmatch['season']) + str(fse.gtmatch['episode']))
		except KeyError:
			logger.debug("error episode-only merging, missing season key")
			pass
		fse.gtmatch.pop('season', None)
		logger.log(15, "rule 'episode-only' OK")

	if 'parent-dir' in fse.rules:
		fse.transfer_to = fse.matched_dirpath
		logger.log(15, "rule 'parent-dir' OK")

	if 'subdir-only' in fse.rules:
		subdir_index = fse.rules.index('subdir-only') + 1
		subdir = fse.rules[subdir_index].replace(':', ' ')
		if subdir not in fse.matched_subdirs:
			logger.warning("rule 'subdir-only' WARN > subdir '{}' doesn't exists".format(subdir))
		else:
			fse.transfer_to = os.path.join(fse.matched_dirpath, subdir)
			logger.log(15, "rule 'subdir-only' OK")

	if 'season' in fse.rules:
		if 'season' not in fse.gtmatch:
			logger.warning("rule 'season' WARN > Couldn't find Season from filename")
		else:
			season = str(fse.gtmatch['season'])
			for subdir in fse.matched_subdirs:
				search = re.search("^Season {}".format(season), subdir, re.IGNORECASE)
				if search:
					fse.transfer_to = os.path.join(fse.matched_dirpath, subdir)
					logger.log(15, "rule 'season' OK")
			if not fse.transfer_to and not config.args.create_dir:
				logger.warning("rule 'season' WARN > Couldn't find Season {} folder".format(season))
			elif not fse.transfer_to and config.args.create_dir:
				path_to_new_dir = os.path.join(fse.matched_dirpath, "Season {}".format(season))
				os.mkdir(path_to_new_dir)
				output_index[fse.matched_dirname]["subdirs"].append(os.path.basename(path_to_new_dir))
				logger.info("Created directory: '{}' ".format(path_to_new_dir))
				fse.transfer_to = path_to_new_dir
				logger.log(15, "rule 'season' OK")


def invalid_rule_patterns(rules):
	for rule in rules:
		if rule not in available_rules:
			if not rules[rules.index(rule) - 1] != 'subdir-only':
				continue
			if not rules[rules.index(rule) - 1] != 'alt-title':
				continue
			raise KeyError("Invalid rule : '{}'".format(rule))

	invalid_matches = [
		['subdir-only', 'parent-dir'],
		['season', 'subdir-only'],
		['season', 'parent-dir']
	]
	for invalid_match in invalid_matches:
		if all(item in rules for item in invalid_match):
			raise KeyError("Invalid rule pairing: {}".format(rules))
