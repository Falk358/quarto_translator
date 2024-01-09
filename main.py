from quarto_translator.tokenCounter import TokenCounter
from quarto_translator.docLoader import DocLoader
from configparser import ConfigParser
from quarto_translator.textSplitter import QuartoTextSplitter
from quarto_translator.translator import Translator




def makeEstimate(loader: DocLoader):
    doc_dict = loader.getContentsDict()
    counter = TokenCounter()
    for path in doc_dict.keys():
        print(path)
        text = doc_dict[path]
        counter.countTokensInString(text)


    print(counter.getCounter())
    counter.printCostEstimateTranslation(pricing_input=0.0015, pricing_output=0.002) #pricing for gpt-3.5 Turbo



def main():

    configparser = ConfigParser()
    configparser.read("translator.config")
<<<<<<< Updated upstream
    model = configparser.get(section="openai", option="MODEL_NAME")
    print(f"Using openai model {model}")

    loader = DocLoader(configparser = configparser)
    loader.loadContents()
    all_files = loader.getContentsDict()

    splitter = QuartoTextSplitter(chunk_size= 2000, model_name=model)
    text_splits = splitter.splitAllTextFileDict(all_files)

    translator = Translator(file_chunk_dict=text_splits, parser=configparser, model_name=model)
    #filepath_test = "/home/max/Documents/quarto_translator/source/wahrscheinlichkeitsrechnung2.qmd"
    #translated_file = translator.translateFile(filepath_test)
    #translator.writeSingleFileToTarget(filepath=filepath_test, file_string_content=translated_file)
    translated_file_dict = translator.translateAllFiles()
    translator.writeAllFilesToTarget(translated_file_dict)
=======
    loader = DocLoader(configparser = configparser)
    loader.loadContents()
    makeEstimate(loader)
    splitter = QuartoTextSplitter(chunk_size= 3000)
    all_files = loader.getContentsDict()
    text_splits = splitter.splitAllTextFileDict(all_files)
    translator = Translator(parser= configparser, file_chunk_dict=text_splits)
    translated_file = translator.translateFile("/home/max/Documents/quarto_translator/source/wahrscheinlichkeitsrechnung2.qmd")
    print(translated_file)
    #splitter.printFileChunks(text_splits["/home/max/Documents/quarto_translator/source/wahrscheinlichkeitsrechnung2.qmd"])
>>>>>>> Stashed changes

















if __name__ == "__main__":
    main()
