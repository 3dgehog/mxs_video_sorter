import logging
import difflib
import os
import re
import shlex
import guessit

logger = logging.getLogger('main')

valid_series_rules = [
	'parent-dir',
	'subdir-only',
	'parent-dir',
	'season',
	'episode-only',
	'alt-title',
	'format-title',
	'no-proper'
]

DIFF_CUTOFF = 0.7


def get_rules(config, fse):
	diffmatch = difflib.get_close_matches(fse.vfile.title, config.rule_book.options('series_rules'), n=1, cutoff=DIFF_CUTOFF)
	regex_compile = re.compile("{}".format(fse.vfile.title), re.IGNORECASE)
	regexmatch = list(filter(regex_compile.match, config.rule_book.options('series_rules')))
	if diffmatch or regexmatch:
		if diffmatch:
			rules = config.rule_book.get('series_rules', diffmatch[0])
		if regexmatch:
			rules = config.rule_book.get('series_rules', regexmatch[0])
		if rules:
			rules = shlex.split(rules)
			_invalid_rule_check(rules)
			fse.rules = rules
		else:
			logger.warning("No rules set")
	logger.debug("rules = {}".format(fse.rules))


# Before Matching
def after_matching_rules(config, fse):
	if not fse.rules:
		return
	if 'alt-title' in fse.rules:
		if 'alternative_title' in fse.guessitmatch:
			try:
				separator = fse.rules[fse.rules.index('alt-title') + 1].replace(":", " ")
			except IndexError:
				raise KeyError("Missing separator for alt-title")
			if separator in valid_series_rules:
				raise KeyError("Missing separator for alt-title")
			fse.vfile.title = \
				fse.guessitmatch['title'] + separator + fse.guessitmatch['alternative_title']
			logger.log(15, "rule 'alt-title' OK")
		else:
			logger.warning("rule 'alt-title' WARN, no alternative_title key found")


def valid_title(config, fse):
	if not difflib.get_close_matches(fse.vfile.title, config.rule_book.options('series_rules'), n=1, cutoff=DIFF_CUTOFF):
		logger.warning('NOT IN LIST')
		if config.args.review:
			return True
		return False
	return True


# Before Transfering
def before_transfer_rules(config, fse):
	if not fse.rules:
		return
	if 'episode-only' in fse.rules:
		try:
			fse.guessitmatch['episode'] = int(str(fse.guessitmatch['season']) + str(fse.guessitmatch['episode']))
		except KeyError:
			logger.debug("error episode-only merging, missing season key")
			pass
		fse.guessitmatch.pop('season', None)
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
		if 'season' not in fse.guessitmatch:
			logger.warning("rule 'season' WARN > Couldn't find Season from filename")
		else:
			season = str(fse.guessitmatch['season'])
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
				config.series_dirs_index[fse.matched_dirname]["subdirs"].append(os.path.basename(path_to_new_dir))
				logger.info("Created directory: '{}' ".format(path_to_new_dir))
				fse.transfer_to = path_to_new_dir
				logger.log(15, "rule 'season' OK")

	if 'format-title' in fse.rules:
		guessit_dict = dict(fse.guessitmatch)
		titles = guessit_dict['title'].split(' ')
		count = 1
		temp_dict = {}
		for title in titles:
			temp_dict['title' + str(count)] = title
			count += 1
		guessit_dict = _merge_two_dicts(guessit_dict, temp_dict)
		format_index = fse.rules.index('format-title') + 1
		newname = fse.rules[format_index].replace('&', '%') % (guessit_dict) + \
			"." + guessit_dict['container']
		fse.transfer_to = os.path.join(fse.transfer_to, newname)
		logger.log(15, "rule 'format-title' OK")


def during_transfer_rules(config, fse):
	if 'no-proper' not in fse.rules:
		if not os.path.isdir(fse.transfer_to):
			transfer_to = os.path.dirname(fse.transfer_to)
		else:
			transfer_to = fse.transfer_to

		for existing in transfer_to:
			existing_guessitmatch = guessit.guessit(existing)
			try:
				if existing_guessitmatch['episode'] != fse.guessitmatch['episode']:
					continue
			except KeyError:
				continue
			fse_obj = False
			ext_obj = False
			logger.debug("same episode found")
			if 'proper_count' in fse.guessitmatch:
				fse_obj = True
			if 'proper_count' in existing_guessitmatch:
				ext_obj = True
			if fse_obj and ext_obj:
				logger.debug("both are proper, favoring the new")
				fse.replace = os.path.join(transfer_to, existing)

			elif fse_obj and not ext_obj:
				logger.debug("this file proper, existing isn't")
				fse.replace = os.path.join(transfer_to, existing)

			elif ext_obj and not fse_obj:
				logger.debug("this file isn't proper, existing is")
				fse.transfer_to = None

			else:
				logger.debug("both are normal, favoring the new")
				fse.replace = os.path.join(fse.transfer_to, existing)
			break
		logger.log(15, "rule 'proper' OK")

		# if 'proper_count' in fse.guessitmatch:
		# 	logger.debug("this episode is proper")
		# 	for item in os.listdir(fse.transfer_to):
		# 		item_guessitmatch = guessit.guessit(item)
		# 		try:
		# 			if item_guessitmatch['episode'] != fse.guessitmatch['episode']:
		# 				continue
		# 			logger.debug("same episode found")
		# 			if 'proper_count' not in item_guessitmatch:
		# 				fse.replace = os.path.join(fse.transfer_to, item)
		# 				logger.log(11, "replacing episode {} with {}".format(
		# 					item, fse.vfile.filename
		# 				))
		# 				continue
		# 			logger.warn("both episode are same and proper... ignoring")
		# 		except KeyError:
		# 			continue


def _invalid_rule_check(rules):
	for rule in rules:
		if rule not in valid_series_rules:
			if not rules[rules.index(rule) - 1] != 'subdir-only':
				continue
			if not rules[rules.index(rule) - 1] != 'alt-title':
				continue
			if not rules[rules.index(rule) - 1] != 'format-title':
				continue
			raise KeyError("Invalid series rule: '{}'".format(rule))

	invalid_series_rule_pairs = [
		['subdir-only', 'parent-dir'],
		['season', 'subdir-only'],
		['season', 'parent-dir']
	]
	for invalid_pair in invalid_series_rule_pairs:
		if all(item in rules for item in invalid_pair):
			raise KeyError("Invalid rule pairing: {}".format(rules))


def _merge_two_dicts(x, y):
	z = x.copy()
	z.update(y)
	return z
