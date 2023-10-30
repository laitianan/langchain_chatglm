

import requests
import json 


##初始化接口模板
post_json = json.dumps({"params":[
    
    {"name":"订单查询","id":"888","functionDesc":"查询某订单详细信息","usableFlag":1,"inputParams":
      [{"name":"order_id","type":"string","required":1,"title":"订单ID"},{"name":"datetime","type":"string","required":1,"title":"订单时间"}]},
        
    {"name":"销量查询","id":"999","functionDesc":"查询店铺的销量","usableFlag":1,"inputParams":
      [{"name":"shop_name","type":"string","required":1,"title":"店铺名称"},{"name":"begin_time","type":"string","required":1,"title":"查询开始时间"},{"name":"end_time","type":"string","required":1,"title":"查询结束时间时间"}]}
    
    ]})

# r1 = requests.post("http://61.141.232.106:8084/init_funtion_template/completions", data=post_json)
# print(r1.content.decode("utf8"))

# r1 = requests.post("http://127.0.0.1:8084/init_funtion_template/completions", data=post_json)
# print(r1.content.decode("utf8"))
# r1 = requests.post("http://127.0.0.1:8084/delete_all_funtion_template/completions")
# print(r1.content.decode("utf8"))


# r1 = requests.post("http://61.141.232.106:8084/delete_all_funtion_template/completions")
# print(r1.content.decode("utf8"))



####聊天接口
# post_json=json.dumps({"message":[{"role": "user", "content": "请问你叫什么"},{"role":"assistant","content":"我是来自阿里云的大规模语言模型，我叫通义千问。"},{"role": "user", "content": "你可以解决什么样的问题呢"}]})

# r1 = requests.post("http://61.141.232.106:8084/chat/completions", data=post_json)
# print(r1.content.decode("utf8"))


# post_json=json.dumps({"message":"你好"})
# r1 = requests.post("http://61.141.232.106:8084/chat/completions", data=post_json)
# print(r1.content.decode("utf8"))


#意图查询
# post_json=json.dumps({"message":[{"role": "user", "content": "西红柿怎么炒"}]})
# r1 = requests.post("http://61.141.232.106:8084/chat_funtion_intention/completions", data=post_json)
# print(r1.content.decode("utf8"))

# ##
# post_json=json.dumps({"funtion_id":"888","message":[{"role": "user", "content": "我想查询订单456789在今年八月一号的的详情"}]})
# r1 = requests.post("http://61.141.232.106:8084/chat_funtion/completions", data=post_json)
# print(r1.content.decode("utf8"))






post_json=json.dumps({"funtion_id":"888","message":
                      [{"role": "user", "content": "我想查询订单45689654的详情"},
                        {"role": "assistant", "content": "请明确告诉我要查询的日期是"},
                        {"role": "user", "content": "我想查询十五天前的"}]})

r1 = requests.post("http://61.141.232.106:8084/chat_funtion/completions", data=post_json)
print(r1.content.decode("utf8"))


