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
        parm={
            "model": self.model_name,
            "request_timeout": self.request_timeout,
            "max_tokens": self.max_tokens,
            "stream": self.streaming,
            "n": self.n,
            "temperature": self.temperature,
            "max_length": self.max_length,
            "top_p":self.top_p,
            **self.model_kwargs,
        }
        return parm

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

    text="""
你的任务是根据***分隔符的历史对话沟通记录，从user和assistant聊天记录理解user需求，并从聊天记录抽取正确的结构值以结构化数据格式返回，取不到的值使用None代替,
时间字段直接从user聊天抽取不出来需结合系统当前时间推理,系统当前时间2023-11-14 15:14:05,比如则根据系统当前时间推理:今天的日期为2023-11-14 00:00:00,严格禁止生成聊天记录不存在的数据,
输出应该是严格按以下模式格式化的标记代码片段，必须包括开头和结尾的" ' ' ' json"和" ' ' ' ":
```json
{
	"shop_name": STRING  // 店铺名称，抽取不到时使用"None"代替.
	"begin_time": STRING  // 开始时间(YYYY-MM-HH)，抽取不到时使用"None"代替
	"end_time": STRING  // 结束时间(YYYY-MM-HH)，抽取不到时使用"None"代替
}
历史对话沟通记录：
***
user:前天366大街早上八点十分钟到晚上六点半的销售量
***
你的回答:
"""

    for i in range(100):

        res = llm.predict(text)
        print(i,res)