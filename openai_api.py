# coding=utf-8
# Implements API for ChatGLM2-6B in OpenAI's format. (https://platform.openai.com/docs/api-reference/chat)
# Usage: python openai_api.py
# Visit http://localhost:8000/docs for documents.


import time
import torch
import uvicorn
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Literal, Optional, Union
from transformers import AutoTokenizer, AutoModel
from sse_starlette.sse import ServerSentEvent, EventSourceResponse
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
fh = logging.FileHandler(filename='./openai_server.log')
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)  # 将日志输出至屏幕
logger.addHandler(fh)  # 将日志输出至文件

from fastapi import  Request
from fastapi.responses import JSONResponse
from functools import wraps

@asynccontextmanager
async def lifespan(app: FastAPI): # collects GPU memory
    yield
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


app = FastAPI(lifespan=lifespan)

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
        content={"status": f"Oops! {exc.name} "},
    )


def raise_UnicornException(func):  # 定义一个名为 raise_UnicornException 的装饰器函数，它接受一个参数 func这个 func 就是即将要被修饰的函数
    @wraps(func)
    async def wrapper(*args, **kwargs):  # 在 raise_UnicornException() 函数内部，定义一个名为 wrapper() 的闭包函数
        try:
            logging.info(f"接口：{func.__name__}，前端参数为：{args} {kwargs}")
            res = await func(*args, **kwargs)
            logging.info(f"返回值：{res}")
        except  Exception as e:
            info=str(e)
            raise  UnicornException(name=info)
        return res

    return wrapper


class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = "owner"
    root: Optional[str] = None
    parent: Optional[str] = None
    permission: Optional[list] = None


class ModelList(BaseModel):
    object: str = "list"
    data: List[ModelCard] = []


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class DeltaMessage(BaseModel):
    role: Optional[Literal["user", "assistant", "system"]] = None
    content: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = None
    max_tokens: Optional[int] = 500
    stream: Optional[bool] = False

class EmbeddingsRequest(BaseModel):
    model: Optional[str] = None
    engine: Optional[str] = None
    input: Union[str, List[Any]]
    user: Optional[str] = None
    encoding_format: Optional[str] = None

class UsageInfo(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0
    completion_tokens: Optional[int] = 0

class EmbeddingsResponse(BaseModel):
    object: str = "list"
    data: List[Dict[str, Any]]
    model: str
    usage: UsageInfo

class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Literal["stop", "length"]


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length"]]


class ChatCompletionResponse(BaseModel):
    model: str
    object: Literal["chat.completion", "chat.completion.chunk"]
    choices: List[Union[ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice]]
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))


@app.get("/v1/models", response_model=ModelList)
@raise_UnicornException
async def list_models():
    global model_args
    model_card = ModelCard(id="gpt-3.5-turbo")
    return ModelList(data=[model_card])


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
@raise_UnicornException
async def create_chat_completion(request: ChatCompletionRequest):
    global model, tokenizer
    if request.messages[-1].role != "user":
        raise HTTPException(status_code=400, detail="Invalid request")
    query = request.messages[-1].content
    # logging.info(str(request.messages))
    # print("/v1/chat/completions 参数接受值:\t"+str(request.messages))
    prev_messages = request.messages[:-1]
    if len(prev_messages) > 0 and prev_messages[0].role == "system":
        query = prev_messages.pop(0).content + query

    history = []
    if len(prev_messages) % 2 == 0:
        for i in range(0, len(prev_messages), 2):
            if prev_messages[i].role == "user" and prev_messages[i+1].role == "assistant":
                history.append([prev_messages[i].content, prev_messages[i+1].content])

    if request.stream:
        generate = predict(query, history, request)
        return EventSourceResponse(generate, media_type="text/event-stream")

    # response, _ = model.chat(tokenizer, query, history=history)
    response, _ = model.chat(tokenizer, query, history=history, temperature=request.temperature,max_new_tokens=request.max_tokens)

    # logging.info("info后台返回值："+str(response))
    # print("print后台返回值："+str(response))
    choice_data = ChatCompletionResponseChoice(
        index=0,
        message=ChatMessage(role="assistant", content=response),
        finish_reason="stop"
    )

    return ChatCompletionResponse(model=request.model, choices=[choice_data], object="chat.completion")


async def predict(query: str, history: List[List[str]], request: ChatCompletionRequest):
    global model, tokenizer
    # logging.info(str(query))
    # print(str(query))
    choice_data = ChatCompletionResponseStreamChoice(
        index=0,
        delta=DeltaMessage(role="assistant"),
        finish_reason=None
    )
    chunk = ChatCompletionResponse(model=request.model, choices=[choice_data], object="chat.completion.chunk")
    yield "{}".format(chunk.json(exclude_unset=True, ensure_ascii=False))

    current_length = 0
    #,repetition_penalty=1.1,do_sample=True,top_p=0.8
    for new_response, _ in model.stream_chat(tokenizer, query, history=history,temperature=request.temperature,max_new_tokens=request.max_tokens):
    # for new_response, _ in model.stream_chat(tokenizer, query, history=history):
        if len(new_response) == current_length:
            continue

        new_text = new_response[current_length:]
        current_length = len(new_response)

        choice_data = ChatCompletionResponseStreamChoice(
            index=0,
            delta=DeltaMessage(content=new_text),
            finish_reason=None
        )
        chunk = ChatCompletionResponse(model=request.model, choices=[choice_data], object="chat.completion.chunk")
        yield "{}".format(chunk.json(exclude_unset=True, ensure_ascii=False))


    choice_data = ChatCompletionResponseStreamChoice(
        index=0,
        delta=DeltaMessage(),
        finish_reason="stop"
    )
    chunk = ChatCompletionResponse(model=request.model, choices=[choice_data], object="chat.completion.chunk")
    yield "{}".format(chunk.json(exclude_unset=True, ensure_ascii=False))
    yield '[DONE]'
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
def process_input(model_name, inp):
    if model_name=="OpenAIEmbeddings":
        inps=[]
        for token in inp:
            inps.append(enc.decode(token))
        return inps
    if isinstance(inp, str):
        inps = [inp]
    return inps

# @app.post("/v1/embeddings", response_model=EmbeddingsResponse)
@app.post("/v1/embeddings", response_model_exclude_none=True)
@raise_UnicornException
async def create_embeddings(request: EmbeddingsRequest, model_name: str = "text2vec-large-chinese"):
    global  t2v_model
    """Creates embeddings for the text"""
    if request.model is None:
        request.model = model_name
    print("request.input\t"+str(request.input))
    request.input = process_input(request.model, request.input)

    data = []
    token_num = 0
    batch_size = 3
    batches = [
        request.input[i : min(i + batch_size, len(request.input))]
        for i in range(0, len(request.input), batch_size)
    ]
    for num_batch, batch in enumerate(batches):
        # payload = {
        #     "model": request.model,
        #     "input": batch,
        #     "encoding_format": request.encoding_format,
        # }
        print("batch")
        print(batch)
        embedding = t2v_model.encode(batch)
        tokennum=sum([len(e) for e in batch])
        data += [
            {
                "object": "embedding",
                "embedding": list(emb.astype(float)),
                "index": num_batch * batch_size + i,
            }
            for i, emb in enumerate(embedding)
        ]
        token_num += tokennum
    return EmbeddingsResponse(
        data=data,
        model=request.model,
        usage=UsageInfo(
            prompt_tokens=token_num,
            total_tokens=token_num,
            completion_tokens=None,
        ),
    ).dict(exclude_none=True)


def qwen():
    from transformers import AutoTokenizer, AutoModelForCausalLM
    print("qwen loading")
    path="/data/laitianan/qwen-14b-4bit"
    # Note: The default behavior now has injection attack prevention off.
    tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        path,
        device_map="auto",
        trust_remote_code=True
    ).eval()

    return tokenizer,model
def internlm7b():
    print("internlm loading")
    path="/data/laitianan/internlm-chat-7b"
    tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
    model = AutoModel.from_pretrained(path, trust_remote_code=True,torch_dtype=torch.float16).cuda()
    return tokenizer, model

if __name__ == "__main__":
    tokenizer,model=qwen()
    from text2vec import SentenceModel
    t2v_model = SentenceModel("/data/laitianan/Langchain-Chatchat-master/text2vec-large-chinese")
    uvicorn.run(app, host='0.0.0.0', port=8081, workers=1)
