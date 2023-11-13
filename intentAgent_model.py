from typing import List, Tuple, Any, Union,Optional
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import BaseSingleActionAgent
from langchain import LLMChain, PromptTemplate
from langchain.base_language import BaseLanguageModel
from langchain.memory import ConversationBufferMemory
from langchain.agents.conversational_chat.base import ConversationalChatAgent
from utils import  parse_json_markdown,parse_json_markdown_for_list
import  logging
from typing import List, Tuple, Any, Union, Optional
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import BaseSingleActionAgent
from langchain import LLMChain, PromptTemplate
from langchain.base_language import BaseLanguageModel
from prompt_helper import INTENT_FORMAT_INSTRUCTIONS,INTENT_FORMAT_MULTI_INSTRUCTIONS
from langchain.agents.conversational_chat.base import ConversationalChatAgent
from search_intention import  Doc
class IntentAgent(BaseSingleActionAgent):
    tools: List
    llm: BaseLanguageModel

    prompt1 = PromptTemplate.from_template(INTENT_FORMAT_INSTRUCTIONS)
    prompt2 = PromptTemplate.from_template(INTENT_FORMAT_MULTI_INSTRUCTIONS)

    llm_chain1: LLMChain = None
    llm_chain2: LLMChain = None
    default_intent_name:str
    summary:str=None
    tool_names=[]
    name_id_map={}
    def get_llm_chain(self,single=True):
        if single:
            if not self.llm_chain1:
                self.llm_chain1 = LLMChain(llm=self.llm, prompt=self.prompt1)
        else:
            if not self.llm_chain2:
                self.llm_chain2 = LLMChain(llm=self.llm, prompt=self.prompt2)

    def merge_summary(self):
        if self.summary==None:
            self.tool_names = [tool.name for tool in self.tools]
            self.name_id_map={tool.name:tool.id for tool in self.tools}
            summary = []
            for i, tool in enumerate(self.tools):
                summary.append(f"{i + 1}、{tool.name}:{tool.description}")
            summary = "\n".join(summary)
            self.summary=summary

    # 根据提示(prompt)选择工具
    def choose_tool(self, query) -> List[str]:
        self.get_llm_chain()
        self.merge_summary()
        res=[]
        resp = self.llm_chain1.predict(intents=self.tool_names, intention_summary=self.summary, user_input=query)
        for name in self.tool_names:
            if name in resp:
                res.append(name)
                break
        res.append(self.default_intent_name)
        return res

    async def choose_tools(self, query) -> List[Doc]:
        self.get_llm_chain(False)
        self.merge_summary()
        resp = self.llm_chain2.predict(intents=self.tool_names, intention_summary=self.summary, user_input=query)
        # logging.info(f"解析前：{resp}-------------------------------------------------")
        resp=parse_json_markdown_for_list(resp)
        # logging.info(f"解析后：{resp}-------------------------------------------------")
        docs=set()
        for i,name in enumerate(resp) :
            if name !=self.default_intent_name:
                docs.add(Doc(self.name_id_map[name],name,100.0-i-1,"AI"))

        return list(docs)

    @property
    def input_keys(self):
        return ["input"]

    # 通过 AgentAction 调用选择的工具，工具的输入是 "input"
    def plan(
            self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        tools=self.choose_tool(kwargs["input"])
        tool_name = tools[0]
        return AgentAction(tool=tool_name, tool_input=kwargs["input"], log="")

    async def aplan(
            self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[List[AgentAction], AgentFinish]:
        raise NotImplementedError("IntentAgent does not support async")