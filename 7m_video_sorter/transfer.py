import logging
import progressbar
import shutil
import time
import threading
import os

logger = logging.getLogger('main')


def transferer(config, match_queue):
	if config.args.review or not config.args.transfer:
		return
	bar = pbar(match_queue.qsize())
	global counter
	counter = 0
	_pbar_thread = threading.Thread(target=_pbar_run, args=(bar,), daemon=True)
	_pbar_thread.start()
	while True:
		if match_queue.qsize() == 0:
			bar.finish()
			logger.debug("end of match queue")
			break

		fse = match_queue.get()
		logging.info("Working on {}".format(fse.vfile.title))

		# Update ProgressBar
		counter += 1

		copy(config, fse)

		bar.update(counter)
		logging.debug("copied to: '{}'".format(fse.transfer_to))

	logger.info("Transferer Done")


def copy(config, fse):
	shutil.copy(fse.vfile.abspath, fse.transfer_to)
	if not os.path.exists(os.path.join(fse.transfer_to, fse.vfile.filename)):
		logger.critical("The file {} was copied but doesn't exist in copied location".format(fse.vfile.filename))
		raise Exception("The file {} was copied but doesn't exist in copied location".format(fse.vfile.filename))
	logging.info("COPIED")
	if config.args.prevent_delete:
		return
	# remove directory or simple file
	if fse.isdir:
		shutil.rmtree(fse.path_to_fse)
	else:
		os.remove(fse.path_to_fse)
	logging.info("DELETED FROM SOURCE")
	logging.debug("fse removed")


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


def _pbar_run(bar):
	while True:
		bar.update(counter)
		time.sleep(2)
