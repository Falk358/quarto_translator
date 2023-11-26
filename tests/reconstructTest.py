import unittest
from quarto_translator.textSplitter import QuartoTextSplitter
from quarto_translator.textReconstructor import QuartoTextReconstructor
from langchain.schema.document import Document


class ReconstructionTest(unittest.TestCase):




    def setUp(self):
        self.markdown_test_string = "# My level 1 header\n ## My level 2 header\n This is content under the level 2 header.\n ## My other level 2 header\n blabala this is other content under my other level 2 header"
        test_doc = Document
        test_doc.page_content = "this is a test document for testing reconstruction\n here is a new line"
        test_doc.metadata = {"h1": "Test Header 1", "h2": "Test Header 2"}
        self.test_doc = test_doc
        self.test_doc_result = "# Test Header 1\n ## Test Header 2\n this is a test document for testing reconstruction\n here is a new line"




    def testTextSplitter(self):
        splitter = QuartoTextSplitter()
        text_split = splitter.splitText(self.markdown_test_string)
        assert(len(text_split) > 0)
        for doc in text_split:
            assert(type(doc) is Document)


    def testTextReconstructor(self):
        reconstructor = QuartoTextReconstructor()
        reconstructed_string = reconstructor.reconstructTextFromDocument(self.test_doc)
        assert(self.test_doc_result == reconstructed_string)













if __name__ == "__main__":
    unittest.main()
