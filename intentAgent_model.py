from typing import List, Tuple, Any, Union,Optional
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import BaseSingleActionAgent
from langchain import LLMChain, PromptTemplate
from langchain.base_language import BaseLanguageModel
from langchain.memory import ConversationBufferMemory
from langchain.agents.conversational_chat.base import ConversationalChatAgent
from utils import  parse_json_markdown

from typing import List, Tuple, Any, Union, Optional
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import BaseSingleActionAgent
from langchain import LLMChain, PromptTemplate
from langchain.base_language import BaseLanguageModel
from prompt_helper import INTENT_FORMAT_INSTRUCTIONS
from langchain.agents.conversational_chat.base import ConversationalChatAgent

class IntentAgent(BaseSingleActionAgent):
    tools: List
    llm: BaseLanguageModel

    prompt = PromptTemplate.from_template(INTENT_FORMAT_INSTRUCTIONS)
    llm_chain: LLMChain = None
    default_intent_name:str
    def get_llm_chain(self):
        if not self.llm_chain:
            self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)

    # 根据提示(prompt)选择工具
    def choose_tools(self, query) -> List[str]:
        self.get_llm_chain()
        tool_names = [tool.name for tool in self.tools]
        summary=[]
        for i,tool in enumerate(self.tools):
            summary.append(f"{i}.{tool.name}:{tool.description}")
        summary="\n".join(summary)
        i=0
        while True:
            i+=1
            resp = self.llm_chain.predict(intents=tool_names, intention_summary=summary, user_input=query)
            try:
                resp=parse_json_markdown(resp)
                break
            except :
                pass
            ###三次试错找不到意图强制返回
            if i>=3:
                return [self.default_intent_name]
                break
        return [resp["intention_name"]]

    @property
    def input_keys(self):
        return ["input"]

    # 通过 AgentAction 调用选择的工具，工具的输入是 "input"
    def plan(
            self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        tool_name = self.choose_tools(kwargs["input"])[0]
        return AgentAction(tool=tool_name, tool_input=kwargs["input"], log="")

    async def aplan(
            self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[List[AgentAction], AgentFinish]:
        raise NotImplementedError("IntentAgent does not support async")