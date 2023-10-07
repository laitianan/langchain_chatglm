from typing import List, Tuple, Any, Union,Optional
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import BaseSingleActionAgent
from langchain import LLMChain, PromptTemplate
from langchain.base_language import BaseLanguageModel


class IntentAgent(BaseSingleActionAgent):
    tools: List
    llm: BaseLanguageModel

    # 通过 In-context Learning 的方式引导模型使用正确的工具
    intent_template: str = """
    现在有一些意图，类别为{intents}，你的任务是理解连续对话的意图，并判断该对话最后一个问题属于哪一类意图。
    回复的意图类别必须在提供的类别中，并且必须按格式回复：“意图类别：<>”。

    举例：
    问题：什么是游戏角色皮卡丘？
    意图类别：游戏角色信息查询

    问题：什么是演员刘德华？
    意图类别：演员信息查询
    
    问题：查询深圳前海店铺销量近15天的销量信息？
    意图类别：店铺销量统计信息查询
    
    问题：查询深圳前海店铺ID12456789销量近三个月的销量信息？
    意图类别：店铺销量统计信息查询
    
    问题：查询订单12456789的相关信息？
    意图类别：用户购买订单信息查询
    
    问题：“{query}”
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
        resp = self.llm_chain.predict(intents=tool_names, query=query)
        select_tools = [(name, resp.index(name)) for name in tool_names if name in resp]
        select_tools.sort(key=lambda x: x[1])
        return [x[0] for x in select_tools]

    @property
    def input_keys(self):
        return ["input"]

    # 通过 AgentAction 调用选择的工具，工具的输入是 "input"
    def plan(
            self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        # only for single tool
        tool_name = self.choose_tools(kwargs["input"])[0]
        print("tool_name:",tool_name)
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
    description = "存在用户历史购买订单的查询信息的工具，输入应该是用户对指定订单详情的查询"

    # 用来模拟知识库检索的 prompt, 正经做 retrive 可以使用 向量数据库 和 文本相似度匹配

    context = """
    现在有一些历史对话，你的任务是抽出用户问题的订单ID，
    回复的id必须按格式回复：“订单ID：<>”。
    举例：
    问题：我想查询订单号123456789的信息？
    订单ID：123456789

    问题：78945689？
    订单ID：78945689"""
    qa_template = """
    请根据下面带```分隔符的文本来生成提取对应的订单ID。
    如果该文本中没有相关订单号内容可以回答问题，请直接回复：“订单ID：<None>”
    ```{text}```
    问题：{query}
    """
    prompt = PromptTemplate.from_template(qa_template)
    llm_chain: LLMChain = None

    # 生成基于知识的回答
    def _call_func(self, query) -> str:
        # print(f"已知订单信息查询query******{query}*****")
        self.get_llm_chain()
        context=self.context
        resp = self.llm_chain.predict(text=context, query=query)
        # print(f"订单信息查询******{resp}*****")
        return resp

    def get_llm_chain(self):
        if not self.llm_chain:
            self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)



class Order_statistics_Tool(functional_Tool):
    llm: BaseLanguageModel

    # IntentAgent 会根据 description 与 query 的相关性选择工具
    name = "店铺销量统计信息查询"
    description = "商家店铺近段时间销总销量的查询信息的工具，输入应该是用户指定店铺名称查询或者店铺ID，以及对应的查询时间段"
    import datetime
    # 用来模拟知识库检索的 prompt, 正经做 retrive 可以使用 向量数据库 和 文本相似度匹配
    data_time=datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    import datetime
    # 用来模拟知识库检索的 prompt, 正经做 retrive 可以使用 向量数据库 和 文本相似度匹配
    data_time = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    context = f"""
        现在有一些历史对话，当前系统时间{data_time},你的任务是根据用户最后问题生成对应的SQL，其中数据库字段order_time为订单时间，shop_name为店铺名称，shop_ID为店铺ID
        回复的必须按格式回复：“sql：select sum(pay_money) from order_info where <>=<> and order_time >= <>  and order_time <= <>) ”。
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

        请根据下面带```分隔符的文本对话来生成提取对应的SQL。
        如果该文本对话中没有相关店铺信息内容可以回答问题，请直接回复：“sql：<None>”
        ```{text}```
        问题：{query}
        """
    prompt = PromptTemplate.from_template(qa_template)
    llm_chain: LLMChain = None

    # 生成基于知识的回答
    def _call_func(self, query) -> str:
        print(f"已知店铺信息查询query******{query}*****")
        self.get_llm_chain()
        context=self.context
        resp = self.llm_chain.predict(text=context, query=query)
        print(f"已知店铺查询******{resp}*****")
        return resp

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
from ChatGLM2 import ChatGLM2
llm = ChatGLM2(temperature=0.95)
tools = [Character_knowledge_Tool(llm=llm), Actor_knowledge_Tool(llm=llm),Order_select_Tool(llm=llm),Order_statistics_Tool(llm=llm)]

# 选择工具
agent = IntentAgent(tools=tools, llm=llm)
# agent.choose_tools("游戏角色马里奥是谁？")
# print(agent.choose_tools("用户：游戏角色马里奥是谁？\nAI:游戏角色信息查询\n用户：我想查询深圳前海店铺六月份的总销量"))

agent_exec = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=False, max_iterations=1)
# # agent_exec.run("查询订单的相关信息？")
res=agent_exec.run("我想查询深圳前海店铺六月份的总销量")
print("res:\t",res)