from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter






class textSplitter():

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


    def splitTextFileDict(self, file_dict: dict):
        """
        takes a dictionary with file path as key and markdown text as input;
        iterates over dictionary and returns dict with filepath as key; langchain.schema.document.Document as value
        """
        split_doc_dict = {}
        for key, document in file_dict.items():
            split_doc = self.splitText(document)
            split_doc_dict[key] = split_doc
        
        return split_doc


    def splitText(self, document_string):
        split_text = self.md_text_splitter.split_text(document_string)
        return split_text

