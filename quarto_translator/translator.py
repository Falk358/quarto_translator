import os
import sys
from configparser import ConfigParser

from openai import OpenAI


class Translator:
    """
    calls chatpt-3.5 turbo to translate all files in passed dictionary
    parameter explanation file_chunk_dict: dictionary with filepath as key and list of text chunks of that file as value
    """

    def __init__(self, file_chunk_dict: dict, parser: ConfigParser, model_name="gpt-4"):
        self.file_chunk_dict = file_chunk_dict
        self.__setup(parser)
        self.model_type = model_name
        self.llm = OpenAI(api_key=self.api_key)
        self.system_message = {
            "role": "system",
            "content": f'Please act as a translator from {self.source_language} to {self.target_language}. The following is a quarto markdown file: please only translate the textual content, leaving the quarto, knitr and markdown instructions in the file. Furthermore, if you come across a reference within regular text which is annotated with an "@" sign, please leave it as is. Example: @fig-C9.G.3.',
        }

    def __setup(self, parser):
        self.output_folder = parser.get("filepaths", "TARGET_PATH")
        self.api_key = parser.get("openai", "API_KEY")
        if self.api_key is None:
            print("Error retrieving api key!!! aborting")
            sys.exit(-1)
        self.source_language = parser.get("translation", "SOURCE_LANGUAGE")
        self.target_language = parser.get("translation", "TARGET_LANGUAGE")

    def translateFile(self, filepath):
        """
        translates a single file defined by filepath (absolute path to file)
        """
        translated_file_string = ""
        llm_outputs = []
        for chunk in self.file_chunk_dict[filepath]:
            user_message = {"role": "user", "content": chunk}
            completion = self.llm.chat.completions.create(
                model=self.model_type,
                messages=[self.system_message, user_message],
                temperature=1.0,
            )
            message = completion.choices[0].message
            llm_outputs.append(message)

        for output in llm_outputs:
            translated_file_string = translated_file_string + "\n\n" + output.content

        return translated_file_string

    def translateAllFiles(self):
        """returns dict with source file path as key and translated file as value"""
        translated_file_dict = {}
        for path in self.file_chunk_dict:
            translated_file_str = self.translateFile(path)
            translated_file_dict[path] = translated_file_str
            self.writeSingleFileToTarget(
                filepath=path, file_string_content=translated_file_str
            )

        return translated_file_dict

    def writeSingleFileToTarget(self, filepath: str, file_string_content: str):
        """
        takes path to source file and string containing translated file as argument, writes file with same name and _translated extension into the target folder specified in .conf
        """
        filename = os.path.basename(filepath)
        filename_no_ext = os.path.splitext(filename)[0]
        file_ext = os.path.splitext(filename)[1]
        if self.output_folder is None:
            print(
                f"Error! No output folder read from config file; Aborting writing file {filename}"
            )
            return

        target_path = (
            self.output_folder + "/" + filename_no_ext + "_translated" + file_ext
        )

        with open(target_path, "w") as target_file:
            target_file.write(file_string_content)

    def writeAllFilesToTarget(self, translated_file_dict: dict):
        """
        takes dict with source file path as key and translated file string as value as argument;
        writes the strings to the target dir specified in .conf file
        """
        for source_path, translated_file in translated_file_dict.items():
            self.writeSingleFileToTarget(
                filepath=source_path, file_string_content=translated_file
            )
