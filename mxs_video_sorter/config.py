import yaml
import os
import logging
import re
import subprocess
import shutil
import configparser
from collections import OrderedDict

logger = logging.getLogger('main')


class ConfigManager:
	"""A controller to access all the configs from the config files.
	- input_dir : Input Directory
	- series_dirs : [Series Directories]
	- ignore : List of File System Entries to ignore
	- rule_book : The rulebook to organize series
	"""
	def __init__(self):
		self.config_dir = os.path.join(os.environ['HOME'], '.config/mxs_video_sorter/')
		self._verify_config_dir()
		self._get_yamlconfig()
		self._run_before_scripts()
		self._verify_get_input_dir()
		self._verify_get_series_dirs()
		self._verify_get_movies_dirs()
		self.ignore = self.yamlconfig["ignore"]
		self.re_compile_file_extension = self._compile_video_file_extensions_pattern()
		self._get_rule_book()
		self._get_series_dirs_index()
		self._get_movies_groups()

	video_extension_list = ['mkv', 'm4v', 'avi', 'mp4', 'mov']

	def _get_movies_groups(self):
		"""Sets self.movies_sections as list
		{"movies::english":
			[{"option1", "value1"}, {"option2", "value2"}]
		}
		"""
		tempdict = OrderedDict()
		movies_sections_regex = re.compile('movies::', re.IGNORECASE)
		for section in self.rule_book.sections():
			if not movies_sections_regex.match(section):
				continue
			if section[8:] not in self.movies_dirs.keys():
				raise KeyError("Section {} doesn't exist in config.yaml".format(section))
			tempdict.update({section: []})
			for option in self.rule_book.options(section):
				value = self.rule_book.get(section, option)
				tempdict[section].append({option: value})

		logger.debug("got movies rule {}".format(tempdict))
		self.movies_groups = tempdict

	def _get_series_dirs_index(self):
		"""sets self.series_dirs_index as
		{"foldername": {"path": "...", "subdirs": [..., ...]}} of all
		output folder in config.yaml"""
		logger.debug("indexing output directories")
		tempdict = {}
		# List through listed output dirs
		for dir in self.series_dirs:
			dir = os.path.abspath(dir)

			# list through output dir
			for folder in os.listdir(dir):
				# Ignore not folders
				if not os.path.isdir(os.path.join(dir, folder)):
					logger.debug("skipped '{}' because its not a directory".format(folder))
					continue

				# Check incase duplicates found in series dirs
				if folder in tempdict:
					raise KeyError("Duplicate name {}".format(folder))

				# Adds to path
				tempdict[folder] = {}
				tempdict[folder]['path'] = os.path.join(dir, folder)
				path = tempdict[folder]['path']

				# list though current dir to get subdir
				tempdict[folder]['subdirs'] = []
				for subfolder in os.listdir(path):
					if not os.path.isdir(os.path.join(path, subfolder)):
						continue

					# Adds to subdir
					tempdict[folder]['subdirs'].append(subfolder)
		logger.debug("indexing done")
		self.series_dirs_index = tempdict

	def _get_rule_book(self):
		"""Sets self.rule_book as ConfigParser object on rule_book.conf"""
		config = configparser.ConfigParser(allow_no_value=True)
		config.read(os.path.join(self.config_dir + 'rule_book.conf'))
		logger.debug("got rule_book '{}'".format(dict(config)))
		self.rule_book = config

	def _get_yamlconfig(self):
		"""Sets self.yamlconfig as dict from config.yaml"""
		with open(os.path.join(self.config_dir, "config.yaml"), 'r') as ymlfile:
			self.yamlconfig = yaml.load(ymlfile)

	def _verify_config_dir(self):
		"""Checks if config dir exists and creates it if it didn't"""
		# if $HOME/.config/7m_video_sorter doesn't exists, create it
		if not os.path.exists(self.config_dir):
			logger.debug("config folder didn't exists, therefore created")
			os.makedirs(self.config_dir)

		for file in os.listdir("mxs_video_sorter/conf_template"):
			# if files in .conf doesn't exist in $HOME/.config/7m_video_sorter, create it
			if not os.path.exists(os.path.join(self.config_dir, file)):
				shutil.copyfile(os.path.join(
					"mxs_video_sorter/conf_template", file),
					os.path.join(self.config_dir, file))

	def _verify_get_series_dirs(self):
		"""Sets self.series_dirs as a list of all directories in config.yaml
		['path/to/output/dir/1', 'path/to/output/dir/2']"""
		dirs = []
		for dir in self.yamlconfig["series_dirs"]:
			if not dir:
				raise ValueError("Couldn't find series directories from config.yaml")
			if not os.path.exists(dir):
				raise ValueError("Series Directory '{}' doesn't exists".format(dirs))
			dirs.append(dir)
		logger.debug("got series dirs '{}'".format(dirs))
		self.series_dirs = dirs

	def _verify_get_movies_dirs(self):
		"""Sets self.movies_dirs from the config.yaml file as dict
		{"section": "path", ...}
		"""
		for name, dir in self.yamlconfig["movies_dirs"].items():
			if not dir:
				raise ValueError("Couldn't find movies directory from config.yaml")
			if not os.path.exists(dir):
				raise ValueError("{} doesn't exists".format(dir))
		logger.debug("got movies dirs {}".format(self.yamlconfig["movies_dirs"]))
		self.movies_dirs = self.yamlconfig["movies_dirs"]

	def _verify_get_input_dir(self):
		"""Sets self.input_dir as input_dir from the config.yaml file"""
		if not self.yamlconfig["input_dir"]:
			raise ValueError("Couldn't find input directory from config.yaml")
		if not os.path.exists(self.yamlconfig["input_dir"]):
			raise ValueError("{} doesn't exists".format(self.yamlconfig["input_dir"]))
		logger.debug("got input dir {}".format(self.yamlconfig["input_dir"]))
		self.input_dir = self.yamlconfig["input_dir"]

	def _compile_video_file_extensions_pattern(self):
		"""returns re.compile('^.*(\.mkv|\.mp4)$', re.IGNORECASE)"""
		extensions = self.video_extension_list
		output = '^.*('
		for extension in extensions:
			output = output + '\.' + extension + '|'
		output = output[:-1] + ")$"
		return re.compile("{}".format(output), re.IGNORECASE)

	def _run_before_scripts(self):
		"""Run before_scripts in config.yaml"""
		if not self.yamlconfig['before_scripts']:
			logger.debug("no before scripts to run")
			return
		for script in self.yamlconfig['before_scripts']:
			logger.debug("running before script '{}'".format(script))
			process = subprocess.Popen([script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			process.wait()
			logging.debug("script '{}' output: '{}'".format(script, process.communicate()))


if __name__ == "__main__":
	config = ConfigManager()
