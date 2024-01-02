# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 15:35:36 2023

@author: admin
"""



import requests
import json 
import time
base_url="61.141.232.106:8084"

while True:
    history=[]
    user_input=input("用户输入:")
    t0 = time.time()
    # user_input="订单查询"
    history.append({"role": "user", "content":user_input})
    post_json=json.dumps({"message":history})
    r1 = requests.post(f"http://{base_url}/chat_multi_intention/completions", data=post_json)
    c=r1.content.decode("utf8")
    # print(f"--------------忽略这段输出:{c}-------------------------")
    
    resp=json.loads(r1.content.decode("utf8"))
    if resp["status"]==200:
        funname_resp=[]
        tools=resp["tools"]
        for tool in tools :

            message=json.loads(tool["message"])
            if len(message.items())>0:
                parm_none=[k for k ,v in message.items() if v==None ]
                cont=f"需要用户提供{parm_none}，才可查询"
            else:
                parm_none=[]
                cont="查询信息不详"
            if tool["funtion_id"]=='2114':
                cont="""{"订单号":"XS2023121515590681195","配送时间":"2023-12-15 19:30:00到21:00:00","订单id":1185249689478250496,"订单状态":"待备货"}"""
            elif tool["funtion_id"]=='2130':
                cont="""[{"商品名称":"四重奏","排名":"NO1"},{"商品名称":"甜心莓莓","排名":"NO2"}]"""
            elif tool["funtion_id"]=='2122':
                cont="""每天完成三千万订单"""
            elif tool["funtion_id"]=='2123':
                cont="""{"数量":300}"""
                
                
                
                
                
                
                
                
                
            elif tool["funtion_id"]=='2118':
                cont="""{"日期":"2023-12-29"","销量":1456}"""
            funname_resp.append({"funtion_id":tool["funtion_id"], "resp": cont })
            # print(cont)
            
        post_json=json.dumps({"funname_resp":funname_resp,"message":history})

        r1 = requests.post(f"http://{base_url}/beautify_chat/completions", data=post_json)
        res=json.loads(r1.content.decode("utf8"))
        
        history.append({"role": res["role"], "content":res["message"]})
        resp_content=res["message"]
        print(f"AI回复:{resp_content}")
        t02 = time.time()
        print("总耗时(秒):", t02 - t0)
    # break



