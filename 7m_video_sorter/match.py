import logging
import guessit

logger = logging.getLogger('main')


def match(config, search_queue, match_queue):
	while True:
		fse = search_queue.get()

		if fse == "end":
			logger.debug("received 'end' signal, breaking the match loop")
			break

		match = guessit.guessit(fse.vfile)
