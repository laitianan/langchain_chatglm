
import requests
import json

base_url="127.0.0.1:8084"
# base_url="61.141.232.106:8084"

#初始化接口模板
post_json = json.dumps({"params" :[

{
        "name": "查某一天下单总量",
        "id": "2116",
        "functionDesc": "查询具体日期的下单总量",
        "businessTypeNames": "商城业务,零售业务",
        "businessSonTypeNames": "其它子业务",
        "usableFlag": True,
        "inputParams": [
          {
            "name": "day",
            "type": "STRING",
            "required": True,
            "title": "日期(yyyy-MM-dd)"
          },
          {
            "name": "businessTypeNames",
            "type": "STRING",
            "required": True,
            "title": "业务类型[新零售业务,商场业务]"
          }
        ]
      },




]})





# r1 = requests.post(f"http://{base_url}/init_funtion_template/completions", data=post_json)
# print(r1.content.decode("utf8"))

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
# strs=["业绩"]
# strs=["查询今天366大街的业绩"]
ress=set()
for i in range(1):
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
    ress.add(str(js))
    end_time = time.time()    # 程序结束时间
    run_time = end_time - start_time    # 程序的运行时间，单位为秒
    print(run_time)
    if js["status"]==402:
        break
import re 
# json_string='```json\n{\n    "intention_name": "销量查询"\n}\n```'
# json_string='" \' \' \' json"\n{ \n    "intention_name": "意图不明" \n}'
# match = re.search(r"```(json)?(.*)```", json_string, re.DOTALL)



 