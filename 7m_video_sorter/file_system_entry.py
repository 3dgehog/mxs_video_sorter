import os


class FileSystemEntry:
    def __init__(self, config, fse):
        self.config = config
        self.path_to_fse = os.path.join(config.input_dir, fse)
        self.fse = fse
        self.dirname = config.input_dir
        self.get_info()

    def get_info(self):
        """Attributes are:
        - valid (if its a valid file)
        - isdir (if its a directory)
        - vfile (video files)
        - path_to_vfile (abs path to video file)
        """
        self.valid = False
        self.isdir = os.path.isdir(self.path_to_fse)

        if self.isdir:
            for item in os.listdir(self.path_to_fse):
                # if secondary directory, ignore
                if os.path.isdir(os.path.join(self.path_to_fse, item)):
                    continue

                # if file has file extension
                if self.config.re_compile_file_extension.match(item):
                    # if file was already valid, break and set to not valid
                    # reason: does not support multiple files right now!!
                    if self.valid:
                        self.valid = False
                        break
                    self.vfile = item
                    self.path_to_vfile = os.path.join(self.path_to_fse, item)
                    self.valid = True

        else:
            # check if the file found has a valid file extension
            if self.config.re_compile_file_extension.match(self.fse):
                self.vfile = self.fse
                self.path_to_vfile = self.path_to_fse
                self.valid = True
