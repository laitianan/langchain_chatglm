
import requests
import json

base_url="127.0.0.1:8084"
# base_url="61.141.232.106:8084"

#初始化接口模板
post_json = json.dumps({"params" :[

    {
        "name": "订单号查询",
        "id": "2114",
        "functionDesc": "通过订单号查询订单详情",
        "businessTypeNames": "其它业务,商城业务",
        "businessSonTypeNames": "其它子业务,现烤店业务",
        "usableFlag": False,
        "inputParams": [
            {
                "name": "orderNo",
                "type": "STRING",
                "required": True,
                "title": "订单号"
            }
        ]
    },
    {
        "name": "查某一天下单总量",
        "id": "2116",
        "functionDesc": "查询具体日期的下单总量",
        "businessTypeNames": "商城业务,零售业务",
        "businessSonTypeNames": "其它子业务",
        "usableFlag": False,
        "inputParams": [
            {
                "name": "day",
                "type": "STRING",
                "required": True,
                "title": "日期"
            }
        ]
    },
    {
        "name": "门店当天实时业绩查询",
        "id": "2117",
        "functionDesc": "门店当天实时业绩查询",
        "businessTypeNames": "零售业务,商城业务",
        "businessSonTypeNames": "其它子业务",
        "usableFlag": False,
        "inputParams": [
            {
                "name": "shop_name",
                "type": "STRING",
                "required": True,
                "title": "店铺名称"
            }
        ]
    },
    {
        "name": "门店按天查询业绩",
        "id": "2118",
        "functionDesc": "门店按天查询业绩",
        "businessTypeNames": "其它业务",
        "businessSonTypeNames": "其它子业务",
        "usableFlag": False,
        "inputParams": [
            {
                "name": "day",
                "type": "STRING",
                "required": True,
                "title": "日期"
            },
            {
                "name": "shop_name",
                "type": "STRING",
                "required": True,
                "title": "店铺名称"
            }
        ]
    },
    {
        "name": "站点当天实时业绩查询",
        "id": "2119",
        "functionDesc": "站点当天实时业绩查询",
        "businessTypeNames": "其它业务",
        "businessSonTypeNames": "其它子业务",
        "usableFlag": False,
        "inputParams": [
            {
                "name": "shop_name",
                "type": "STRING",
                "required": True,
                "title": "站点名称"
            }
        ]
    },
    {
        "name": "站点按天查询业绩",
        "id": "2120",
        "functionDesc": "站点按天查询业绩",
        "businessTypeNames": "其它业务",
        "businessSonTypeNames": "其它子业务",
        "usableFlag": False,
        "inputParams": [
            {
                "name": "day",
                "type": "STRING",
                "required": True,
                "title": "日期"
            },
            {
                "name": "shop_name",
                "type": "STRING",
                "required": True,
                "title": "站点名称"
            }
        ]
    }

]})





r1 = requests.post(f"http://{base_url}/init_funtion_template/completions", data=post_json)
print(r1.content.decode("utf8"))

# r1 = requests.post(f"http://{base_url}/init_funtion_template/completions", data=post_json)
# print(r1.content.decode("utf8"))
# r1 = requests.post(f"http://{base_url}/delete_all_funtion_template/completions")
# print(r1.content.decode("utf8"))
# r1 = requests.post(f"http://{base_url}/get_all_template/completions")
# print(r1.content.decode("utf8"))


# import requests
# import json
# r1 = requests.post(f"http://{base_url}/get_all_template/completions")
# print(r1.content.decode("utf8"))


# r1 = requests.post(f"http://{base_url}/delete_all_funtion_template/completions")
# print(r1.content.decode("utf8"))



####聊天接口
# post_json=json.dumps({"message":[{"role": "user", "content": "我想查询订单456的详情"},
#                                  {"role":"function","content":'{"订单时间": "2023-11-27", "数量": "1", "金额":"178","配送状态": "正在配送之中","商品名称":"黑森林蛋糕","配送城市":"深圳南山"}'
#                                   }]})

# r1 = requests.post(f"http://{base_url}/chat/completions", data=post_json)
# print(r1.content.decode("utf8"))


# post_json=json.dumps({"message":"你好"})
# r1 = requests.post(f"http://{base_url}/chat/completions", data=post_json)
# print(r1.content.decode("utf8"))

import time

# function()   运行的程序

# 意图查询
import numpy as np
strs=["查询今天下午六点366大街的业绩"]
# strs=["查询今天366大街的业绩"]
for i in range(0):
    print("------------------------------------------------------------------")
    start_time = time.time()    # 程序开始时间
    query=np.random.choice(strs,1)[0]
    post_json =json.dumps({"message" :[{"role": "user", "content": query}]})
    r1 = requests.post(f"http://{base_url}/chat_intention_search/completions", data=post_json)
    # r1 = requests.post(f"http://{base_url}/chat_funtion_intention/completions", data=post_json)
    # print(r1.content.decode("utf8"))
    js=json.loads(r1.content.decode("utf8"))
    # print(js["message"])
    print(i,query)
    print(js)
    end_time = time.time()    # 程序结束时间
    run_time = end_time - start_time    # 程序的运行时间，单位为秒
    print(run_time)
    if js["status"]==402:
        break
import re 
# json_string='```json\n{\n    "intention_name": "销量查询"\n}\n```'
# json_string='" \' \' \' json"\n{ \n    "intention_name": "意图不明" \n}'
# match = re.search(r"```(json)?(.*)```", json_string, re.DOTALL)


from ast import literal_eval


def parse_json_markdown(json_string: str) -> dict:
    """
    Parse a JSON string from a Markdown string.

    Args:
        json_string: The Markdown string.

    Returns:
        The parsed JSON object as a Python dictionary.
    """
    # Try to find JSON string within triple backticks
    match = re.search(r"```(json)?(.*)```", json_string, re.DOTALL)

    # If no match found, assume the entire string is a JSON string
    if match is None:
        json_str = json_string
    else:
        # If match found, use the content within the backticks
        json_str = match.group(2)

    # Strip whitespace and newlines from the start and end
    json_str = json_str.strip()
    parsed= literal_eval(json_str)
    # Parse the JSON string into a Python dictionary
    # parsed = json.loads(json_str)
    return parsed

# res=parse_json_markdown(json_string)
# print(res)
# r1 = requests.post(f"http://{base_url}/chat_funtion_intention/completions", data=post_json)
# print(r1.content.decode("utf8"))

# ##
# post_json=json.dumps({"funtion_id":"888","message":[{"role": "user", "content": "我想查询订单456789在今年八月一号的的详情"}]})
# r1 = requests.post(f"http://{base_url}/chat_funtion/completions", data=post_json)
# print(r1.content.decode("utf8"))



# post_json=json.dumps({"funtion_id":"888","message":
#                       [{"role": "user", "content": "我想写一份策划书"},
#                         {"role": "assistant", "content": "1.----，2----3.*******，请你选择需求"},
#                         {"role": "user", "content": "3"}]})




# r1 = requests.post(f"http://{base_url}/chat_funtion/completions", data=post_json)
# print(r1.content.decode("utf8"))

# -*- coding: utf-8 -*-
# """
# Created on Thu Nov  9 18:08:31 2023

# @author: 98608
# """


# mp={
#     "订单售后查询":"根据用户订单ID查询用户订单售后信息",
#     "订单状态查询":"根据用户订单ID查询用户订单状态信息",
#     "订单配送查询":"根据用户订单ID查询用户订单目前配信息",
#     "订单数据查询":"根据用户订单ID查询用户订单数据信息",
#     "门店当天实时业绩查询":"门店当天实时业绩查询",
#     "站点当天实时业绩查询":"站点当天实时业绩查询"
#     }


# summary=[]
# for i,key in enumerate(mp):
#     summary.append(f"{i+1}、{key}:{mp[key]}")

# summary="\n".join(summary)

# user_input="订单查询"

# INTENT_FORMAT_INSTRUCTIONS: str = """
# 现在有一些意图，类别为：{intents}，
# 你扮演AI角色的任务是根据***分隔符的文本对话，来进行意图的识别`，对话中可能存在多轮对话意图，仅仅需要判断该对话user最后一个问题属于哪一类别意图。
# 输出应该是严格按以下模式格式化的标记代码片段，必须包括开头和结尾的" ' ' ' json"和" ' ' ' ":
# ```json
# {{
#     "intention_name": string  // 意图类别，意图类别必须在提供的类别中
# }}
# ```
# 备注意图详情描述：
# {intention_summary}
# ***
# 历史对话沟通记录：
# {user_input}
# ***
# 你的回答：
# """

# query=INTENT_FORMAT_INSTRUCTIONS.format(intents=list(mp.keys()),intention_summary=summary,user_input=user_input)




# python -m fastchat.serve.vllm_worker --model-path /data/laitianan/qwen-14b-4bit --trust-remote-code













# curl http://192.168.0.11:8081/v1/chat/completions \
# -X POST \
#   -H "Content-Type: application/json" \
#   -d '{
#       "model": "qwen-14b-4bit",
#       "messages": [{"role": "user", "content": "Say this is a test!"}],
#       "temperature": 0.7
#     }' 





# curl http://localhost:8081/v1/completions \
#   -H "Content-Type: application/json" \
#   -d '{
#     "model": "qwen-14b-4bit",
#     "prompt": "Say this is a test!",
#     "max_tokens": 2000,
#     "temperature": 0.7
#   }'


# python -m fastchat.serve.vllm_worker --model-path "/home/ubuntu/.cache/modelscope/hub/qwen/Qwen-14B-Chat" --trust-remote-code




