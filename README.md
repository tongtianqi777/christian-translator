# Christian Translator

A translator web application that is better than Google Translation for the languages supported. It utilizes the latest GPT models from OpenAI for Christian domain texts.

## Why is This Useful

Many multi-lingo churches around the world rely on volunteers to translate church publications such as sermons, testimonies, emails, etc.
For a long time the volunteers have to rely on [Google Translation](http://translate.google.com) or translation agencies. We hope this tool can offer some simplicity with high quality translation.

## Supported Languages

- English -> Chinese
- Chinese -> English

## Get Started

The project is super simple, with a Python file `app.py` handling all the requests with Flask.

The UI is rendered with the html files under `templates`.

To run the application locally:

```
python app.py
```

## Deployment

The project can easily be deployed on Microsoft Azure. Note the OpenAPI key is required as an environment variable: `OPENAI_API_KEY`

## Contributors

- Tianqi Tong (tianqitong@outlook.com)

## Roadmap

- Train fine-tuned model with translation examples
