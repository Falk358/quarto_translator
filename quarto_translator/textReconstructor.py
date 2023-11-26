from langchain.schema.document import Document




class QuartoTextReconstructor():

    def __init__(self):
        pass


    
    def reconstructTextFromDocument(self, doc: Document):
        """
        input :langchain.schema.document.Document
        output :reconstructed text from split or None on error
        """
        document_text = ""
        for key, header in doc.metadata.items():
            if key == "h1":
                document_text = document_text + "# " + header + "\n "
            elif key == "h2":
                document_text = document_text + "## " + header + "\n "
            elif key == "h3":
                document_text = document_text + "### " + header + "\n "
            else:
                print(f"Error reconstructing string from Document; unkown header key entry in metadata: {key} for document {doc}")
                return

        if (doc.page_content is None):
            print(f"Error reconstructing string from Document; page_content is none for doc {doc}")
            return

        document_text = document_text + doc.page_content

        return document_text


