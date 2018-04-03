import yaml
import os
import logging
import re
import subprocess
import shutil
import configparser

logger = logging.getLogger('main')


class ConfigManager:
    """A controller to access all the configs from the config files.
    - input_dir : Input Directory
    - output_dirs : [Output Directories]
    - ignore : List of File System Entries to ignore
    - valid_list: List of all valid shows from valid_list"""
    def __init__(self):
        self.config_dir = os.path.join(os.environ['HOME'], '.config/7m_video_sorter/')
        self._verify_config_dir()
        self._get_yamlconfig()
        self._run_before_scripts()
        self._verify_get_input_dir()
        self._verify_get_output_dir()
        self.ignore = self.yamlconfig["ignore"]
        self.re_compile_file_extension = self._compile_video_file_extensions_pattern()
        self._get_rule_book()

    video_extension_list = ['mkv', 'm4v', 'avi', 'mp4']

    def _get_rule_book(self):
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(os.path.join(self.config_dir + 'rule_book.conf'))
        self.rule_book = config

    def _get_yamlconfig(self):
        with open(os.path.join(self.config_dir, "config.yaml"), 'r') as ymlfile:
            self.yamlconfig = yaml.load(ymlfile)

    def _verify_config_dir(self):
        # if $HOME/.config/7m_video_sorter doesn't exists, create it
        if not os.path.exists(self.config_dir):
            logger.debug("config folder didn't exists, therefore created")
            os.makedirs(self.config_dir)

        for file in os.listdir("7m_video_sorter/.conf"):
            # if files in .conf doesn't exist in $HOME/.config/7m_video_sorter, create it
            if not os.path.exists(os.path.join(self.config_dir, file)):
                shutil.copyfile(os.path.join("7m_video_sorter/.conf", file),
                                os.path.join(self.config_dir, file))

    def _verify_get_output_dir(self):
        dirs = []
        for dir in self.yamlconfig["output_dirs"]:
            if not dir:
                raise ValueError("Couldn't find output directories from config.yaml")
            if not os.path.exists(dir):
                raise ValueError("Output Directory '{}' doesn't exists".format(dirs))
            dirs.append(dir)
        logger.debug("got output dirs '{}'".format(dirs))
        self.output_dirs = dirs

    def _verify_get_input_dir(self):
        """Returns input_dir from the config.yaml file"""
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
