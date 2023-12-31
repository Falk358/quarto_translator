# quarto_translator

## Translate Quarto documents into different natural languages

A Python project for translating Quarto Markdown documents using the OpenAI API.

Note that this program has only been tested for Linux, functionality on Windows is not guaranteed due to different path separators in Windows (uses `\` instead of `/`).


## Usage

Fill in the [template.config](template.config) file and rename it to `translator.config`. The following fields are needed:

- `SOURCE_PATH`: Path to the Quarto source documents.
- `TARGET_PATH`: Path for storing the translated Quarto documents.
- `API_KEY`: OpenAI API key. The account needs to be created on the [OpenAI API website](https://openai.com/blog/openai-api) in combination with a credit card.
- `SOURCE_LANGUAGE`: Natural language that the Quarto source documents are written in, e.g., `German`.
- `TARGET_LANGUAGE`: Natural language that the Quarto documents should be translated to, e.g., `English`.

