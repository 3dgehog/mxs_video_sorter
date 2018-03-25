import yaml
import os
import subprocess
import logging
import re

logger = logging.getLogger('main')


class ConfigManager:
    def __init__(self):
        with open("7m_video_sorter/config.yaml", 'r') as ymlfile:
            self.yamlconfig = yaml.load(ymlfile)
        self._pre_execute()
        self.input_dir, self.output_dir = self.get_dirs()
        self.file_ignore = self.yamlconfig.file_ignore
        self.regex_file_extensions_pattern = self._compile_video_file_extensions_pattern()

    def get_dirs(self):
        """Returns [input_dir, output_dir] from either the config.yaml file of
        the environment variables $INPUT_DIR and $OUTPUT_DIR. To add to
        environment variables enter: export INPUT_DIR='/path/to/input/file'"""
        dirs = []
        for dir in ["input_dir", "output_dir"]:
            if self.yamlconfig[dir]:
                dirs.append(self.yamlconfig[dir])
            elif os.environ.get(dir.upper()):
                dirs.append(os.environ.get(dir.upper()))
            else:
                raise ValueError("Couldn't find {}".format(dir))
        # Check if the paths exists, its no use running otherwise :P
        for dir in dirs:
            if not os.path.exists(dir):
                raise ValueError("{} doesn't exists".format(dir))
        logger.debug("got dirs {}".format(dirs))
        return dirs

    def _pre_execute(self):
        if self.yamlconfig['pre_execute']:
            subprocess.run([self.yamlconfig['pre_execute']])
            logger.debug("ran _pre_execute from config_manager")

    def _compile_video_file_extensions_pattern(self):
        """returns re.compile('^.*(\.mkv|\.mp4)$', re.IGNORECASE)"""
        extensions = self.yamlconfig["video_file_extensions"]
        output = '^.*('
        for extension in extensions:
            output = output + '\.' + extension + '|'
        output = output[:-1] + ")$"
        return re.compile("{}".format(output), re.IGNORECASE)


if __name__ == "__main__":
    config = ConfigManager()
