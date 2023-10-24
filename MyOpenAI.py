# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 14:48:02 2023

@author: 98608
"""

from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
api_base = "http://61.141.232.106:8084/v1"#公网
api_base = "http://192.168.0.11:8084/v1"#内网

class  myOpenAi(ChatOpenAI):
    openai_api_base = api_base
    openai_api_key = "123456"
    model_name = "internlm-chat-7b"
    max_tokens = 8000
    # top_p=8

class myOpenAIEmbeddings(OpenAIEmbeddings):
    ##model 一定要写OpenAIEmbeddings，自定义后台有做判断，而 curl 传递参数model，可以随便填写，其中原因是openai提交方式会把文字token转换为数字之后传递到后台，需重新把数字转文字。
    model = "OpenAIEmbeddings"
    openai_api_base= api_base
    openai_api_key="None"


if __name__ == '__main__':
    llm = myOpenAi(temperature=0)

    res = llm.predict("你好呀")
    print(res)