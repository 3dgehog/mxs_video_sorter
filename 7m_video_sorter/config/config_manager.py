import yaml
import os
import logging
import re
import subprocess

logger = logging.getLogger('main')


class ConfigManager:
    """A controller to access all the configs from the config files.
    - input_dir : Input Directory
    - output_dir : [Output Directories]
    - ignore : List of File System Entries to ignore"""
    def __init__(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                  "config.yaml"), 'r') as ymlfile:
            self.yamlconfig = yaml.load(ymlfile)
        self._before_scripts()
        self.input_dir = self._get_input_dir()
        self.output_dirs = self._get_output_dir()
        self.ignore = self.yamlconfig["ignore"]
        self.re_compile_file_extension = self._compile_video_file_extensions_pattern()
        self.valid_list = self._make_valid_list()

    video_extension_list = ['mkv', 'm4v', 'avi', 'mp4']

    def _make_valid_list(self):
        with open(self.yamlconfig['valid_list']) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            content = [x.upper() for x in content]
            return content

    def _get_output_dir(self):
        dirs = []
        for dir in self.yamlconfig["output_dirs"]:
            if not dir:
                raise ValueError("Couldn't find output directories from config.yaml")
            if not os.path.exists(dir):
                raise ValueError("Output Directory '{}' doesn't exists".format(dirs))
            dirs.append(dir)
        logger.debug("got output dirs '{}'".format(dirs))
        return dirs

    def _get_input_dir(self):
        """Returns input_dir from the config.yaml file"""
        if not self.yamlconfig["input_dir"]:
            raise ValueError("Couldn't find input directory from config.yaml")
        if not os.path.exists(self.yamlconfig["input_dir"]):
            raise ValueError("{} doesn't exists".format(self.yamlconfig["input_dir"]))
        logger.debug("got input dir {}".format(self.yamlconfig["input_dir"]))
        return self.yamlconfig["input_dir"]

    def _compile_video_file_extensions_pattern(self):
        """returns re.compile('^.*(\.mkv|\.mp4)$', re.IGNORECASE)"""
        extensions = self.video_extension_list
        output = '^.*('
        for extension in extensions:
            output = output + '\.' + extension + '|'
        output = output[:-1] + ")$"
        return re.compile("{}".format(output), re.IGNORECASE)

    def _before_scripts(self):
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
