import os


class FileSystemEntry:
    """
    The Object that takes care of the File System Entry in the Input Folder
    - path_to_fse: abspath path to fse
    """
    def __init__(self, config, fse):
        self.config = config
        self.path_to_fse = os.path.join(config.input_dir, fse)
        self.fse = fse
        self.vfile = VideoFile()
        self.get_info()

    def get_info(self):
        """
        - valid: True if its a valid file)
        - isdir: True if its a directory
        - vfile.filename: video filename
        - vfile.abspath: abspath to video file
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
                    self.vfile.filename = item
                    self.vfile.abspath = os.path.join(self.path_to_fse, item)
                    self.valid = True

        else:
            # check if the file found has a valid file extension
            if self.config.re_compile_file_extension.match(self.fse):
                self.vfile.filename = self.fse
                self.vfile.abspath = self.path_to_fse
                self.valid = True


class VideoFile:
    pass
