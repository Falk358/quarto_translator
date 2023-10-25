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

    def splitText(self, document_string):
        split_text = self.md_text_splitter.split_text(document_string)
        return split_text

