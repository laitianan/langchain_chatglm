from funtion_basetool import  functional_Tool
from langchain.base_language import BaseLanguageModel
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import BaseSingleActionAgent
from langchain import LLMChain, PromptTemplate
from utils import  parse_json_markdown
import json
from typing import Any, Dict, List, Literal, Optional, Union
import datetime
import logging
class Model_Tool(functional_Tool):
    llm: BaseLanguageModel

    llm_chain: LLMChain = None
    name:str
    description:str
    id:str
    prompt_dict:dict
    prompt:Optional[Any]
    def _call_func(self, query):
        id=self.id
        self.prompt = self.prompt_dict[id]
        self.get_llm_chain()
        i=0
        current_time = datetime.datetime.now()
        current_time=str(current_time)[:19]
        while True:
            i+=1
            resp = self.llm_chain.predict(user_input=query,current_time=current_time)
            try:
                if resp.find('None\n')!=-1:
                    resp = resp.replace('None\n', '"None"\n')
                resp=parse_json_markdown(resp)
                break
            except :
                pass
            ###三次试错找不到意图强制返回
            if i>=3:
                return self.id,""

        return self.id,json.dumps(resp,ensure_ascii=False)

    def get_llm_chain(self):
        if not self.llm_chain:
            self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)


class Unknown_Intention_Model_Tool(functional_Tool):
    llm: BaseLanguageModel
    id: str="000000"
    llm_chain: LLMChain = None
    name:str="意图不明"
    description:str="用户随便询问的内容,当其他意图不匹配时请选择该意图"

    def _call_func(self, query):
        if query.count("user"):
            query=f"system:当前你是幸福西饼AI客服助手，请你尽量使用中文回答用户的问题\n{query}"
        else:
            query = f"system:当前你是幸福西饼AI客服助手，请你尽量使用中文回答用户的问题\nuser:{query}"
        resp = self.llm.predict(query)
        return "",resp

    def get_llm_chain(self):
        pass



