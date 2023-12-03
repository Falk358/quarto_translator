import sys
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
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
        self.llm = ChatOpenAI(model= model, temperature=0, openai_api_key= self.api_key)
        self.prompt_template = ChatPromptTemplate.from_messages(
                [
                ("system", "Please act as a translator from {source_language} to {target_language}. The following is a quarto markdown file: please only translate the textual content, leaving the quarto and markdown instructions in the file."),
                ("human", "{chunk}")
                ])


    def __setup(self, parser):
        self.output_folder = parser.get("filepaths", "TARGET_PATH")
        self.api_key = parser.get("openai", "API_KEY")
        if self.api_key is None:
            print("Error retrieving api key!!! aborting")
            sys.exit(-1)
        self.source_language = parser.get("translation", "SOURCE_LANGUAGE")
        self.target_language = parser.get("translation", "TARGET_LANGUAGE")
    


    def translateFile(self, filepath):
        translated_file = ""
        for chunk in self.file_chunk_dict[filepath]:
            response = self.llm(self.prompt_template.format_messages(source_language=self.source_language, target_language=self.target_language, chunk=chunk))
            print(response.content)
            translated_file = translated_file + "\n\n" + response.content

        return translated_file









