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
        
        self.chunk_size = 3000
        test_doc = Document(page_content= "this is a test document for testing reconstruction\n here is a new line", metadata= {"h1": "Test Header 1", "h2": "Test Header 2"})
        self.test_doc = test_doc
        self.test_doc_result = "# Test Header 1\n ## Test Header 2\n this is a test document for testing reconstruction\n here is a new line"




    def testTextSplitter(self):
        splitter = QuartoTextSplitter(self.chunk_size)
        text_split = splitter.splitText(self.markdown_test_string)
        assert(len(text_split) > 0)
        for chunk in text_split:
            assert(type(chunk) is str)


    #def testDocumentReconstruction(self):
    #    reconstructor = QuartoTextReconstructor(self.test_file_contents_dict)
    #    reconstructed_string = reconstructor.reconstructTextFromDocument(self.test_doc)
    #    assert(self.test_doc_result == reconstructed_string)

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
            first_file_reconstructed = first_file_reconstructed + chunk + "\n\n"

        with open("first_file_reconstructed.qmd", "w") as reconstructed_file:
            reconstructed_file.write(first_file_reconstructed)

        print(f"len original:{len(first_file_text)}")
        print(f"len reconstructed:{len(first_file_reconstructed)}")

        assert(len(first_file_text)+1 == len(first_file_reconstructed))


    def testSingleFileTranslation(self):
        splitter = QuartoTextSplitter(chunk_size= self.chunk_size)
        test_file_contents_split_dict = splitter.splitAllTextFileDict(self.test_file_contents_dict)
        first_filepath = next(iter(self.test_file_contents_dict))

        translator = Translator(file_chunk_dict=test_file_contents_split_dict, parser=self.configparser)

        translated_file = translator.translateFile(first_filepath)

        first_file_text = ""
        with open(first_filepath, "r") as first_file:
            first_file_text = first_file.read()

        print(f"len original:{len(first_file_text)}")
        print(f"len reconstructed:{len(translated_file)}")

        assert(len(first_file_text)+1 == len(translated_file))














if __name__ == "__main__":
    unittest.main()
