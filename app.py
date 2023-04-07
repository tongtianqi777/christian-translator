import json
import re

from flask import Flask
from flask import request, render_template

import openai
openai.organization = "org-PDxYgRN9zTF3ZZV0iyKjg6yO"
openai.api_key = "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"

# EB looks for an 'application' callable by default.
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/health')
def health():
    return True


@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data['input']

    lines = split_multilingual_text(text)

    translated_lines = []
    for line in lines:
        translated_line = get_english_translation_from_chinese_line(line)
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


def split_multilingual_text(text):
    """
    Splits multilingual text into a list of strings based on line ending characters, ignoring lines shorter than 2 characters and lines without any Chinese characters.

    Parameters:
    text (str): The multilingual text to split.

    Returns:
    List[str]: A list of strings, each containing a line of multilingual text.
    """
    line_endings = ['。', '！', '？', '.', '!', '?', '\n']  # common line ending characters in multiple languages
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')  # regex pattern to match Chinese characters
    lines = []
    current_line = ''
    for char in text:
        if char in line_endings:
            if len(current_line) >= 2 and chinese_pattern.search(current_line):
                lines.append(current_line)
            current_line = ''
        else:
            current_line += char
    if len(current_line) >= 2 and chinese_pattern.search(current_line):
        lines.append(current_line)
    return lines


# run the app.
if __name__ == "__main__":
    app.run(port=8000)
