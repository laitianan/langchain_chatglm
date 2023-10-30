# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 14:48:02 2023

@author: 98608
"""
from typing import Any, Dict, List, Literal, Optional, Union
import json
import requests
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
# api_base = "http://61.141.232.106:8084/v1"#公网
api_base = "http://192.168.0.11:8081/v1"#内网
# api_base = "http://127.0.0.1:8081/v1"#内网
from api_protocol import ChatMessage

class  myOpenAi(ChatOpenAI):
    openai_api_base = api_base
    openai_api_key = "123456"
    model_name = "qwen-14b-4bit"
    max_tokens = 2000
    temperature=0.8
    # top_p=8



class openai_model():

    def __init__(self,max_tokens = 2000,temperature=0.8):
        self.temperature=temperature
        self.max_tokens=max_tokens

    def predict(self,messages:Union[str, List[ChatMessage]]):
        history = []
        if isinstance(messages,str):
            history.append({"role": "user", "content": messages})
        else:
            for mess in messages:
                history.append({"role": mess.role, "content": mess.content})
        data=json.dumps({
            "model": "qwen-14b-4bit",
            "messages": history,
            "stream": False,
            "max_tokens":self.max_tokens,
            "temperature": self.temperature
          })
        r1 = requests.post(f"{api_base}/chat/completions", headers={'Content-Type': 'application/json'},data=data)
        res = json.loads(r1.content.decode("utf8"))
        content=res["choices"][0]["message"]["content"]
        return content


class myOpenAIEmbeddings(OpenAIEmbeddings):
    ##model 一定要写OpenAIEmbeddings，自定义后台有做判断，而 curl 传递参数model，可以随便填写，其中原因是openai提交方式会把文字token转换为数字之后传递到后台，需重新把数字转文字。
    model = "OpenAIEmbeddings"
    openai_api_base= api_base
    openai_api_key="None"


if __name__ == '__main__':
    llm = myOpenAi(temperature=0.7,max_tokens=2000)
    res = llm.predict("你好")
    print(res)
