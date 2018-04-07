import re
import logging

logger = logging.getLogger('main')


valid_movies_rules = [
	'language',
]

movies_regex = re.compile('^movies::', re.IGNORECASE)


def get_sections(config, fse):
	"""Gets rules and adds them in a dict"""
	sections = config.rule_book.sections()
	for section in sections:
		if not movies_regex.match(section):
			del sections[sections.index(section)]
			continue
		if section[8:] not in config.movies_dirs.keys():
			raise KeyError("Section {} doesn't exist in config.yaml".format(section))
	logger.debug("sections = {}".format(sections))
	fse.sections = sections
