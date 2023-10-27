from funtion_basetool import  functional_Tool
from langchain.base_language import BaseLanguageModel
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import BaseSingleActionAgent
from langchain import LLMChain, PromptTemplate
from utils import  parse_json_markdown
import json
class Model_Tool(functional_Tool):
    llm: BaseLanguageModel

    llm_chain: LLMChain = None
    name:str
    description:str
    id:str
    prompt_dict:dict

    def _call_func(self, query):
        self.prompt = self.prompt_dict[self.id]
        self.get_llm_chain()
        i=0
        while True:
            i+=1
            resp = self.llm_chain.predict(user_input=query)
            try:
                resp=parse_json_markdown(resp)
                break
            except :
                pass
            ###三次试错找不到意图强制返回
            if i>=3:
                return self.id,None

        return self.id,json.dumps(resp)

    def get_llm_chain(self):
        if not self.llm_chain:
            self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)


class Unknown_Intention_Model_Tool(functional_Tool):
    llm: BaseLanguageModel

    llm_chain: LLMChain = None
    name:str="意图不明"
    description:str="用户随便询问的内容,当其他意图不匹配时请选择该意图"

    def _call_func(self, query):
        resp = self.llm.predict(query)
        return None,resp

    def get_llm_chain(self):
        pass



