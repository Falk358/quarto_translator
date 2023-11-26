from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter






class QuartoTextSplitter():

    """
    receives a string containing a single document and returns a list of splits
    splits the document based on Markdown headers level 1, 2 and 3 (#, ##, ###)
    """
    def __init__(self):
        headers_to_split_on = [
                ("#", "h1"),
                ("##", "h2"),
                ("###", "h3")
        ]
        self.md_text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)


    def splitAllTextFileDict(self, file_dict: dict):
        """
        takes a dictionary with file path as key and markdown text as input;
        iterates over dictionary and returns dict with filepath as key; langchain.schema.document.Document as value
        """
        split_file_dict = {}
        for key, document in file_dict.items():
            split_file = self.splitText(document)
            split_file_dict[key] = split_file
        
        return split_file_dict

    def printFileDocumentList(self, documents: list):
        """
        input: list of Document() associated to single file (single entry in split_file_dict)
        prints individual Document (which are document splits processed by MarkDownHeaderTextSplitter())
        """
        for doc in documents:
            print(doc)
            print("---------------------------------------next--------------------------------")
        


    def splitText(self, document_string):
        split_text = self.md_text_splitter.split_text(document_string)
        return split_text

