import logging
import os
from guess_language import guess_language

logger = logging.getLogger('main')


valid_movies_rules = [
	'language',
]


def transfer_rules(config, fse):
	_fix_language(fse)
	_fix_release_group(fse)
	_find_movies_group(config, fse)
	if not fse.movies_rbook_group:
		logger.warn("Unable to group")
		return
	config_section = fse.movies_rbook_group[8:]
	for groupname, path in config.movies_dirs.items():
		if groupname == config_section:
			fse.transfer_to = path
	if fse.isdir:
		logger.debug("movie is in a directory, changing tranfer_to")
		fse.transfer_to = os.path.join(path, fse.fse)


def _find_movies_group(config, fse):
	for group, options in config.movies_groups.items():
		logger.debug("options : {}".format(options))
		for option in options:
			if 'language' in option.keys():
				if option['language'] == fse.guessitmatch['language']:
					fse.movies_rbook_group = group
					logger.log(15, "group: '{}' <-- language".format(fse.movies_rbook_group[8:]))
					return

			if 'release_group' in option.keys():
				if option['release_group'] == fse.guessitmatch['release_group']:
					fse.movies_rbook_group = group
					logger.log(15, "group: '{}' <-- release_group".format(fse.movies_rbook_group[8:]))
					return


def _fix_language(fse):
	if 'language' in fse.guessitmatch:
		fse.guessitmatch['language'] = str(fse.guessitmatch['language'])
	else:
		fse.guessitmatch['language'] = guess_language(fse.guessitmatch['title'])


def _fix_release_group(fse):
	if 'release_group' not in fse.guessitmatch:
		fse.guessitmatch['release_group'] = None
