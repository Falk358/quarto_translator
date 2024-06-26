import os
from configparser import ConfigParser


class DocLoader:
    """
    uses a source folder and filetype to load all files of given filetype within the folder into a dict of strings (each string contains one files content; filepath as key)

    """

    def __init__(self, configparser: ConfigParser, file_type=".qmd"):
        self.file_names = []
        self.file_contents = (
            {}
        )  # contains path_to_file as key and file contents (string) as val

        source_folder = configparser.get("filepaths", "SOURCE_PATH")
        source_folder = os.path.expanduser(source_folder)
        if not os.path.exists(source_folder):
            print(f"error finding directory with path {source_folder}")
            return

        self.__findFilenames(source_folder, file_type)

    def __findFilenames(self, source_folder: str, file_type: str):
        for root, _, files in os.walk(source_folder, topdown=True):
            for file_name in files:
                # print(file_name)
                _, extension = os.path.splitext(file_name)
                if extension == file_type:
                    path_to_file = os.path.join(root, file_name)
                    self.file_names.append(path_to_file)

    def loadContents(self):
        if len(self.file_names) < 1:
            print("Error loading contents; no files found during init")
            return
        for file_name in self.file_names:
            with open(file_name, "r") as file:
                self.file_contents[file_name] = file.read()

    def getContentsDict(self):
        return self.file_contents

    def getFileNames(self):
        """
        return individual file names in source folder
        """
        return self.file_names

    def printContents(self):
        for key, value in self.file_contents.items():
            print(f"File path: {key}\n Contents:\n {value}")
