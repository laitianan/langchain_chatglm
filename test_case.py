
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
          }
        ]
      },
      


]})





# r1 = requests.post(f"http://{base_url}/init_funtion_template/completions", data=post_json)
# print(r1.content.decode("utf8"))

# base_url="127.0.0.1:8084"
# for i in range(100):
#     r1 = requests.post(f"http://{base_url}/get_all_template/completions")
#     # print(r1.content.decode("utf8"))
#     content=r1.content.decode("utf8")
#     if "查某一天下单总量"in content:
#         # print(content)
#         print("yes")
#     else:
#         print("None")
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


cont="""[{"渠道名称":"线下收银","渠道id":21},{"渠道名称":"门店收银","渠道id":22},{"渠道名称":"门店收银（有赞）","渠道id":23},{"渠道名称":"外卖渠道-美团外卖西饼","渠道id":31},{"渠道名称":"外卖渠道-饿了么西饼","渠道id":32},{"渠道名称":"无人售货机","渠道id":396},{"渠道名称":"新零售APP","渠道id":437},{"渠道名称":"幸福西饼GO小程序","渠道id":1101},{"渠道名称":"新零售APP","渠道id":1102},{"渠道名称":"幸福西饼DIY","渠道id":1104},{"渠道名称":"智慧零售小程序","渠道id":1105},{"渠道名称":"幸福西饼生日蛋糕自烤面包","渠道id":1106},{"渠道名称":"幸福商城","渠道id":1301},{"渠道名称":"星厨","渠道id":1302},{"渠道名称":"中石化商城","渠道id":1303},{"渠道名称":"新零售商城","渠道id":1304},{"渠道名称":"鹏福供应商城","渠道id":1305},{"渠道名称":"团购频道","渠道id":1306},{"渠道名称":"农行商城","渠道id":1307},{"渠道名称":"商城团购频道","渠道id":1308},{"渠道名称":"自营团购","渠道id":1309},{"渠道名称":"幸福送H5","渠道id":1310},{"渠道名称":"B端商城","渠道id":1311},{"渠道名称":"外卖渠道-饿了么切件","渠道id":3202},{"渠道名称":"有赞-王森世界名厨蛋糕","渠道id":3304},{"渠道名称":"有赞-幸福西饼微信商城","渠道id":3305},{"渠道名称":"有赞-幸福先生旗舰店","渠道id":3307},{"渠道名称":"有赞-喜芝派","渠道id":3308},{"渠道名称":"有赞-幸福西饼糕点铺","渠道id":3309},{"渠道名称":"有赞-幸福in成都","渠道id":3310},{"渠道名称":"秋华蓝卡","渠道id":3601},{"渠道名称":"苏州中国银行","渠道id":3602},{"渠道名称":"第三方小渠道-东方福利网","渠道id":3603},{"渠道名称":"商城大客户部-生活榜样","渠道id":3604},{"渠道名称":"第三方小渠道-花礼网","渠道id":3605},{"渠道名称":"丰食","渠道id":3606},{"渠道名称":"第三方小渠道-礼舍网","渠道id":3608},{"渠道名称":"第三方小渠道-联联周边游","渠道id":3609},{"渠道名称":"第三方小渠道-云闪付银联","渠道id":3610},{"渠道名称":"商城大客户部-品诺","渠道id":3611},{"渠道名称":"商城大客户部-熊猫优福","渠道id":3612},{"渠道名称":"商城大客户部-优荟加","渠道id":3613},{"渠道名称":"商城大客户部-聚福宝","渠道id":3614},{"渠道名称":"电商渠道-拼多多","渠道id":3701},{"渠道名称":"美团团购配送","渠道id":31001},{"渠道名称":"外卖渠道-美团外卖星厨","渠道id":31002},{"渠道名称":"外卖渠道-饿了么星厨","渠道id":32001},{"渠道名称":"电商渠道-京东旗舰店","渠道id":39101},{"渠道名称":"电商渠道-京东自营店","渠道id":39102},{"渠道名称":"京东-幸福先生旗舰店","渠道id":39103},{"渠道名称":"电商渠道-京东食品店","渠道id":39104},{"渠道名称":"电商渠道-天猫旗舰店","渠道id":39202},{"渠道名称":"第三方小渠道-考拉订蛋糕","渠道id":40423},{"渠道名称":"第三方小渠道-盒马鲜生","渠道id":40424},{"渠道名称":"团购渠道-支付宝口碑","渠道id":40438},{"渠道名称":"团购渠道-美团点评","渠道id":40439},{"渠道名称":"团购渠道-抖音","渠道id":40441},{"渠道名称":"团购渠道-快手","渠道id":40442},{"渠道名称":"商城大客户部","渠道id":40712},{"渠道名称":"售后单","渠道id":40715},{"渠道名称":"全名营销订单","渠道id":40744},{"渠道名称":"抖店-幸福西饼官方旗舰店","渠道id":300101},{"渠道名称":"抖店-幸福西饼烘焙旗舰店","渠道id":300102},{"渠道名称":"外卖渠道-抖音外卖","渠道id":360701},{"渠道名称":"小渠道","渠道id":4044041},{"渠道名称":"市场部免费单","渠道id":4070926},{"渠道名称":"市场部销售单","渠道id":4070927}]"""
####聊天接口
post_json=json.dumps({
    "message":[{"role": "user", "content": "订单xs456详情和今天366大街门店业绩"},
                                  ]})
base_url="127.0.0.1:8084"
r1 = requests.post(f"http://{base_url}/chat_all_links/completions", data=post_json)
print(r1.content.decode("utf8"))


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



 