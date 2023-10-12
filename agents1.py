from typing import List, Tuple, Any, Union,Optional
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import BaseSingleActionAgent
from langchain import LLMChain, PromptTemplate
from langchain.base_language import BaseLanguageModel
from langchain.memory import ConversationBufferMemory
from langchain.agents.conversational_chat.base import ConversationalChatAgent

from langchain.memory import ConversationBufferWindowMemory
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
memory = ConversationBufferWindowMemory( k=3,memory_key="chat_history", return_messages=True)
class IntentAgent(BaseSingleActionAgent):
    tools: List
    llm: BaseLanguageModel

    # 通过 In-context Learning 的方式引导模型使用正确的工具
    intent_template: str = """
    现在有一些意图，类别为{intents}，你扮演AI角色的任务是根据```分隔符的文本对话，并结合***分隔符的意图描述来进行意图的识别`，对话中可能存在多轮对话意图，仅仅需要判断该对话Human最后一个问题属于哪一类别意图。
    回复的意图类别必须在提供的类别中，并且必须按格式回复,语言为中文：“意图类别：<>”。
    ***
    举例：
    历史对话：什么是游戏角色皮卡丘？
    意图类别：游戏角色信息查询

    历史对话：什么是演员刘德华？
    意图类别：演员信息查询
    
    历史对话：查询深圳前海店铺销量近15天的销量信息？
    意图类别：店铺销量统计信息查询
    
    历史对话：查询深圳前海店铺销量近半年的销量信息？
    意图类别：店铺销量统计信息查询
    
    历史对话：查询深圳前海店铺ID12456789销量近三个月的销量信息？
    意图类别：店铺销量统计信息查询
    
    历史对话：查询订单12456789的相关信息？
    意图类别：用户购买订单信息查询
    
    历史对话：花生怎么种植出来的
    意图类别：其他意图

    历史对话：海底有什么
    意图类别：其他意图
    
    历史对话：‘’‘Human: 我想咨询订单456789\nAI: 订单456789正在配送之中\nHuman: 你好‘’‘
    意图类别：其他意图
    （原因是他问完订单详情，并且AI回复了，之后转去问其他意图不明显信息）
    
    历史对话：‘’‘Human: 前海店铺近一年的销量\nAI: 销量为5000万单\nHuman: 你好\nAI: 销量为5000万单\nHuman: 幸福西饼好吃吗\n‘’‘
    意图类别：其他意图
    （原因是他问完销量，并且AI回复了，之后转去问其他意图不明显信息）
    
    备注意图详情描述：{intention_summary}
    ***
    历史对话信息```{history}```
    """
    prompt = PromptTemplate.from_template(intent_template)
    llm_chain: LLMChain = None

    def get_llm_chain(self):
        if not self.llm_chain:
            self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)

    # 根据提示(prompt)选择工具
    def choose_tools(self, query) -> List[str]:
        self.get_llm_chain()
        tool_names = [tool.name for tool in self.tools]
        # tool_names+=["意图不明"]
        # intention_summary=["意图名称："+tool.name+",意图描述："+tool.description for tool in self.tools]
        # intention_summary="；".join(intention_summary)

        tool_strings = "\n".join(
            [f"> {tool.name}: {tool.description}" for tool in tools]
        )


        print("buffer_as_str\n"+memory.buffer_as_str)
        history=memory.buffer_as_str

        if history =='' or history is None:
            history="Human: "+query
        else:
            history += "\nHuman: " + query
        print("-------"+history)
        resp = self.llm_chain.predict(intents=tool_names,intention_summary=tool_strings, history=history)
        print(resp)
        select_tools = [(name, resp.index(name)) for name in tool_names if name in resp]
        select_tools.sort(key=lambda x: x[1])

        if len(select_tools)==0:
            return [No_Understand_Tool_Tool(llm=self.llm).name]

        return [e[0] for e in select_tools ]

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


from langchain.tools import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


# 重写抽象方法，"call_func"方法执行 tool
class functional_Tool(BaseTool):
    name: str = ""
    description: str = ""
    url: str = ""
    return_direct = True  # 直接返回结果

    def _call_func(self, query):
        raise NotImplementedError("subclass needs to overwrite this method")

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self._call_func(query)

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("APITool does not support async")


class Character_knowledge_Tool(functional_Tool):
    llm: BaseLanguageModel

    # IntentAgent 会根据 description 与 query 的相关性选择工具
    name = "游戏角色信息查询"
    description = "存有一些角色和信息的工具，输入应该是对游戏角色的询问"

    # 用来模拟知识库检索的 prompt, 正经做 retrive 可以使用 向量数据库 和 文本相似度匹配
    context = "已知游戏角色信息：  Mario: 马里奥是日本电子游戏设计师宫本茂创作的一个角色。他是同名电子游戏系列的主角，也是日本电子游戏公司任天堂的吉祥物。Princess Peach: 碧姬公主，是任天堂著名游戏系列马里奥系列中的重要角色。她是游戏中虚构的蘑菇王国的公主，也是王国的统治者。"
    qa_template = """
    请根据下面带```分隔符的文本来回答问题。
    如果该文本中没有相关内容可以回答问题，请直接回复：“抱歉，该问题需要更多上下文信息。”
    ```{text}```
    问题：{query}
    """
    prompt = PromptTemplate.from_template(qa_template)
    llm_chain: LLMChain = None

    # 生成基于知识的回答
    def _call_func(self, query) -> str:
        # print(f"已知游戏角色信息query******{query}*****")
        self.get_llm_chain()
        context = "已知游戏角色信息：  Mario: 马里奥是日本电子游戏设计师宫本茂创作的一个角色。他是同名电子游戏系列的主角，也是日本电子游戏公司任天堂的吉祥物。Princess Peach: 碧姬公主，是任天堂著名游戏系列马里奥系列中的重要角色。她是游戏中虚构的蘑菇王国的公主，也是王国的统治者。"
        resp = self.llm_chain.predict(text=context, query=query)
        # print(f"已知游戏角色信息******{resp}*****")
        return resp

    def get_llm_chain(self):
        if not self.llm_chain:
            self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)

class Order_select_Tool(functional_Tool):
    llm: BaseLanguageModel

    # IntentAgent 会根据 description 与 query 的相关性选择工具
    name = "用户购买订单信息查询"
    description = "根据订单id查询订单详情信息的工具，输入应该是对订单的询问"

    context = """
    举例：
    问题：我想查询订单号123456789的信息？
    订单ID：123456789

    问题：78945689？
    订单ID：78945689"""
    qa_template = """
    请根据下面带```历史对话来生成提取对应的订单ID，回复的id必须按格式回复：“订单ID：<>”。
    如果该文本中没有相关订单号内容可以回答问题，请直接回复：“订单ID：<None>”
    {text}
    ```历史对话：{history}```
    """
    prompt = PromptTemplate.from_template(qa_template)
    llm_chain: LLMChain = None

    # 生成基于知识的回答
    def _call_func(self, query) -> str:
        # print(f"已知订单信息查询query******{query}*****")
        self.get_llm_chain()
        context=self.context
        history=memory.buffer_as_str
        if history =='' or history is None:
            history="Human: "+query
        else:
            history += "\nHuman: " + query
        resp = self.llm_chain.predict(text=context, history=history)

        if "None" in resp:
            return "请输入你咨询的订单ID"
        # print(f"订单信息查询******{resp}*****")
        order_id=resp.replace("订单ID：","")
        return f"你购买的订单{order_id}正在配送之中"

    def get_llm_chain(self):
        if not self.llm_chain:
            self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)


class No_Understand_Tool_Tool(functional_Tool):
    llm: BaseLanguageModel

    # IntentAgent 会根据 description 与 query 的相关性选择工具
    name = "其他意图"
    description = "用户随便询问的内容,当其他意图不匹配时请选择该意图"

    llm_chain: LLMChain = None

    # 生成基于知识的回答
    def _call_func(self, query) -> str:
        # self.get_llm_chain()
        history = memory.buffer_as_str
        if history =='' or history is None:
            history="Human: "+query
        else:
            history += "\nHuman: " + query
        resp = self.llm.predict("当前你的角色是幸福西饼的AI客服，请根据下面的历史聊天记录回答用户问题,聊天记录中的AI是你的角色\n"+history)
        try:
            index=resp.index(":")
            if index<=3:
                resp=resp[index+1:]
        except :
            pass
        return resp

    def get_llm_chain(self):
        if not self.llm_chain:
            self.llm_chain = LLMChain(llm=self.llm)



class Order_statistics_Tool(functional_Tool):
    llm: BaseLanguageModel

    # IntentAgent 会根据 description 与 query 的相关性选择工具
    name = "店铺销量统计信息查询"
    description = "店铺总销量查询信息的工具，输入应该是对指定店铺名称或店铺ID，查询某时间段总销量"
    import datetime
    # 用来模拟知识库检索的 prompt, 正经做 retrive 可以使用 向量数据库 和 文本相似度匹配
    data_time=datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    import datetime
    # 用来模拟知识库检索的 prompt, 正经做 retrive 可以使用 向量数据库 和 文本相似度匹配
    data_time = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    context = f"""
        现在有一些历史对话，当前系统时间{data_time},你的任务是根据用户最后问题生成对应的SQL，其中数据库字段order_time为订单时间，shop_name为店铺名称，shop_ID为店铺ID
        回复的必须按格式回复：“sql：select sum(pay_money) from order_info where <>=<> and order_time >= <>  and order_time <= <> ”。
        举例：
        问题：我想查询店铺123456789的销量近三个月的销量信息？
        sql：select sum(pay_money) from order_info where shop_ID='123456789' and order_time >= DATE_SUB(NOW(), INTERVAL 3 MONTH) 
        问题：查询深圳前海店铺ID12456789销量近15天的销量信息
        sql：select sum(pay_money) from order_info where shop_ID='12456789' and order_time >= DATE_SUB(NOW(), INTERVAL 15 Day)  
        问题：我想查询深圳前海店铺销量近15天的销量信息？
        sql：select sum(pay_money) from order_info where shop_name='深圳前海店铺' and order_time >= DATE_SUB(NOW(), INTERVAL 15 DAY) 
        问题：我想查询深圳前海店铺今年七月份的销量信息？
        sql：select sum(pay_money) from order_info where shop_name='深圳前海店铺' and order_time >= '2023-07-01'  and order_time <= '2023-07-31'
        问题：我想查询深圳前海店铺今年七月份初到今年九月底的销量信息？
        sql：select sum(pay_money) from order_info where shop_name='深圳前海店铺' and order_time >= 2023-07-01'  and order_time <= '2023-10-01'
        """
    # print(context)
    qa_template = """

        请根据下面带***分隔符模板的文本，并根据下面带```分隔符文本对话来生成提取对应的SQL。
        如果对话中没有相关店铺信息内容可以回答问题，请直接回复：“sql：<None>”
        ***{text}***
        对话：```{query}```
        """
    prompt = PromptTemplate.from_template(qa_template)
    llm_chain: LLMChain = None

    # 生成基于知识的回答
    def _call_func(self, query) -> str:
        # print(f"已知店铺信息查询query******{query}*****")
        self.get_llm_chain()
        context=self.context
        resp = self.llm_chain.predict(text=context, query=query)
        print(f"已知店铺查询******{resp}*****")
        return "销量为5000万单"

    def get_llm_chain(self):
        if not self.llm_chain:
            self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)


class Actor_knowledge_Tool(functional_Tool):
    llm: BaseLanguageModel

    # tool description
    name = "演员信息查询"
    description = "存有一些演员的工具，输入应该是对演员的询问"

    # QA params
    qa_template = """
    请根据下面带```分隔符的文本对话最后的问题来回答问题。
    如果该文本对话中没有相关内容可以回答问题，请直接回复：“抱歉，该问题需要更多上下文信息。”
    ```{text}```
    问题：{query}
    """
    prompt = PromptTemplate.from_template(qa_template)
    llm_chain: LLMChain = None

    def _call_func(self, query) -> str:
        # print(f"已知演员信息query******{query}*****")
        self.get_llm_chain()
        context = "已知演员信息：  梁朝伟: 1962年6月27日出生于中国香港，祖籍广东台山，华语影视男演员、歌手，国家一级演员, 汤唯: 1979年10月7日出生于浙江省杭州市，毕业于中央戏剧学院导演系本科班，中国内地女演员。"
        resp = self.llm_chain.predict(text=context, query=query)
        # print(f"已知演员信息******{resp}*****")
        return resp

    def get_llm_chain(self):
        if not self.llm_chain:
            self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)




from langchain.agents import AgentExecutor
from MyOpenAI import myOpenAi
llm = myOpenAi(temperature=0.7)

# order=Order_select_Tool(llm=llm)
# res=order._run("查询订单123456")
# print(res)
# if True:
#     exit()

tools = [Character_knowledge_Tool(llm=llm), Actor_knowledge_Tool(llm=llm),No_Understand_Tool_Tool(llm=llm),Order_select_Tool(llm=llm),Order_statistics_Tool(llm=llm)]

# # 选择工具
agent = IntentAgent(tools=tools, llm=llm)
A="""'Human: 游戏角色马里奥是谁
AI: 马里奥是日本电子游戏设计师宫本茂创作的一个角色
Human: 我想查询深圳前海店铺最近六个月的总销量
AI: sql：select sum(pay_money) from order_info where shop_name=\'深圳前海店铺\' and order_time >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
'Human: 我想查询订单
AI: 你的订单ID 为空，请输入你的资讯的订单ID
'Human: 12346
'"""

# for i in range(0):
#     # agent.choose_tools("用户：游戏角色马里奥是谁？\nAI：意图类别：游戏角色信息查询\n用户：我想查询深圳前海店铺最近六个月的总销量")
#     print(agent.choose_tools("用户：游戏角色马里奥是谁？\nAI：意图类别：游戏角色信息查询\n用户：我想查询深圳前海店铺最近六个月的总销量"))

# agent_exec = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=False, max_iterations=1)
# # agent_exec.run("查询订单的相关信息？")
# res=agent_exec.run("用户：游戏角色马里奥是谁？\nAI：意图类别：游戏角色信息查询\n用户：我想查询深圳前海店铺六月份的总销量\nAI：意图类别：店铺销量统计信息查询\n用户：我想查询订单12456的详细信息")
# res=agent_exec.run("用户：游戏角色马里奥是谁？\nAI：意图类别：游戏角色信息查询\n用户：我想查询深圳前海店铺最近六个月的总销量")
# print("res:\t",res)
DEFAULT_TEMPLATE = """下面是一段Human和AI之间的友好对话。人工智能是健谈的，并根据其上下文提供许多具体细节,与Hunman沟通或者回答问题:
{history}
Human: {input}
AI:"""
from langchain.prompts.prompt import PromptTemplate
PROMPT = PromptTemplate(input_variables=["history", "input"], template=DEFAULT_TEMPLATE)

# 配置agent
chat_agent = ConversationalChatAgent.from_llm_and_tools(
    llm=llm, tools=tools, memory=memory,
    verbose=True, # 是否打印调试日志，方便查看每个环节执行情况
    # output_parser=output_parser #
)
agent_exec = AgentExecutor.from_agent_and_tools(agent=agent, memory=memory, tools=tools, verbose=False, max_iterations=1)

# agent = AgentExecutor.from_agent_and_tools(
#     agent=chat_agent, tools=tools, memory=memory, verbose=True,
#     max_iterations=3 # 设置大模型循环最大次数，防止无限循环
# )



# res=agent_exec.run(A)
# memory.save_context({"input": "Hi"},{"output": "What's up"})
# print(memory.load_memory_variables({}))
# print("***--"+res)
# # print(agent.choose_tools(A))
# if True:
#     exit()
# res=agent_exec.run("游戏角色马里奥是谁")
# print(res)
# print("111111111111")
# res=agent_exec.run("我想查询深圳前海店铺最近六个月的总销量")
# print("2222222222222222")
# print(res)
#
# res=agent_exec.run("我想查询订单的配送时间")
# print("33333333333333333")
# print(res)
# res=agent_exec.run("1245648")
# print("44444444444444444444444444")
# print(res)
# print(memory.load_memory_variables({})["chat_history"])
# res=agent_exec.run("你知道我问谁出生在哪吗")
# print(res)


# res=agent_exec.run("我想咨询订单4567896")
# print("33333333333333333")
# print(res)
# res=agent_exec.run("你好")
# print("44444444444444444444444444")

while True:
    try:
        user_input = input("请输入您的问题：")
        response = agent_exec.run(user_input)
        print("****:\t"+response)
        # print("history:\t"+str(memory.load_memory_variables({})["chat_history"]))
    except KeyboardInterrupt:
        break