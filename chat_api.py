
import time
import asyncio
from logging.handlers import RotatingFileHandler

import uvicorn
from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functools import wraps
from langchain.agents import AgentExecutor

from bm25 import BM25
from doc import Doc
from intentAgent_model import IntentAgent
from tool_model import Model_Tool, Unknown_Intention_Model_Tool
from MyOpenAI import myOpenAi, call_qwen_funtion
from prompt_helper import init_all_fun_prompt
from utils import load_interface_template,save_interface_template
import time
import logging
logger = logging.getLogger()

logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)
file_handler = RotatingFileHandler("./data/chat_api.log", 'a', 10*1024*1024, 360,encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

app = FastAPI()
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
            # logging.info(f"接口：{func.__name__}，前端参数为：{args} {kwargs}")
            res = await func(*args, **kwargs)
            end_time = time.time()  # 程序结束时间
            run_time = end_time - start_time  # 程序的运行时间，单位为秒
            logging.info(f"接口：{func.__name__},前端参数为：{args} {kwargs},运行时间：{run_time},返回值：{res}")
        except  Exception as e:
            info=str(e)
            logging.info(f"接口：{func.__name__}，接口异常错误提示：{info}")
            raise  UnicornException(name=info)
        return res

    return wrapper



from config import api_base, saveinterfacepath

@app.post("/chat/completions", response_model=ChatResponse)
@raise_UnicornException
async def chat(request: ChatCompletionRequest):
    response=call_qwen_funtion(request.message)
    resp=response.choices[0].message.content
    return ChatResponse(status=200,message=resp)


@app.post("/init_funtion_template/completions", response_model=InitInterfaceResponse)
@raise_UnicornException
async def init_funtion_template(request: InitInterfaceRequest):
    global  initparam
    if initparam  :
        interface_fun = {param.id:param for param in initparam.params}
        for param in request.params:
            interface_fun[param.id] = param
            if not param.usableFlag:
                del interface_fun[param.id]
        initparam.params=list(interface_fun.values())
    else:
        initparam=request
    save_interface_template(initparam, saveinterfacepath)
    init_run()
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
    # logging.info(f"具体参数：{history}")
    return history


@app.post("/chat_funtion_intention/completions", response_model=ChatCompletionResponse)
@raise_UnicornException
async def chat_funtion_intention(request: FunCompletionRequest):
    global  agent_exec,toos_dict
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



@app.post("/chat_intention_search/completions", response_model=Intention_Search_Response)
@raise_UnicornException
async def chat_intention_search(request: ChatCompletionRequest):
    global  search,agent_exec

    mess=merge_message(request.message)
    query=request.message[-1].content
    docs1, docs2 = await asyncio.gather(search.cal_similarity_rank(query), agent_exec.agent.choose_tools(mess))
    docs1, docs2=set(docs1),set(docs2)
    d=docs2.intersection(docs1)

    docs2=docs2-d
    docs1=docs1-d
    d=list(d)
    for e in d:
        e.fro="AI"
    docs=list(d)+list(docs2)+list(docs1)
    funtions=[Funtion(id=doc.funtion_id,name=doc.name,fro=doc.fro) for doc in docs]
    return Intention_Search_Response(status=200,funtions=funtions)


def init_run():
    global  agent_exec,toos_dict,llm,initparam,search

    initparam = load_interface_template(saveinterfacepath)
    if not initparam:
        return


    llm = myOpenAi(temperature=0.8,max_tokens=2000)
    toos_dict = {}
    docs=[]
    prompt_dict=init_all_fun_prompt(initparam)
    for param in initparam.params  :
        if param.usableFlag:
            sub_param_type={e.name:e.type for e in param.inputParams}
            toos_dict[param.id]=Model_Tool(name=param.name,description=param.functionDesc,id=param.id,llm=llm,prompt_dict=prompt_dict,sub_param_type=sub_param_type)
            docs.append(Doc(funtion_id=param.id, name=param.name))
    # search = Query_Search(docs)
    search =BM25(docs)

    tools=list(toos_dict.values())
    unknowntool=Unknown_Intention_Model_Tool(llm=llm)
    tools.append(unknowntool)
    # # 选择工具
    agent = IntentAgent(tools=tools, llm=llm,default_intent_name=unknowntool.name)
    agent_exec = AgentExecutor.from_agent_and_tools(agent=agent,  tools=tools, verbose=False,max_iterations=1)
    return agent_exec,toos_dict,llm,initparam,search

agent_exec,toos_dict,llm,initparam,search=init_run()

if __name__ == "__main__":


    uvicorn.run("chat_api:app", host='0.0.0.0', port=8084, workers=1)



