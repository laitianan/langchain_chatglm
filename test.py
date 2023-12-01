#!/usr/bin/env python
# coding: utf-8
# encoding:utf-8
# In[14]:


import os
import pandas as pd
import json
import inspect
import openai
import openai
from  utils import parse_json_markdown 
openai.api_base = "http://192.168.0.11:8081/v1"
openai.api_key = "none"



def call_qwen(messages, functions=None):
    # print(f"input\t{messages}")
    if functions:
        response = openai.ChatCompletion.create(
            model="Qwen", messages=messages, functions=functions
        )
    else:
        response = openai.ChatCompletion.create(model="Qwen", messages=messages)
    # print(response)
    # print("output\t"+response.choices[0].message.get("content",""))
    return response




def test_2():
    functions = [
        {
            "name_for_human": "谷歌搜索",
            "name_for_model": "google_search",
            "description_for_model": "谷歌搜索是一个通用搜索引擎，可用于访问互联网、查询百科知识、了解时事新闻等。"
            + " Format the arguments as a JSON object.",
            "parameters": [
                {
                    "name": "search_query",
                    "description": "搜索关键词或短语",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
        },
        {
            "name_for_human": "天气预报查询",
            "name_for_model": "query_weather",
            "description_for_model": "根据用户输入的时间与城市地址，返回用户指定在特定日期特定城市天气预报"
            + " Format the arguments as a JSON object.",
            "parameters": [
                {
                    "name": "datetime",
                    "description": "日期时间",
                    "required": True,
                    "schema": {"type": "datetime"},
                },
                {
                    "name": "city",
                    "description": "城市",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
        },
    ]

    def get_time():
        import datetime
        current_time = datetime.datetime.now()
        current_time = str(current_time)[:19]
        return current_time

    messages = [{"role": "system", "content":f"当前北京时间是：{get_time()}"}]
    while True:
        user_input=input("请你输入你的问题：")
        if user_input=="clear":
            messages = [{"role": "system", "content":f"当前北京时间是：{get_time()}"}]
            continue
        messages.append({"role": "user", "content": user_input})
        resp=call_qwen(messages, functions)
        # resp=json.loads(resp, ensure_ascii=False)
        if resp.choices[0].finish_reason=="stop":
            print("9999999999999999999999999999999999999999999999999")
            messages.append(
                {"role": "assistant", "content":resp.choices[0].message.content},
            )
        else:
            # print(resp.choices[0].message)
            # print(type(resp.choices[0].message.to_dict()))
            import json

            data = resp.choices[0].message.to_dict()
            json_data = json.dumps(data, ensure_ascii=False)
            print(json_data)
            print("8"*100)
            json_data=json.loads(json_data)
            messages.append(
                json_data
            )

            if resp.choices[0].message.function_call["name"]=="query_weather":
                param=resp.choices[0].message.function_call["arguments"]
                param = json.loads(param)
                print(param)
                info=""
                if not param.get("datetime",None):
                    info+="不知道用户查询日期，"
                if not param.get("city",None):
                    info+="不知道用户查询城市名称"
                city=param.get("city",None)
                datetime=param.get("datetime",None)
                import numpy as np
                weathers=["晴朗","小雨","大暴雨","小雪","雾霭"]
                weather = np.random.choice(weathers, 1)[0]
                temps=["适中","20米","100米","好"]
                temp = np.random.choice(temps, 1)[0]
                info=info or f"城市：{city},日期时间：{datetime},当天的天气预报为气温{np.random.randint(-10,37,1)[0]}度，天气{weather}，能见度{temp}"
                # print(info)
                messages.append(
                    {
                        "role": "function",
                        "name": "query_weather",
                    "content":info})
            else:

                messages.append(
                    {
                        "role": "function",
                        "name": "google_search",
                        "content": """周杰伦（Jay Chou），1979年1月18日出生于台湾省新北市，祖籍福建省泉州市永春县，中国台湾流行乐男歌手、音乐人、演员、导演、编剧，毕业于淡江中学。
    2000年发行个人首张专辑《Jay》 [303] 。2001年发行的专辑《范特西》奠定其融合中西方音乐的风格。2002年举行“The One”世界巡回演唱会 [1] 。2003年成为美国《时代周刊》封面人物 [2] 。2004年凭借专辑《叶惠美》获得第15届台湾金曲奖最佳流行音乐演唱专辑奖 [23] 。2005年凭借动作片《头文字D》获得金马奖、金像奖最佳新人奖 [3] 。2006年起连续三年获得世界音乐大奖中国区最畅销艺人奖 [4] 。2007年自编自导的文艺片《不能说的秘密》获得金马奖年度台湾杰出电影奖 [5] 。2008年凭借歌曲《青花瓷》获得第19届台湾金曲奖最佳年度歌曲奖、最佳作曲人奖 [307] 。
    2009年入选美国CNN评出的“25位亚洲最具影响力人物” [6] ；同年凭借专辑《魔杰座》获得第20届台湾金曲奖最佳国语男歌手奖 [7] 。2010年入选美国《Fast Company》评出的“全球百大创意人物”。2011年凭借专辑《跨时代》获得第22届台湾金曲奖最佳国语男歌手奖、最佳国语专辑奖 [309] 。2012年登上福布斯中国名人榜榜首 [8] 。2014年发行个人首张数字专辑《哎呦，不错哦》 [310] 。2023年凭借专辑《最伟大的作品》获得IFPI全球畅销专辑榜冠军 [301] 。
    周杰伦热心公益慈善 [325] ，还涉足商业、设计等领域 [324] ，多次向中国内地灾区捐款捐物。2007年成立杰威尔有限公司 [10] 。2008年捐款援建希望小学 [12] 。2011年担任华硕笔电设计师 [11] 。2014年担任中国禁毒宣传形象大使 [183] 。""",
                    }
                )
            resp = call_qwen(messages, functions)
            messages.pop(-1)
            messages.pop(-1)
            messages.append(
                {"role": "assistant", "content": resp.choices[0].message.content},
            )
        content=resp.choices[0].message.get("content", "")
        print(f"AI回复:{content}")

if __name__ == "__main__":
    # print("### Test Case 1 - No Function Calling (普通问答、无函数调用) ###")
    # test_1()
    # print("### Test Case 2 - Use Qwen-Style Functions (函数调用，千问格式) ###")
    test_2()
    # print("### Test Case 3 - Use GPT-Style Functions (函数调用，GPT格式) ###")
    # test_3()
    # print("### Test Case 4 - Use LangChain (接入Langchain) ###")
    # test_4()