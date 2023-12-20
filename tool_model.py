from funtion_basetool import  functional_Tool
from langchain.base_language import BaseLanguageModel
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import BaseSingleActionAgent
from langchain import LLMChain, PromptTemplate
from utils import parse_json_markdown, get_current_weekday, validate_date_string, get_num, is_xxCH
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
    sub_param_type:dict
    def _call_func(self, query):

        sub_param={k:None for k,v in self.sub_param_type.items()}
        id=self.id

        if len(sub_param)<=0 or len(query)<=7:
            return self.id,json.dumps(sub_param, ensure_ascii=False)

        self.prompt = self.prompt_dict[id]
        current_time = datetime.datetime.now()
        current_time=str(current_time)[:19]+","+get_current_weekday()
        current_date=current_time[:10]
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        before_yesterday=today - datetime.timedelta(days=2)
        user_input=self.prompt.format(user_input=query,current_time=current_time,current_date=current_date,yesterday=yesterday.__str__(),before_yesterday=before_yesterday.__str__())
        i = 0
        n=3
        while True:
            resp_p = self.llm.predict(user_input)
            resp=resp_p
            logging.info(f"<chat>\n\nquery:\t{user_input}\n<!-- *** -->\nresponse:\n{resp}\n\n</chat>")
            try:
                resp=parse_json_markdown(resp)
                for k, v in resp.items():
                    if not v or k not in sub_param:
                        continue

                    v_=v.lower().strip()
                    if  "null" in v_  or "未知"  in v_ or is_xxCH(v_,query.lower().strip()) :
                        resp[k]=None
                for k,v in sub_param.items():
                    if k in resp and resp[k] is not None:
                        sub_param[k]=resp[k]
                    v= sub_param[k]
                    num=get_num(v)
                    if num!="" and num not in query:
                        sub_param[k]=None
                    if self.sub_param_type[k].lower()=="string" and isinstance(sub_param[k],list):
                        if len(sub_param[k])>0:
                            sub_param[k]=str(sub_param[k][0])
                s=sum([1 if e == None else 0 for e in sub_param.values()])
                if s/len(sub_param) >=0.5 and i<n :
                    i+=1
                    continue
                else:
                    break
            except :
                if i>=n:
                    break
                i += 1
        return self.id, json.dumps(sub_param, ensure_ascii=False)

    def get_llm_chain(self):
        if not self.llm_chain:
            self.llm_chain = LLMChain(llm=self.llm)


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


        # response = self.llm.predict(query)
        # logging.info(f"<chat>\n\nquery:\t{query}\n<!-- *** -->\nresponse:\n{response}\n\n</chat>")
        return "",""

    def get_llm_chain(self):
        pass



