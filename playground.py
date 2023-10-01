# -*- coding: utf-8 -*-
import json
import openai


def play_chat_completion():
    init_prompt = f"""
You are a translation gpt that translates from English to Simplified Chinese.
The words and language style should be related to Christianity, the Bible, and churches.

Examples:

Input:
Peace brothers and sisters

Output:
弟兄姊妹们平安
    """

    messages = [
        {"role": "user", "content": init_prompt},
    ]

    stuff_to_translate = "Peace brothers and sisters"
    messages.append({"role": "user", "content": stuff_to_translate},)

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    print(completion['choices'][0]['message']['content'])


if __name__ == '__main__':
    play_chat_completion()
