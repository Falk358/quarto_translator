import unittest
import os
from quarto_translator.textSplitter import QuartoTextSplitter
from quarto_translator.docLoader import DocLoader
from langchain.schema.document import Document
from configparser import ConfigParser
from quarto_translator.translator import Translator


class ReconstructionTest(unittest.TestCase):




    def setUp(self):
        self.markdown_test_string = "# My level 1 header\n ## My level 2 header\n This is content under the level 2 header.\n ## My other level 2 header\n blabala this is other content under my other level 2 header"
        self.configparser = ConfigParser()
        self.configparser.read("translator.config")
        self.docloader = DocLoader(self.configparser)
        self.docloader.loadContents()
        self.test_file_contents_dict = self.docloader.getContentsDict()
        
        self.chunk_size = 2000
        test_doc = Document(page_content= "this is a test document for testing reconstruction\n here is a new line", metadata= {"h1": "Test Header 1", "h2": "Test Header 2"})
        self.test_doc = test_doc
        self.test_doc_result = "# Test Header 1\n ## Test Header 2\n this is a test document for testing reconstruction\n here is a new line"

        
        self.source_dir = self.configparser["filepaths"]["SOURCE_PATH"]
        self.target_dir = self.configparser["filepaths"]["TARGET_PATH"]
        imaginary_file_name = "test_file.txt"
        imaginary_file_name_no_ext = os.path.splitext(imaginary_file_name)[0]
        imaginary_file_ext = os.path.splitext(imaginary_file_name)[1]
        self.imaginary_file_source_path = self.source_dir + "/"+ imaginary_file_name
        self.imaginary_file_target_path = self.target_dir + "/" + imaginary_file_name_no_ext + "_translated" + imaginary_file_ext

    def tearDown(self):
        if (os.path.isfile(self.imaginary_file_target_path)):
            os.remove(self.imaginary_file_target_path)


    def testTextSplitter(self):
        splitter = QuartoTextSplitter(self.chunk_size)
        text_split = splitter.splitText(self.markdown_test_string)
        assert(len(text_split) > 0)
        for chunk in text_split:
            assert(type(chunk) is str)


    def testFileDocumentReconstruction(self):
        splitter = QuartoTextSplitter(chunk_size= self.chunk_size)
        test_file_contents_split_dict = splitter.splitAllTextFileDict(self.test_file_contents_dict)
        first_filepath = next(iter(self.test_file_contents_dict))

        print(first_filepath)
        first_file_text = ""
        with open(first_filepath, "r") as first_file:
            first_file_text = first_file.read()

        first_file_reconstructed = ""
        for chunk in test_file_contents_split_dict[first_filepath]:
            first_file_reconstructed = first_file_reconstructed + "\n\n" + chunk 

        assert(len(first_file_text) <= len(first_file_reconstructed))
        difference_in_length = len(first_file_reconstructed.replace("\n", "")) - len(first_file_text.replace("\n", ""))
        assert(difference_in_length == 0) 



    def testFileWriting(self):

        test_file_chunk = {self.imaginary_file_source_path: ["chunk1\n", "chunk2\n", "chunk3 this is a longer chonk bllallablalbal\n", "chunk4\n"] }
        translator = Translator(parser=self.configparser, file_chunk_dict=test_file_chunk)
        translator.writeSingleFileToTarget(filepath=self.imaginary_file_source_path, file_string_content="blababla this is a test")
        
        assert(os.path.isfile(self.imaginary_file_target_path))















if __name__ == "__main__":
    unittest.main()
