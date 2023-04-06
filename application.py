from flask import Flask
from flask import request

# import openai
# openai.organization = "org-PDxYgRN9zTF3ZZV0iyKjg6yO"
# openai.api_key = "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"

# EB looks for an 'application' callable by default.
application = Flask(__name__)


@application.post('/translate')
def login():
    data = request.get_json()
    input = data['input']
    prompt = "Translate this Chinese Christian article into English:\n\n{input}\n\n".format(input=input)

    # completion = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": prompt}]
    # )

    # return completion['choices'][0]['message']['content']
    return "succcess"


# run the app.
if __name__ == "__main__":
    application.debug = False
    application.run(port=5000)
