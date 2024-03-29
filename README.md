# Christian Translator

A web application that calls OpenAI API to translate Christian domain texts.


## Why is This Useful

Many multi-lingo churches around the world rely on volunteers to translate church publications such as sermons, testimonies, emails, etc.
For a long time the volunteers have to rely on [Google Translation](http://translate.google.com) or translation agencies. We hope this tool can offer some simplicity with high quality translation.

From a few experiments, it appears that GPT is better than Google Translation when being hinted about the Christian faith context.
For example, for the same English text:

```text
Peace brothers and sisters
```

When translating the text above to Chinese:

Output from Google Translation
```text
兄弟姐妹们平安
```

Output from GPT
```text
平安弟兄姊妹
```

Clearly GPT did better since Christians tend to call each other `弟兄姊妹` in Chinese.

Another longer example:
```text
For years, maybe, you have tried fruitlessly to exercise control over yourself, and perhaps this is still your experience;
but when once you see the truth you will recognize that you are indeed powerless to do anything, but that in setting you aside altogether God has done it all.
Such a revelation brings human self-effort to an end.
```

Output from Google Translation
```text
多年来，也许，你一直试图控制自己，但徒劳无功，也许这仍然是你的经历；
但是一旦你看到真相，你就会认识到你确实无能为力，但上帝将你完全搁置一旁，这一切都已完成。
这样的启示结束了人类的自我努力。
```

Output from GPT
```text
也许多年以来，你一直试图毫无成效地掌控自己，也许这仍然是你的体验；
但是一旦你看到真理，你就会认识到，你确实无能为力，但是神已将你完全归置于一旁，祂已经完成了一切。
这样的启示将人类的自我努力终结了。
```

The GPT did a better job, cause it successfully translated `truth` as `真理`, and even used `祂` (the specific word used to refer to the Lord) in its output.

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

Then open the browser and go to http://127.0.0.1:8000 for the UI.

## Prompt Engineering

The following template is used as initial prompt for each chat completion:

```text
You are a translation gpt that translates from {src_lang} to {tgt_lang}.
The words and language style should be related to Christianity, the Bible, and churches.

Examples:

{"".join(examples)}
```

Then each prompt can be an input to be translated.


## Deployment

The project can easily be deployed with AWS Elastic Beanstalk. Note the OpenAPI key is required as an environment variable: `OPENAI_API_KEY`

Install the EB CLI: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html

To deploy the application to AWS:
```shell
eb deploy
```


## Contributing

Feel free to bring up a pull request or a Github issue.

Current contributors:
- Tianqi Tong (tianqitong@outlook.com)

## Roadmap

- Train a fine-tuned model with translation examples
