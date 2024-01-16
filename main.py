import os
from quarto_translator.tokenCounter import TokenCounter
import sys
from quarto_translator.docLoader import DocLoader
from configparser import ConfigParser
from quarto_translator.textSplitter import QuartoTextSplitter
from quarto_translator.translator import Translator
import argparse



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
    arg_parse = argparse.ArgumentParser(prog="quartoTranslator", description="translate written text in Quarto file from source language to target language, leaving syntax mostly intact.", epilog="Usage: python3 main.py -c template.config")
    arg_parse.add_argument("-c", "--config", help="path to specified config file")
    arg_parse.add_argument("-s", "--select", action="store_true", help= "select which files to process")
    cmd_args = arg_parse.parse_args()
    if cmd_args.config is None:
        print("Error: Missing argument --config: \nUsage:\n python3 main.py -c template.config\n python3 main.py --config template.config")
        sys.exit(-1)

    configparser = ConfigParser()
    configparser.read(cmd_args.config)
    model = configparser.get(section="openai", option="MODEL_NAME")
    print(f"Using openai model {model}")

    loader = DocLoader(configparser = configparser)
    loader.loadContents()
    all_files = loader.getContentsDict()
    

    splitter = QuartoTextSplitter(chunk_size= 2000, model_name=model)
    text_splits = splitter.splitAllTextFileDict(all_files)

    translator = Translator(file_chunk_dict=text_splits, parser=configparser, model_name=model)
    if cmd_args.select:
        file_names_found = loader.getFileNames()
        file_names_no_path = map(lambda x: os.path.split(x)[1], file_names_found)

        print("The following files where found in selected source folder:")
        for index, file_name in enumerate(file_names_no_path):

            print(f"[{index}]: {file_name}")

        selected_indices = input("Enter the numbers of files to process (comma-separated): ").split(',')
        selected_indices = map(lambda x: int(x), selected_indices)

        for i in selected_indices:
            translated_file = translator.translateFile(file_names_found[i])
            translator.writeSingleFileToTarget(file_names_found[i], translated_file)
    else:
        translator.translateAllFiles()
        #translator.writeAllFilesToTarget(translated_file_dict)



if __name__ == "__main__":
    main()
