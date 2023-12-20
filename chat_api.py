
import time
import asyncio
from logging.handlers import RotatingFileHandler
# from shared import SharedObject
from config import api_base, saveinterfacepath
import uvicorn
from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functools import wraps
from langchain.agents import AgentExecutor

from bm25 import BM25
from doc import Doc
from intentAgent_model import IntentAgent
from redis_manger import get_version, set_version
from tool_model import Model_Tool, Unknown_Intention_Model_Tool
from MyOpenAI import myOpenAi, call_qwen_funtion
from prompt_helper import init_all_fun_prompt, FUNTION_CALLING_FORMAT_INSTRUCTIONS
from utils import load_interface_template, save_interface_template, is_true_number, is_xxCH
import time
from fastapi import  Request
from fastapi.responses import JSONResponse
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
from api_protocol import (
    InitInterfaceResponse,
    InitInterfaceRequest,
    ChatCompletionRequest,
    ChatCompletionResponse,
    FunCompletionRequest,
    ChatResponse,
    DeleteResponse,
    TemplateResponse,
    Intention_Search_Response,
    Funtion, Beautify_ChatCompletionRequest, ChatMessage, Chat_LinksResponse, LinksResp

)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):

    return JSONResponse(
        status_code=408,
        content={"status": 402,"message":f"{exc.name}"},
    )

def init_run():
    global  agent_exec,toos_dict,llm,initparam,search
    initparam = load_interface_template(saveinterfacepath)
    if not initparam:
        return  None,None,None,None,None
    llm = myOpenAi()
    toos_dict = {}
    docs=[]
    prompt_dict=init_all_fun_prompt(initparam)
    for param in initparam.params  :
        if param.usableFlag:
            sub_param_type={e.name:e.type for e in param.inputParams}
            toos_dict[param.id]=Model_Tool(name=param.name,description=param.functionDesc,id=param.id,llm=llm,prompt_dict=prompt_dict,sub_param_type=sub_param_type)
            docs.append(Doc(funtion_id=param.id, name=param.name))
    # search = Query_Search(docs)
    if len(docs)==0:
        search=None
        agent_exec=None
        toos_dict=None
    else:
        search =BM25(docs)
        tools=list(toos_dict.values())
        unknowntool=Unknown_Intention_Model_Tool(llm=llm)
        tools.append(unknowntool)
        # # 选择工具
        agent = IntentAgent(tools=tools, llm=llm,default_intent_name=unknowntool.name)
        agent_exec = AgentExecutor.from_agent_and_tools(agent=agent,  tools=tools, verbose=False,max_iterations=1)
    return agent_exec,toos_dict,llm,initparam,search

agent_exec,toos_dict,llm,initparam,search=init_run()
current_version=get_version()

def raise_UnicornException(func):  # 定义一个名为 raise_UnicornException 的装饰器函数，它接受一个参数 func这个 func 就是即将要被修饰的函数

    @wraps(func)
    async def wrapper( *args, **kwargs):  # 在 raise_UnicornException() 函数内部，定义一个名为 wrapper() 的闭包函数
        global agent_exec, toos_dict, llm, initparam, search, current_version
        try:
            version=get_version()
            if current_version != version:
                agent_exec, toos_dict, llm, initparam, search = init_run()
                current_version=version
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




@app.post("/chat/completions", response_model=ChatResponse)
@raise_UnicornException
async def chat(request: ChatCompletionRequest):
    response=call_qwen_funtion(request.message)
    resp=response.choices[0].message.content
    return ChatResponse(status=200,message=resp)


@app.post("/beautify_chat/completions", response_model=ChatResponse)
@raise_UnicornException
async def beautify_chat(request: Beautify_ChatCompletionRequest):
    global  toos_dict,llm
    funname_resp = request.funname_resp

    query="\n".join([f"{i+1}.查询：{toos_dict[res.funtion_id].description},查询结果如下:{res.resp}" for i,res in enumerate(funname_resp)])
    userinput=merge_message(request.message)
    content = FUNTION_CALLING_FORMAT_INSTRUCTIONS.format(content=query, userinput=userinput)
    mess = request.message
    # if mess[0].role == "system":
    #     mess.pop(0)
    # mess.insert(0, ChatMessage(role="system", content="仅仅回答用户咨询与幸福西饼有关的问题"))
    mess.append(ChatMessage(role="user",content=content))
    response = call_qwen_funtion(mess, top_p=0)
    resp = response.choices[0].message.content
    i=1
    n=3
    while i<=n:
        i+=1
        if is_true_number(resp,query)  and not is_xxCH(resp,query) and (len(resp)<=len(content.replace(" ",""))*2 or len(resp)<=len("未查到信息，请尝试咨询其他业务")*2):
            break
        else:
            response = call_qwen_funtion(mess,top_p=0.8)
            resp = response.choices[0].message.content
    if i>n:
        resp="很抱歉，我无法提供您需要的信息。请咨询客服以获取更多帮助"
    logging.info(f"<chat>\n\nquery:\t{content}\n<!-- *** -->\nresponse:\n{resp}\n\n</chat>")
    return ChatResponse(status=200, message=resp)



@app.post("/init_funtion_template/completions", response_model=InitInterfaceResponse)
@raise_UnicornException
async def init_funtion_template(request: InitInterfaceRequest):
    global  initparam,current_version
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
    set_version()
    current_version=get_version()
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

@app.post("/chat_multi_intention/completions", response_model=Chat_LinksResponse)
@raise_UnicornException
async def chat_multi_intention(request: FunCompletionRequest):
    global  agent_exec,toos_dict

    mess = merge_message(request.message)
    docs = await agent_exec.agent.choose_tools(mess)
    tools=[]
    for doc in docs:
        tool = toos_dict[doc.funtion_id]
        id_, message = tool._run(mess)
        tools.append(LinksResp(funtion_id=doc.funtion_id,name=doc.name,message=message))
    return Chat_LinksResponse(status=200, tool=tools)



@app.post("/chat_intention_search/completions", response_model=Intention_Search_Response)
@raise_UnicornException
async def chat_intention_search(request: ChatCompletionRequest):
    global  search,agent_exec

    mess=merge_message(request.message)
    query=request.message[-1].content
    docs1, docs2 = await asyncio.gather(search.cal_similarity_rank(query), agent_exec.agent.choose_tools(mess))
    if len(docs2)!=0 and len(query.replace(" ",""))>4 :
        # docs1=[]
        pass
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




if __name__ == "__main__":


    uvicorn.run("chat_api:app", host='0.0.0.0', port=8084, workers=1)



