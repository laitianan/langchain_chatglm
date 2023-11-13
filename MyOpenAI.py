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
from  config import api_base
from api_protocol import ChatMessage
from langchain.llms import OpenAI

""":param
    llm = ChatOpenAI(
        model_name="Qwen",
        openai_api_base=api_base ,
        openai_api_key="EMPTY",
        streaming=False,
    )
"""
class  myOpenAi(ChatOpenAI):
    openai_api_base = api_base
    openai_api_key = "123456"
    model_name = "qwen-14b-4bit"
    max_tokens = 1500
    temperature=0.7
    top_p = 0.8
    max_length = 1500
    # model_kwargs =
    @property
    def _default_params(self) -> Dict[str, Any]:
        """Get the default parameters for calling OpenAI API."""
        res={
            "model": self.model_name,
            "request_timeout": self.request_timeout,
            "max_tokens": self.max_tokens,
            "stream": self.streaming,
            "n": self.n,
            "temperature": self.temperature,
            "max_length": self.max_length,
            **self.model_kwargs,
        }
        return res

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

    # embed_query("你好")

if __name__ == '__main__':
    llm = myOpenAi()

    mp = {
        "订单售后查询": "根据用户订单ID查询用户订单售后信息",
        "订单状态查询": "根据用户订单ID查询用户订单状态信息",
        "订单配送查询": "根据用户订单ID查询用户订单目前配信息",
        "订单数据查询": "根据用户订单ID查询用户订单数据信息",
        "门店当天实时业绩查询": "门店当天实时业绩查询",
        "站点当天实时业绩查询": "站点当天实时业绩查询"
    }

    summary = []
    for i, key in enumerate(mp):
        summary.append(f"{i + 1}、{key}:{mp[key]}")

    summary = "\n".join(summary)

    user_input = "订单查询"

    INTENT_FORMAT_INSTRUCTIONS: str = """
    现在有一些意图，类别为：{intents}，
    你扮演AI角色的任务是根据***分隔符的文本对话，来进行一种或多种的意图识别，语义或关键词匹配识别，请使用列表方式返回。
    输出应该是严格按以下模式格式化的标记代码片段，必须包括开头和结尾的" ' ' ' json"和" ' ' ' ":
    ```json
    {{
        "intention_name": list  // 意图类别数组，意图类别必须在提供的类别中，比如
    }}
    ```
    备注意图详情描述：
    {intention_summary}
    ***
    历史对话沟通记录：
    {user_input}
    ***
    你的回答：
    """

    query = INTENT_FORMAT_INSTRUCTIONS.format(intents=list(mp.keys()), intention_summary=summary, user_input=user_input)

    res = llm.predict(query)
    print(res)
    # embeddings=myOpenAIEmbeddings()
    # res=embeddings.embed_query("你好")
    # print(res)
