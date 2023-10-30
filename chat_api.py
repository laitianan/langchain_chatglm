
import time

import uvicorn
from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prompt_helper import  init_all_fun_prompt
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Literal, Optional, Union
import  logging
import pickle
import os
from functools import wraps
from langchain.agents import AgentExecutor
from intentAgent_model import IntentAgent
from tool_model import Model_Tool, Unknown_Intention_Model_Tool
from MyOpenAI import myOpenAi,openai_model
from prompt_helper import init_all_fun_prompt
from utils import load_interface_template,save_interface_template

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
fh = logging.FileHandler(filename='./server.log')
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)  # 将日志输出至屏幕
logger.addHandler(fh)  # 将日志输出至文件

app = FastAPI()
saveinterfacepath="./data/"
from api_protocol import  (
InitInterfaceResponse,
InitInterfaceRequest,
ChatCompletionRequest,
ChatCompletionResponse,
FunCompletionRequest,
ChatResponse,
DeleteResponse
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi import  Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):

    return JSONResponse(
        status_code=408,
        content={"status": f"Oops! {exc.name} "},
    )


def raise_UnicornException(func):  # 定义一个名为 raise_UnicornException 的装饰器函数，它接受一个参数 func这个 func 就是即将要被修饰的函数
    @wraps(func)
    async def wrapper(*args, **kwargs):  # 在 raise_UnicornException() 函数内部，定义一个名为 wrapper() 的闭包函数
        try:
            logging.info(f"接口：{func.__name__}，前端前期参数为：{args} {kwargs}")
            res = await func(*args, **kwargs)
            logging.info(f"返回值：{res}")
        except  Exception as e:
            info=str(e)
            raise  UnicornException(name=info)
        return res

    return wrapper


@app.post("/chat/completions", response_model=ChatResponse)
@raise_UnicornException
async def chat(request: ChatCompletionRequest):

    llm=openai_model()
    resp=llm.predict(request.message)
    return ChatResponse(status=200,message=resp)


@app.post("/delete_all_funtion_template/completions", response_model=DeleteResponse)
@raise_UnicornException
async def del_temp():
    path = os.path.join(saveinterfacepath, "interface_template.pkl")
    if os.path.exists(path):
        os.remove(path)
        
    return DeleteResponse(status=200,message="删除所有模板成功")

@app.post("/init_funtion_template/completions", response_model=InitInterfaceResponse)
@raise_UnicornException
async def init_funtion_template(request: InitInterfaceRequest):
    global  initparam
    print(initparam)
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
    init_run()
    res=InitInterfaceResponse(status=200,message="添加模板成功", all_function=initparam)
    return res


def merge_message(message):

    if isinstance(message,str):
        return "user:"+message
    history=[]
    if isinstance(message,list):
        for chatMessage in message:
            history.append(f"{chatMessage.role}:{chatMessage.content}")
    history="\n".join(history)

    return history


@app.post("/chat_funtion_intention/completions", response_model=ChatCompletionResponse)
@raise_UnicornException
async def chat_funtion_intention(request: ChatCompletionRequest):
    global  agent_exec

    query=merge_message(request.message)
    fun_id,message=agent_exec.run(query)
    return ChatCompletionResponse(status=200,funtion_id=fun_id,message=message)



@app.post("/chat_funtion/completions", response_model=ChatCompletionResponse)
@raise_UnicornException
async def chat_funtion(request: FunCompletionRequest):
    global  toos_dict

    tool=toos_dict[request.funtion_id]
    query=merge_message(request.message)
    _,message=tool._run(query)
    return ChatCompletionResponse(status=200,funtion_id=request.funtion_id,message=message)


def init_run():
    global  agent_exec,toos_dict,llm,initparam

    initparam = load_interface_template(saveinterfacepath)
    if not initparam:
        return
    llm = myOpenAi(temperature=0.8,max_tokens=2000)
    toos_dict = {}

    prompt_dict=init_all_fun_prompt(initparam)
    for param in initparam.params  :
        if param.usableFlag:
            toos_dict[param.id]=Model_Tool(name=param.name,description=param.functionDesc,id=param.id,llm=llm,prompt_dict=prompt_dict)
    tools=list(toos_dict.values())
    unknowntool=Unknown_Intention_Model_Tool(llm=llm)
    tools.append(unknowntool)
    # # 选择工具
    agent = IntentAgent(tools=tools, llm=llm,default_intent_name=unknowntool.name)
    agent_exec = AgentExecutor.from_agent_and_tools(agent=agent,  tools=tools, verbose=False,max_iterations=1)
    return agent_exec,toos_dict,llm,initparam

if __name__ == "__main__":

    agent_exec,toos_dict,llm,initparam=None,None,None,None
    init_run()
    uvicorn.run(app, host='0.0.0.0', port=8084, workers=1)




""":param
import requests
import json 

post_json = json.dumps({"params":[{"name":"test","id":"999","functionDesc":"接口描述","usableFlag":1,"inputParams":[{"name":"name","type":"type","required":1,"title":"test_info"}]}]})


r1 = requests.post("http://127.0.0.1:8081/init", data=post_json)
print(r1.content.decode("utf8"))

"""