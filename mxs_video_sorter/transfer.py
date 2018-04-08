import logging
import progressbar
import shutil
import time
import threading
import os

logger = logging.getLogger('main')


def transferer(config, match_queue):
	logger.info("Transferer Running")

	global counter
	counter = 0
	full_queue_size = match_queue.qsize()

	if config.args.transfer and not config.args.review and not \
		config.args.no_output and config.args.progressbar:
		logger.debug("Progress Bar thread started")
		bar = pbar_widgets(full_queue_size)
		_pbar_thread = threading.Thread(target=_pbar_run, args=(bar,), daemon=True)
		_pbar_thread.start()
	else:
		_pbar_thread = None

	while True:
		counter += 1

		if match_queue.qsize() == 0:
			if _pbar_thread:
				if _pbar_thread.is_alive():
					bar.finish()
			logger.debug("end of match queue")
			break

		fse = match_queue.get()

		if config.args.review and not config.args.no_output:
			logger.log(15, "{} --> {}".format(fse.vfile.filename, fse.transfer_to))
			input("({} of {}) Press Enter to continue".format(counter, full_queue_size))
			continue

		if not config.args.transfer:
			logger.warning("Nothing was transfered because argument '-t' wasn't called")
			break

		logger.info("Working on {}".format(fse.vfile.filename))

		copy(config, fse)

		if _pbar_thread:
			bar.update(counter)

	logger.info("Transferer Done")


def copy(config, fse):
	if fse.guessitmatch['type'] == 'episode':
		logger.debug("copying: '{}' to: '{}'".format(fse.vfile.filename, fse.transfer_to))
		shutil.copy(fse.vfile.abspath, fse.transfer_to)

	if fse.guessitmatch['type'] == 'movie':
		if fse.isdir:
			logger.debug("copying: '{}' to: '{}'".format(fse.fse, fse.transfer_to))
			shutil.copytree(fse.path_to_fse, fse.transfer_to)
		else:
			logger.debug("copying: '{}' to: '{}'".format(fse.vfile.filename, fse.transfer_to))
			shutil.copy(fse.vfile.abspath, fse.transfer_to)

	logger.info("COPIED")

	if not config.args.delete:
		return
	if fse.isdir:
		shutil.rmtree(fse.path_to_fse)
	else:
		os.remove(fse.path_to_fse)
	logger.info("DELETED")


def pbar_widgets(full_queue_size):
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


def _pbar_run(bar):
	while True:
		bar.update(counter)
		time.sleep(2)
