
import requests
import json

base_url="127.0.0.1:8084"
base_url="61.141.232.106:8084"

##初始化接口模板
post_json = json.dumps({"params" :[

    {"name" :"订单查询" ,"id" :"888" ,"functionDesc" :"查询某订单详细信息" ,"usableFlag" :0 ,"inputParams":
        [{"name" :"order_id" ,"type" :"string" ,"required" :1 ,"title" :"订单ID"}]},

    {"name" :"销量查询" ,"id" :"999" ,"functionDesc" :"查询店铺的销量" ,"usableFlag" :0 ,"inputParams":
        [{"name" :"shop_name" ,"type" :"string" ,"required" :1 ,"title" :"店铺名称"}
          ,{"name" :"begin_time" ,"type" :"string" ,"required" :1 ,"title" :"查询开始时间"}
          ,{"name" :"end_time" ,"type" :"string" ,"required" :1 ,"title" :"查询结束时间时间"}]}

]})

# r1 = requests.post(f"http://{base_url}/init_funtion_template/completions", data=post_json)
# print(r1.content.decode("utf8"))

# r1 = requests.post(f"http://{base_url}/init_funtion_template/completions", data=post_json)
# print(r1.content.decode("utf8"))
# r1 = requests.post(f"http://{base_url}/delete_all_funtion_template/completions")
# print(r1.content.decode("utf8"))
# r1 = requests.post(f"http://{base_url}/get_all_template/completions")
# print(r1.content.decode("utf8"))

# r1 = requests.post(f"http://{base_url}/get_all_template/completions")
# print(r1.content.decode("utf8"))


# r1 = requests.post(f"http://{base_url}/delete_all_funtion_template/completions")
# print(r1.content.decode("utf8"))



####聊天接口
# post_json=json.dumps({"message":[{"role": "user", "content": "请问你叫什么"},{"role":"assistant","content":"我是来自阿里云的大规模语言模型，我叫通义千问。"},{"role": "user", "content": "你可以解决什么样的问题呢"}]})

# r1 = requests.post(f"http://{base_url}/chat/completions", data=post_json)
# print(r1.content.decode("utf8"))


# post_json=json.dumps({"message":"你好"})
# r1 = requests.post(f"http://{base_url}/chat/completions", data=post_json)
# print(r1.content.decode("utf8"))

import time

# function()   运行的程序

# 意图查询
import numpy as np
strs=["查询订单123456","你好","查询销量"]
for i in range(5):
    print("------------------------------------------------------------------")
    start_time = time.time()    # 程序开始时间
    query=np.random.choice(strs,1)[0]
    post_json =json.dumps({"message" :[{"role": "user", "content": query}]})
    r1 = requests.post(f"http://{base_url}/chat_funtion_intention/completions", data=post_json)
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

# json_string="""```json
# {
# 	"orderNo": "西饼西饼"
# }
# ```"""
# import re
# import json
# match = re.search(r"```(json)?(.*)```", json_string, re.DOTALL)

# # If no match found, assume the entire string is a JSON string
# if match is None:
#     json_str = json_string
# else:
#     # If match found, use the content within the backticks
#     json_str = match.group(2)

# # Strip whitespace and newlines from the start and end
# json_str = json_str.strip()

# # Parse the JSON string into a Python dictionary
# parsed = json.loads(json_str)

# print(parsed)

# 你前端可以给可以做的任务提示的，比如
# """
# sorry,不是很明白你的意思。我可以提供一下帮助
# 1.订单查询
# 2.销量查询
# 3.财务查询

# """











a='"{\'intention_name\': \'意图不明\'}"'














