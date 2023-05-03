import sys
import json
import platform
import logging

from flask import Flask
from flask import request, render_template, jsonify

import openai
from retry import retry

# The OpenAI configs
# Note the OpenAI API key needs to be passed in as env variables
openai.organization = "org-PDxYgRN9zTF3ZZV0iyKjg6yO"  # Personal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# output logs to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# EB looks for an 'application' callable by default.
application = Flask(__name__)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/health')
def health():
    return jsonify(success=True)


@application.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text = data['input']
        source_lang = data['source_lang']
        target_lang = data['target_lang']

        lines = split_multilingual_text(text)

        translated_lines = []
        for line in lines:
            logger.info(f"translating ({source_lang} -> {target_lang}): {line}")
            translated_lines.append(get_translation(line, source_lang, target_lang))

        return json.dumps({"translation": "\n".join(translated_lines)})
    except:
        return 'BACKEND TRANSLATION ERROR', 500


def get_translation(line, source_lang, target_lang):
    if source_lang == "english" and target_lang == "chinese":
        prompt = """
Translate this English Christian text into Chinese:

{input}



Return "<translate failed>" if you cannot translate. Don't return anything else.
""".format(input=line)

    elif source_lang == "chinese" and target_lang == "english":
        prompt = """
Translate this Chinese Christian text into English:

{input}



Return "<translate failed>" if you cannot translate. Don't return anything else.
""".format(input=line)

    else:
        raise Exception(f"unsupported translation language: {source_lang} -> {target_lang}")

    # not using davinci. it sometimes produces weird characters in translation. and it's expensive.
    # completion = get_davinci003_completion(prompt)

    completion = get_gpt35_completion(prompt)

    return completion['choices'][0]['message']['content']


LINE_ENDINGS = set(['。', '！', '？', '.', '!', '?', '\n'])  # common line ending characters in multiple languages
LINE_MIN_LEN = 2


@retry(tries=3, delay=1, backoff=2, logger=logger)
def get_gpt35_completion(prompt, role="user"):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": role, "content": prompt}]
    )


@retry(tries=2, delay=1, backoff=2, logger=logger)
def get_davinci003_completion(prompt):
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    print(completion)
    return completion


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
    if platform.system() == "Darwin":
        # enable debug mode if it's mac
        application.debug = True
        application.run()
    else:
        application.debug = False
        application.run()
