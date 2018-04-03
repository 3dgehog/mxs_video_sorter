import logging
import progressbar
import shutil
import time
import threading

logger = logging.getLogger('main')


def transferer(config, match_queue):
	bar = pbar(match_queue.qsize())
	global counter
	counter = 0
	_pbar_thread = threading.Thread(target=pbar_run, args=(bar,), daemon=True)
	_pbar_thread.start()
	while True:
		if config.args.review:
			break

		if match_queue.qsize() == 0:
			bar.finish()
			logger.debug("end of match queue")
			break

		fse = match_queue.get()
		logging.info("Working on {}".format(fse.vfile.title))

		# Update ProgressBar
		counter += 1

		time.sleep(0.5)

		bar.update(counter)
		logging.info("Copy Successful")

	logger.info("Transferer Done")


def pbar(full_queue_size):
	widgets = [
		progressbar.AnimatedMarker(),
		" ",
		progressbar.Percentage(),
		' (',
		progressbar.SimpleProgress(),
		') ',
		progressbar.Bar(marker='=', left='[', right=']', fill='-'),
		progressbar.Timer(format=' %(elapsed)s')
	]
	return progressbar.ProgressBar(widgets=widgets, max_value=full_queue_size)


def pbar_run(bar):
	while True:
		bar.update(counter)
		time.sleep(2)
