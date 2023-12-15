# quarto_translator
A python project for translating quarto markdown files using the openai API. Note that this program has only been tested for Linux, functionality on Windows is not guaranteed due to different path separators in Windows (uses `\` instead of `/`).




# Usage

Fill in your path to the source, target files into the **template.config** file and rename it to **translator.config**. Also fill in your Openai **API Key** into the config file. Note that you need to create an account on [the Openai Api Website] (https://openai.com/blog/openai-api) and add your credit card to use the Openai api.
Finally, you need to fill in the source and target languages. *Source language* refers to the language you are translating from, i.e. the language of the files you are translating. *Target language* refers to the language you want your files translated to.

Example: source language German; target language English will translate your quarto files written in German to English.

