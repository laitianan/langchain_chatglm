
import time

import uvicorn
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Literal, Optional, Union
import  logging
import pickle
import os
from langchain.agents import AgentExecutor
from intentAgent_model import IntentAgent
from tool_model import Model_Tool, Unknown_Intention_Model_Tool
from MyOpenAI import myOpenAi,openai_model
from prompt_helper import init_all_fun_prompt
from utils import load_interface_template,save_interface_template
app = FastAPI()
saveinterfacepath="./data/"
from api_protocol import  (
InitInterfaceResponse,
InitInterfaceRequest,
ChatCompletionRequest,
ChatCompletionResponse,
FunCompletionRequest
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat/completions", response_model=ChatCompletionResponse)
async def init(request: ChatCompletionRequest):
    llm=openai_model()
    resp=llm.predict(request)
    return ChatCompletionResponse(status=200,message=resp)

@app.post("/init_funtion_template/completions", response_model=InitInterfaceResponse)
async def init(request: InitInterfaceRequest):
    global  initparam
    print(request)
    if initparam  :
        interface_fun = {param.id:param for param in initparam.params}
        for param in request.params:
            interface_fun[param.id] = param
            if not param.usableFlag:
                del interface_fun[param.id]
        initparam.params=list(interface_fun.values())
    else:
        initparam=request
    save_interface_template(initparam, path=saveinterfacepath)
    return InitInterfaceResponse(status=200,all_function=initparam)

def merge_message(param:ChatCompletionRequest):
    if isinstance(param.message,str):
        return "user:"+param.message
    history=[]
    if isinstance(param.message,list):
        for chatMessage in param.message:
            history.append(f"{chatMessage.role}:{chatMessage.content}")
    history="\n".join(history)

    return history


@app.post("/chat_intention/completions", response_model=ChatCompletionResponse)
async def init(request: ChatCompletionRequest):
    global  agent_exec
    query=merge_message(request)
    fun_id,message=agent_exec.run(query)
    return ChatCompletionResponse(status=200,funtion_id=fun_id,message=message)


@app.post("/funtion/completions", response_model=ChatCompletionResponse)
async def init(request: FunCompletionRequest):
    global  toos_dict
    tool=toos_dict[request.funtion_id]
    query=merge_message(request.message)
    message=tool._run(query)
    return ChatCompletionResponse(status=200,funtion_id=request.funtion_id,message=message)


def init_run():
    global  agent_exec,toos_dict,llm,initparam
    llm = myOpenAi(temperature=0.8)
    initparam = load_interface_template(saveinterfacepath)
    toos_dict = {}
    for param in initparam.params  :
        if param.usableFlag:
            toos_dict[param.id]=Model_Tool(name=param.name,description=param.functionDesc,id=param.id,llm=llm)
    tools=list(toos_dict.values())
    unknowntool=Unknown_Intention_Model_Tool(llm=llm)
    tools.append(unknowntool)
    # # 选择工具
    agent = IntentAgent(tools=tools, llm=llm,default_intent_name=Unknown_Intention_Model_Tool.name)
    agent_exec = AgentExecutor.from_agent_and_tools(agent=agent,  tools=tools, verbose=False,max_iterations=1)
    return agent_exec,toos_dict,llm,initparam

if __name__ == "__main__":

    agent_exec,toos_dict,llm,initparam=None,None,None,None
    init_run()

    # initparam=load_interface_template(saveinterfacepath)
    #
    #
    # prompt_dict=init_all_fun_prompt(initparam)
    #
    #
    # toos_dict={}
    # for param in initparam.params  :
    #     if param.usableFlag:
    #         toos_dict[param.id]=Model_Tool(name=param.name,description=param.functionDesc,id=param.id,llm=llm)
    #
    # # order=Order_select_Tool(llm=llm)
    # # res=order._run("查询订单123456")
    # tools=list(toos_dict.values())
    # # # 选择工具
    # agent = IntentAgent(tools=tools, llm=llm,default_intent_name=Unknown_Intention_Model_Tool.name)
    # agent_exec = AgentExecutor.from_agent_and_tools(agent=agent,  tools=tools, verbose=False,max_iterations=1)
    # res=agent_exec.run(A)


    uvicorn.run(app, host='0.0.0.0', port=8081, workers=1)




""":param
import requests
import json 

post_json = json.dumps({"params":[{"name":"test","id":"999","functionDesc":"接口描述","usableFlag":1,"inputParams":[{"name":"name","type":"type","required":1,"title":"test_info"}]}]})


r1 = requests.post("http://127.0.0.1:8081/init", data=post_json)
print(r1.content.decode("utf8"))

"""