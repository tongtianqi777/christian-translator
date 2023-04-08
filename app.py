import json

from flask import Flask
from flask import request, render_template

import openai

# The OpenAI configs
# Note the OpenAI API key needs to be passed in as env variables
openai.organization = "org-PDxYgRN9zTF3ZZV0iyKjg6yO"  # Personal

# EB looks for an 'application' callable by default.
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/health')
def health():
    return "all good"


@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data['input']
    source_lang = data['source_lang']
    target_lang = data['target_lang']

    lines = split_multilingual_text(text)

    translated_lines = []
    for line in lines:
        print(f"translating ({source_lang} -> {target_lang}): {line}")

        if source_lang == "english" and target_lang == "chinese":
            translated_line = get_chinese_translation_from_english_line(line)
        elif source_lang == "chinese" and target_lang == "english":
            translated_line = get_english_translation_from_chinese_line(line)
        else:
            raise Exception(f"unsupported translation language: {source_lang} -> {target_lang}")

        translated_lines.append(translated_line)

    return json.dumps({"translation": "\n".join(translated_lines)})


def get_english_translation_from_chinese_line(line):
    prompt = """
Translate this Chinese Christian text into English:

{input}

Say "<translate failed>" if you cannot translate. Don't say anything else."
""".format(input=line)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion['choices'][0]['message']['content']


def get_chinese_translation_from_english_line(line):
    prompt = """
Translate this English Christian text into Chinese:

{input}

Say "<translate failed>" if you cannot translate. Don't say anything else."
""".format(input=line)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion['choices'][0]['message']['content']


LINE_ENDINGS = set(['。', '！', '？', '.', '!', '?', '\n'])  # common line ending characters in multiple languages
LINE_MIN_LEN = 2


def split_multilingual_text(text):
    """
    Splits multilingual text into a list of strings based on line ending characters, ignoring lines shorter than 2 characters.

    Parameters:
    text (str): The multilingual text to split.

    Returns:
    List[str]: A list of strings, each containing a line of multilingual text.
    """
    lines = []
    current_line = ''
    for char in text:
        if char in LINE_ENDINGS:
            if len(current_line) >= LINE_MIN_LEN:
                lines.append(current_line)
            current_line = ''
        else:
            current_line += char

    if len(current_line) >= LINE_MIN_LEN:
        lines.append(current_line)

    return lines


# run the app.
if __name__ == "__main__":
    app.debug = True
    app.run(port=8000)
