# quarto_translator

## Translate Quarto documents into different natural languages

A Python project for translating Quarto Markdown documents using the OpenAI API.

Note that this program has only been tested for Linux, functionality on Windows is not guaranteed due to different path separators in Windows (uses `\` instead of `/`).


## Usage

Install dependencies by running:
```python3 -m pip install -r requirements.txt```

Fill in the [template.config](template.config) file. The following fields are needed:

- `SOURCE_PATH`: Path to the Quarto source documents. Path needs to point to a folder; Needs to be written without trailing slash (e.g. `/path/to/git/quarto_translator/source`)
- `TARGET_PATH`: Path for storing the translated Quarto documents. Also needs to point to a folder, same as format as `SOURCE_PATH`
- `API_KEY`: OpenAI API key. The account needs to be created on the [OpenAI API website](https://openai.com/blog/openai-api) in combination with a credit card.
- `MODEL_NAME`: Name of the model you want to use, according to Openai's model name (example: `gpt-3.5-turbo`)
- `SOURCE_LANGUAGE`: Natural language that the Quarto source documents are written in, e.g., `German`.
- `TARGET_LANGUAGE`: Natural language that the Quarto documents should be translated to, e.g., `English`.

Please run the program by executing `main.py`:

```python3 main.py -c template.config```
