from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field
class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class DeltaMessage(BaseModel):
    role: Optional[Literal["user", "assistant", "system"]] = None
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
    all_function:InitInterfaceRequest

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatCompletionRequest(BaseModel):
    message:Union[str, List[ChatMessage]]

class FunCompletionRequest(BaseModel):
    funtion_id:Optional[int,Any]
    message:Union[str, List[ChatMessage]]

class ChatCompletionResponse(BaseModel):
    status: int
    funtion_id:Optional[int,Any]
    role: Optional[str]="assistant"
    message: ChatMessage