# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 18:00:53 2023

@author: admin
"""
import json 
import requests
import time 

text2="""
你的任务是根据***分隔符的历史对话沟通记录，从user和assistant聊天记录理解user需求，并从聊天记录抽取正确的结构值以结构化数据格式返回，取不到的值使用null代替，不能虚拟用户表达不存在的数据,比如用户说查询订单的详情，因为没有表明订单ID,所以属性orderNo为空，返回{{"orderNo":null}},
部分时间直接从user聊天抽取不出来才结合系统当前时间推理,系统当前时间2023-11-28 16:48:34,比如则根据系统当前时间推理:今天的开始日期时间为2023-11-28 00:00:00,今天的结束日期时间为2023-11-28 23:59:59,严格禁止生成聊天记录不存在的数据,
输出应该是严格按以下模式格式化的标记代码片段，必须包括开头和结尾的" ' ' ' json"和" ' ' ' ":

```json
{
	"orderNo": STRING  // 订单号，抽取不到时使用null代替
    "day": STRING  // 日期(yyyy-MM-dd)，抽取不到时使用null代替
    "shop_name": STRING  // 店铺名称，抽取不到时使用null代替
}

历史对话沟通记录：
***
user:我想366大街昨天的订单为的详情
***
你的回答:
"""
strs=[text2]
# data=json.dumps({
#     "messages": strs,
#   })
# begin=time.time()
# r1 = requests.post(f"http://192.168.0.11:8081/v1/batch_chat/completions", headers={'Content-Type': 'application/json'},data=data)
# res = json.loads(r1.content.decode("utf8"))
# end=time.time()
# # print(res)
# print(end-begin)


class openai_model():

    def __init__(self,max_tokens = 2000,temperature=0.8):
        self.temperature=temperature
        self.max_tokens=max_tokens
        self.base_url="192.168.0.11:8000"
    def predict(self,messages):
        history = []
        if isinstance(messages,str):
            history.append({"role": "user", "content": messages})
        else:
            for mess in messages:
                history.append({"role": mess.role, "content": mess.content})
        data=json.dumps({
            "model": "Qwen-7B-Chat",
            "messages": history,
            "stream": False,
            "max_tokens":self.max_tokens,
            "temperature": self.temperature
          })
        r1 = requests.post(f"http://192.168.0.11:8081/v1/chat/completions", headers={'Content-Type': 'application/json'},data=data)
        # res = json.loads(r1.content.decode("utf8"))
        # content=res["choices"][0]["message"]["content"]
        return r1.content
from ast import literal_eval
import re 
from utils import  parse_json_markdown,get_current_weekday
obj=openai_model()
begin=time.time()
for mess in strs:
    for i in range(10):
        resps = obj.predict(mess)
        # print(res)
        resp = json.loads(resps.decode("utf8"))
        try:
            res=resp["choices"][0]["message"]["content"]
            print("解析之前的值："+res)
            res=parse_json_markdown(res)
            print(f"解析后的值：{res}")
            print("------------------------------------------------------")
        except Exception as e :
            
            print("Exception:"+str(e))
    
end=time.time()
json_string=res

# match = re.search(r"```(json)?(.*)```", json_string, re.DOTALL)
# if match is None:
#     match = re.search(r"{.*}", json_string, re.DOTALL)
#     if match is None:
#         json_str = json_string
#     else:
#         json_str = match.group(0)
#         # print("8"*20,json_str)
# else:
#     json_str = match.group(2)
#     # print("9" * 20,json_str)

# json_str = json_str.strip()
# try:
#     try:
        
#         return literal_eval(json_str)
#     except:
#         return json.loads(json_str)
# except:
#     match = re.findall(r"(//(.*?))[\n]", json_str, re.DOTALL)
#     for e in match:
#         json_str = json_str.replace(e[0], "")

for k,v in res.items():
    res[k]="12"