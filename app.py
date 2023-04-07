from flask import Flask
from flask import request

import openai
openai.organization = "org-PDxYgRN9zTF3ZZV0iyKjg6yO"
openai.api_key = "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"

# EB looks for an 'application' callable by default.
app = Flask(__name__)


@app.route('/')
def root():
    print('Request for root received')
    return "root succcess"


@app.route('/health')
def health():
    return True


@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    input = data['input']
    prompt = "Translate this Chinese Christian article into English:\n\n{input}\n\n".format(input=input)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion['choices'][0]['message']['content']


# run the app.
if __name__ == "__main__":
    app.run(port=8000)
