import yaml
import os
import subprocess


class ConfigManager:
    def __init__(self):
        with open("config.yaml", 'r') as ymlfile:
            self.yamlconfig = yaml.load(ymlfile)
        self._pre_execute()
        self.input_dir, self.output_dir = self.get_dirs()

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
        return dirs

    def _pre_execute(self):
        if self.yamlconfig['pre_execute']:
            subprocess.run([self.yamlconfig['pre_execute']])


if __name__ == "__main__":
    config = ConfigManager()
