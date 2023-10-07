# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 14:49:50 2023

@author: 98608
"""

from langchain import PromptTemplate
from ChatGLM2 import ChatGLM2
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain,RouterOutputParser
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
llm = ChatGLM2(temperature=0.9)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
print(conversation.prompt)
print(conversation.predict(input="我的姓名是tiger"))
print(conversation.predict(input="1+1=?"))
print(conversation.predict(input="我的姓名是什么"))

from langchain.agents import load_tools, initialize_agent, tool
from langchain.agents.agent_types import AgentType
from datetime import date

@tool
def time(text: str) -> str:
    """
    返回今天的日期。
    """
    return str(date.today())

@tool
def calc(text: str) -> str:
    """
    计算器。
    """
    return 88


tools = load_tools( ['llm-math'],llm=llm)
tools.append(time)
tools.append(calc)
agent_math = initialize_agent(agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                                   tools=tools,
                                   llm=llm,
                                   verbose=True)
print(agent_math("计算45 * 54"))
print(agent_math("今天是哪天？"))