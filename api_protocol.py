from typing import Any, Dict, List, Literal, Union, Optional
from pydantic import BaseModel, Field
class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system","function"]
    content: str


class DeltaMessage(BaseModel):
    role: Optional[Literal["user", "assistant", "system","function"]] = None
    api_id:str
    content: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_length: Optional[int] = None

class ChatCompletionResponse(BaseModel):
    api_id:str
    message: ChatMessage

class Param(BaseModel):
    name:str
    type:str
    required:bool
    title: str

class Interface(BaseModel):
    name:str
    id:str
    functionDesc: str
    businessTypeNames:Optional[str]=None
    businessSonTypeNames: Optional[str] = None
    usableFlag:Literal[True, False]
    inputParams:List[Param]

class InitInterfaceRequest(BaseModel):
    params:List[Interface]

class InitInterfaceResponse(BaseModel):
    status:int
    message:Optional[str]
    # all_function:Optional[InitInterfaceRequest]

class TemplateResponse(BaseModel):
    status:int
    message:Optional[str]
    template:Optional[InitInterfaceRequest]

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system","function"]
    content: str


class ChatCompletionRequest(BaseModel):
    message:List[ChatMessage]

class FuntionResp(BaseModel):
    name:str
    resp:str
class Beautify_ChatCompletionRequest(BaseModel):
    funname_resp:List[FuntionResp]
    message: List[ChatMessage]

class FunCompletionRequest(BaseModel):
    funtion_id:Optional[str]= ""
    message:Union[List[ChatMessage],str]

class ChatCompletionResponse(BaseModel):
    status: int
    funtion_id:Optional[str]=""
    role: Optional[str]="assistant"
    message: str

class LinksResp(BaseModel):
    funtion_id:Optional[str]=""
    name:str
    role: Optional[str]="assistant"
    message: str

class Chat_LinksResponse(BaseModel):
    status: int
    tool:List[LinksResp]


class Funtion(BaseModel):
    id:str
    name:str
    fro:str

class Intention_Search_Response(BaseModel):
    status: int
    funtions: List[Funtion]

class ChatResponse(BaseModel):
    status: int
    role: Optional[str]="assistant"
    message: str

class DeleteResponse(BaseModel):
    status: int
    message: str


