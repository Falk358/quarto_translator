import sys
from openai import OpenAI
import os
from configparser import ConfigParser



class Translator():
    """
    calls chatpt-3.5 turbo to translate all files in passed dictionary
    parameter explanation file_chunk_dict: dictionary with filepath as key and list of text chunks of that file as value
    """
    def __init__(self, file_chunk_dict: dict, parser: ConfigParser, model = "gpt-3.5-turbo"):
        self.file_chunk_dict = file_chunk_dict
        self.__setup(parser)
        self.model_type = model
        self.llm = OpenAI(api_key= self.api_key)
        self.system_message = {"role": "system", "content":  f"Please act as a translator from {self.source_language} to {self.target_language}. The following is a quarto markdown file: please only translate the textual content, leaving the quarto and markdown instructions in the file."}


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
        translated_file = ""
        llm_prompts = []
        llm_outputs = []
        for chunk in self.file_chunk_dict[filepath]:
            user_message = {"role": "user", "content": chunk}
            completion = self.llm.chat.completions.create(
                    model = self.model_type,
                    messages = [self.system_message, user_message],
                    temperature= 1.0)
            message = completion.choices[0].message
            llm_outputs.append(message)


        for output in llm_outputs:
            translated_file = translated_file + "\n\n" + output.content

        return translated_file


    def translateAllFiles(self):
        """ returns dict with source file path as key and translated file as value"""
        translated_file_dict = {}
        for path in self.file_chunk_dict:
            translated_file_str = self.translateFile(path)
            translated_file_dict[path] = translated_file_str

        return translated_file_dict


    def writeAllFilesToTarget(self, translated_file_dict:dict):
        """takes dict with source file path as key and translated file string as value as argument; 
        writes the strings to the target dir specified in .conf file"""

        pass 











