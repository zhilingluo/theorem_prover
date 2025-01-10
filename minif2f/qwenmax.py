# -*- coding: utf-8 -*-
# @Time     :  14:37
# @File     : Qwenmax.py
# @Author   : Bruce
# @Team     : XGeneration
import os
import random
import dashscope
from http import HTTPStatus

dashscope.api_key =os.environ['dashscope_key']



def call_qwen_raw(prompt,temperature):
    response = dashscope.Generation.call(
        "qwen-max",
        messages=[prompt],
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        # set the result to be "message" format.
        temperature=temperature,
        result_format='message',
    )
    if response.status_code == HTTPStatus.OK:
        # print(response)
        pass
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
    content = response.output.choices[-1].message.content

    return content
def call_qwen(prompt,temperature,system_prompt='You are a helpful assistant.') -> str:
    messages = [{'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}]
    response = dashscope.Generation.call(
        "qwen-max",
        messages=messages,
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        # set the result to be "message" format.
        temperature=temperature,
        result_format='message',
    )
    if response.status_code == HTTPStatus.OK:
        # print(response)
        pass
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
    content = response.output.choices[-1].message.content

    return content

def call_qwen_longcontext(prompt) -> str:
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}]
    response = dashscope.Generation.call(
        "qwen-max-longcontext",
        messages=messages,
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        # set the result to be "message" format.
        result_format='message',
    )
    if response.status_code == HTTPStatus.OK:
        # print(response)
        pass
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

    content = response.output.choices[-1].message.content

    return content
#print(call_qwen("hello world"))