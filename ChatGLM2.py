# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 14:48:02 2023

@author: 98608
"""
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

from langchain.chat_models import ChatOpenAI
class  ChatGLM2(ChatOpenAI):
    openai_api_base = "http://192.168.0.11:8081/v1"
    openai_api_key = "123456"
    model_name = "chatglm2-6b"
    max_tokens = 8000


# import openai

# openai.api_base = "http://192.168.0.11:8081/v1"

# Enter any non-empty API key to pass the client library's check.
# openai.api_key = "xxx"

# compute the embedding of the text
# embedding = openai.Embedding.create(
#     input="什么是chatgpt？",
#     model="text2vec-large-chinese"
# )
#
# print(embedding['data'][0]['embedding'])