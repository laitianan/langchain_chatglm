from langchain.tools import BaseTool, DuckDuckGoSearchRun
from typing import Dict, Union, Any, List

from langchain.output_parsers.json import parse_json_markdown
from langchain.agents.conversational_chat.prompt import FORMAT_INSTRUCTIONS
from langchain.agents import AgentExecutor, AgentOutputParser
from langchain.schema import AgentAction, AgentFinish
# 搜索工具
class SearchTool(BaseTool):
    name = "Search"
    description = "当问电影相关问题时候，使用这个工具"
    return_direct = True  # 直接返回结果

    def _run(self, query: str) -> str:
        print("\n正在调用搜索引擎执行查询: " + query)
        search = DuckDuckGoSearchRun()
        res=search.run(query)
        return res

# 计算工具
class CalculatorTool(BaseTool):
    name = "Calculator"
    description = "如果问数学相关问题时，使用这个工具"
    return_direct = True  # 直接返回结果

    def _run(self, query: str) -> str:
        return eval(query)




import re
# 自定义解析类
class CustomOutputParser(AgentOutputParser):

    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        print(text)
        cleaned_output = text.strip()
        # 定义匹配正则
        action_pattern = r'"action":\s*"([^"]*)"'
        action_input_pattern = r'"action_input":\s*"([^"]*)"'
        # 提取出匹配到的action值
        action = re.search(action_pattern, cleaned_output)
        action_input = re.search(action_input_pattern, cleaned_output)
        action_value=None
        if action:
            action_value = action.group(1)
        if action_input:
            action_input_value = action_input.group(1)

        # 如果遇到'Final Answer'，则判断为本次提问的最终答案了
        if action_value and action_input_value:
            if action_value == "Final Answer":
                return AgentFinish({"output": action_input_value}, text)
            else:
                return AgentAction(action_value, action_input_value, text)

        # 如果声明的正则未匹配到，则用json格式进行匹配
        print("text:\t",text)
        text=text[1:-1]
        print("text:\t", text)
        response = parse_json_markdown(text)

        action_value = response["action"]
        action_input_value = response["action_input"]
        if action_value == "Final Answer":
            return AgentFinish({"output": action_input_value}, text)
        else:
            return AgentAction(action_value, action_input_value, text)

from langchain.memory import ConversationBufferMemory
from langchain.agents.conversational_chat.base import ConversationalChatAgent
from langchain.agents import AgentExecutor, AgentOutputParser
from MyOpenAI import myOpenAi
SYSTEM_MESSAGE_PREFIX = """尽可能用中文回答以下问题。您可以使用以下工具"""

# 初始化大模型实例，可以是本地部署的，也可是是ChatGPT
# llm = ChatGLM(endpoint_url="http://你本地的实例地址")
llm = myOpenAi(temperature=0.7)
# 初始化工具
tools = [CalculatorTool(), SearchTool()]
output_parser = CustomOutputParser()
# 初始化对话存储，保存上下文
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# 配置agent
chat_agent = ConversationalChatAgent.from_llm_and_tools(
    system_message=SYSTEM_MESSAGE_PREFIX, # 指定提示词前缀
    llm=llm, tools=tools, memory=memory,
    verbose=True, # 是否打印调试日志，方便查看每个环节执行情况
    # output_parser=output_parser #
)
agent = AgentExecutor.from_agent_and_tools(
    agent=chat_agent, tools=tools, memory=memory, verbose=True,
    max_iterations=3 # 设置大模型循环最大次数，防止无限循环
)

res=agent.run("天下无贼主演是谁")
print("***\t"+res)


res=agent.run("该电影刘德华在里面是主演吗")
print("***\t"+res)


