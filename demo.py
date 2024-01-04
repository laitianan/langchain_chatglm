# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 15:35:36 2023

@author: admin
"""
import requests
import json 
import time
base_url="61.141.232.106:8084"
base_url="127.0.0.1:8084"
history=[]
while True:
    
    user_input=input("用户输入:")
    if user_input=="clear":
        history=[]
        continue
    t0 = time.time()
    # user_input="订单查询"
    history.append({"role": "user", "content":user_input})
    post_json=json.dumps({"message":history})
    r1 = requests.post(f"http://{base_url}/chat_multi_intention/completions", data=post_json)
    c=r1.content.decode("utf8")
    print(f"--------------忽略这段输出:{c}-------------------------")
    t02 = time.time()
    print("意图识别参数解析耗时(秒):", t02 - t0)
    resp=json.loads(r1.content.decode("utf8"))
    if resp["status"]==200:
        funname_resp=[]
        tools=resp["tools"]
        for tool in tools :
            print(f"--------------忽略这段输出:{tool}-------------------------")
            message=json.loads(tool["message"])
            if len(message.items())>0:
                
                parm_none=[k for k ,v in message.items() if v==None ]
                if parm_none:
                    parm_none="、".join(parm_none)
                    cont=f"请用户提供{parm_none}，才可查询"
                else:
                    parm_none=[]
            else:
                parm_none=[]
                cont="暂未能提供该业务查询"
            
            if tool["funtion_id"]=='2114' and not parm_none  :
                cont="""{"订单号":"XS2023121515590681195","配送时间":"2023-12-15 19:30:00到21:00:00","订单id":1185249689478250496,"订单状态":"待备货"}"""
                cont=cont.replace("XS2023121515590681195", message["orderNo"])
            elif tool["funtion_id"]=='2130':
                cont="""[{"商品名称":"四重奏","排名":"NO1"},{"商品名称":"甜心莓莓","排名":"NO2"}]"""
            elif tool["funtion_id"]=='2122' :
                cont="""每天完成三千万订单"""
            elif tool["funtion_id"]=='2123':
                cont="""{"数量":300}"""                
            elif tool["funtion_id"]=='2118' and not parm_none:
                cont="""{"日期":"2024-01-01"","销量":1300}"""
    
            elif tool["funtion_id"]=='2117' and not parm_none:
                cont="""{"日期":"2024-01-02"","销量":1456}"""
    
            elif tool["funtion_id"]=='2116' and not parm_none:
                cont="""{"日期":"2024-01-01"","销量":1500}"""
    
            else:
                # cont="暂未能提供该业务查询"
                pass
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



