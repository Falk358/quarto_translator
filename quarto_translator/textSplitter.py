from langchain.text_splitter import RecursiveCharacterTextSplitter


class QuartoTextSplitter:
    """
    receives a string containing a single document and returns a list of splits
    splits the document based on Markdown headers level 1, 2 and 3 (#, ##, ###)
    """

    def __init__(self, chunk_size: int, model_name="gpt-4"):

        self.md_text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            encoding_name="cl100kbase",
            model_name=model_name,
            chunk_size=chunk_size,
            chunk_overlap=0,
            separators=[":::", "\n\n", "\n", " ", ""],
        )

    def splitAllTextFileDict(self, file_dict: dict):
        """
        takes a dictionary with file path as key and markdown text as value as input;
        iterates over dictionary and returns dict with filepath as key; list of strings (each string is a chunk) as value
        """
        split_file_dict = {}
        for key, document in file_dict.items():
            split_file = self.splitText(document)
            split_file_dict[key] = split_file

        return split_file_dict

    def printFileChunks(self, chunks: list):
        """
        input: list of strings associated to single file (single entry in split_file_dict)
        prints text chunks (strings)
        """
        for chunk in chunks:
            print(chunk)
            print(
                "---------------------------------------next--------------------------------"
            )

    def splitText(self, document_string):
        """
        input: string containing on quarto Markdown file content
        output: list of strings
        """
        split_text = self.md_text_splitter.split_text(document_string)
        for text in split_text:
            assert type(text) is str
        return split_text
