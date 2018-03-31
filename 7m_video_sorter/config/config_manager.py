import yaml
import os
import logging
import re

logger = logging.getLogger('main')


class ConfigManager:
    """A controller to access all the configs from the config files.
    - input_dir : Input Directory
    - output_dir : Output Directory
    - ignore : List of File System Entries to out right ignore"""
    def __init__(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                  "config.yaml"), 'r') as ymlfile:
            self.yamlconfig = yaml.load(ymlfile)
        self.input_dir, self.output_dir = self._get_dirs()
        self.ignore = self.yamlconfig["ignore"]
        self.re_compile_file_extension = self._compile_video_file_extensions_pattern()

    video_extension_list = ['mkv', 'm4v', 'avi', 'mp4']

    def _get_dirs(self):
        """Returns [input_dir, output_dir] from the config.yaml file"""
        dirs = []
        for dir in ["input_dir", "output_dir"]:
            if self.yamlconfig[dir]:
                dir = os.path.abspath(self.yamlconfig[dir])
                dirs.append(dir)
            else:
                raise ValueError("Couldn't find {}".format(dir))
        # Check if the paths exists, its no use running otherwise :P
        for dir in dirs:
            if not os.path.exists(dir):
                raise ValueError("{} doesn't exists".format(dir))
        logger.debug("got dirs {}".format(dirs))
        return dirs

    def _compile_video_file_extensions_pattern(self):
        """returns re.compile('^.*(\.mkv|\.mp4)$', re.IGNORECASE)"""
        extensions = self.video_extension_list
        output = '^.*('
        for extension in extensions:
            output = output + '\.' + extension + '|'
        output = output[:-1] + ")$"
        return re.compile("{}".format(output), re.IGNORECASE)


if __name__ == "__main__":
    config = ConfigManager()
