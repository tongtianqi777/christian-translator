import sys
import json
import platform
import logging

from flask import Flask
from flask import request, render_template, jsonify

import openai
from retry import retry
from typing import List

from examples import EXAMPLES_LOOKUP
from utils.text_utils import split_sections

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

SECTION_DELIMITER = "---"

LOCALE_NAME_LOOKUP = {
    "en_US": "English",
    "zh_CN": "Simplified Chinese"
}


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
        input = data['input']
        src_lang = data['src_lang']
        tgt_lang = data['tgt_lang']

        sections = split_sections(input, SECTION_DELIMITER)
        translated_sections = translate_sections(sections, src_lang, tgt_lang)

        joined_sections = f"\n{SECTION_DELIMITER}\n".join(translated_sections)

        return json.dumps({"translation": joined_sections})
    except:
        return 'BACKEND TRANSLATION ERROR', 500


def translate_sections(sections: list, src_locale: str, tgt_locale: str) -> List[str]:
    src_lang = LOCALE_NAME_LOOKUP[src_locale]
    tgt_lang = LOCALE_NAME_LOOKUP[tgt_locale]

    examples = EXAMPLES_LOOKUP[src_locale][tgt_locale]

    # the init prompt needs to be provided for each translation prompt
    init_prompt = f"""
You are a translation gpt that translates from {src_lang} to {tgt_lang}.
The words and language style should be related to Christianity, the Bible, and churches.

Examples:

{"".join(examples)}
"""

    translated_sections = []

    for section in sections:
        messages = [
            {"role": "user", "content": init_prompt},
            {"role": "user", "content": section},
        ]

        logger.info(f"translating ({src_lang} -> {tgt_lang}): {section[:30]}...")

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        translated_sections.append(completion['choices'][0]['message']['content'])

    return translated_sections


# run the app.
if __name__ == "__main__":
    if platform.system() == "Darwin":
        # enable debug mode if it's mac
        application.debug = True
        application.run()
    else:
        application.debug = False
        application.run()
