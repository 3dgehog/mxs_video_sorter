import logging

logger = logging.getLogger('main')


# Before Matching
def before_matching(config, match, fse):
	return fse


def valid_title(config, match, fse):
	for title in config.rule_book.options('title'):
		if fse.vfile.title.upper() != title.upper():
			logger.debug('***NOT IN LIST***')
			if config.args.review:
				break
			return False
	return True


# Before Transfering
def before_transfering():
	pass
