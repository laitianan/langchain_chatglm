
import time

import uvicorn
from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from watchdog.observers import Observer

from global_config import ChatConfig
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
from MyOpenAI import myOpenAi, call_qwen
from prompt_helper import init_all_fun_prompt
from utils import load_interface_template,save_interface_template
import time
import logging

from watch import FileEventHandler

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
DeleteResponse,
TemplateResponse,
Intention_Search_Response,
Funtion

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
        content={"status": 402,"message":f"{exc.name}"},
    )


def raise_UnicornException(func):  # 定义一个名为 raise_UnicornException 的装饰器函数，它接受一个参数 func这个 func 就是即将要被修饰的函数
    @wraps(func)
    async def wrapper(*args, **kwargs):  # 在 raise_UnicornException() 函数内部，定义一个名为 wrapper() 的闭包函数
        try:
            start_time = time.time()  # 程序开始时间
            logging.info(f"接口：{func.__name__}，前端参数为：{args} {kwargs}")
            res = await func(*args, **kwargs)
            end_time = time.time()  # 程序结束时间
            run_time = end_time - start_time  # 程序的运行时间，单位为秒
            logging.info(f"接口：{func.__name__}，运行时间：{run_time}，返回值：{res}")
        except  Exception as e:
            info=str(e)
            logging.info(f"接口：{func.__name__}，接口异常错误提示：{info}")
            raise  UnicornException(name=info)
        return res

    return wrapper


@app.post("/chat/completions", response_model=ChatResponse)
@raise_UnicornException
async def chat(request: ChatCompletionRequest):
    # llm=openai_model()
    # resp=llm.predict(request.message)
    response=call_qwen(request.message)
    resp=response.choices[0].message.content

    return ChatResponse(status=200,message=resp)


# @app.post("/delete_all_funtion_template/completions", response_model=DeleteResponse)
# @raise_UnicornException
async def del_temp():
    global  chatconfig
    path = os.path.join(saveinterfacepath, "interface_template.pkl")
    if os.path.exists(path):
        os.remove(path)
    chatconfig.init_run()
    return DeleteResponse(status=200,message="删除所有模板成功")

@app.post("/init_funtion_template/completions", response_model=InitInterfaceResponse)
@raise_UnicornException
async def init_funtion_template(request: InitInterfaceRequest):
    global chatconfig
    initparam = chatconfig.initparam
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
    chatconfig.init_run()
    res=InitInterfaceResponse(status=200,message="添加模板成功")
    return res


@app.post("/get_all_template/completions", response_model=TemplateResponse)
@raise_UnicornException
async  def get_all_template():
    initparam = load_interface_template(saveinterfacepath)
    return TemplateResponse(status=200,message="获取模板成功",template=initparam)



def merge_message(message):

    if isinstance(message,str):
        return "user:"+message
    history=[]
    if isinstance(message,list):
        for chatMessage in message:
            history.append(f"{chatMessage.role}:{chatMessage.content}")
    history="\n".join(history)
    logging.info(f"具体参数：{history}")
    return history


@app.post("/chat_funtion_intention/completions", response_model=ChatCompletionResponse)
@raise_UnicornException
async def chat_funtion_intention(request: FunCompletionRequest):
    global chatconfig
    agent_exec,toos_dict = chatconfig.agent_exec, chatconfig.toos_dict

    if request.funtion_id is None or request.funtion_id=='':
        query=merge_message(request.message)
        fun_id,message=agent_exec.run(query)
        fun_id=fun_id or ""
        return ChatCompletionResponse(status=200,funtion_id=fun_id,message=message)
    else:
        tool = toos_dict[request.funtion_id]
        query = merge_message(request.message)
        _, message = tool._run(query)
        return ChatCompletionResponse(status=200, funtion_id=request.funtion_id, message=message)


# ,
# Funtion
import asyncio


# async def f(request: FunCompletionRequest):
#     global search, agent_exec
#     mess=merge_message(request.message)
#     query=request.message[-1].content
#     docs, infos = await asyncio.gather(search.cal_similarity_rank(query), agent_exec.choose_tools(mess))


@app.post("/chat_intention_search/completions", response_model=Intention_Search_Response)
@raise_UnicornException
async def chat_intention_search(request: ChatCompletionRequest):
    global  chatconfig

    search, agent_exec=chatconfig.search,chatconfig.agent_exec
    mess=merge_message(request.message)
    query=request.message[-1].content
    # docs1=await search.cal_similarity_rank(query)
    # docs2=await agent_exec.agent.choose_tools(mess)
    docs1, docs2 = await asyncio.gather(search.cal_similarity_rank(query), agent_exec.agent.choose_tools(mess))
    d2=[]
    for e in docs1:
        if e not in docs2:
            d2.append(e)
    docs2.extend(d2)
    funtions=[Funtion(id=doc.funtion_id,name=doc.name,fro=doc.fro) for doc in docs2]


    return Intention_Search_Response(status=200,funtions=funtions)

chatconfig=ChatConfig()
agent_exec,toos_dict,llm,initparam,search=chatconfig.get_init()

if __name__ == "__main__":

    # agent_exec,toos_dict,llm,initparam,search=None,None,None,None,None
    # init_run()

    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, chatconfig.saveinterfacepath, recursive=True)
    observer.start()
    uvicorn.run("chat_api:app", host='0.0.0.0', port=8084, workers=2)




""":param
import requests
import json 

post_json = json.dumps({"params":[{"name":"test","id":"999","functionDesc":"接口描述","usableFlag":1,"inputParams":[{"name":"name","type":"type","required":1,"title":"test_info"}]}]})


r1 = requests.post("http://127.0.0.1:8081/init", data=post_json)
print(r1.content.decode("utf8"))

"""