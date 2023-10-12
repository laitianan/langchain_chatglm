from MyOpenAI import myOpenAi as  OpenAI

import re
from typing import List, Union
import textwrap
import time

from langchain.agents import (
    Tool,
    AgentExecutor,
    LLMSingleActionAgent,
    AgentOutputParser,
)
from langchain.prompts import StringPromptTemplate
from langchain import  LLMChain
from langchain.schema import AgentAction, AgentFinish
from langchain.prompts import PromptTemplate

from langchain.llms.base import BaseLLM

human_message = """TOOLS
------
Assistant can ask the user to use tools to look up information that may be helpful in answering the users original question. The tools the human can use are:
{{tool_names}}
{{tools}}

{format_instructions}

USER'S INPUT
--------------------
Here is the user's input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else):

{{{{input}}}}"""

format_instructions = human_message.format(
    format_instructions="nidfhaofdhao"
)
tool_names=["12456","457896"]
tool_strings="dfdfdfdf"
final_prompt = format_instructions.format(
    tool_names=tool_names, tools=tool_strings,input="456678"
)
print(final_prompt.format(input="456678"))