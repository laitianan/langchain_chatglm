
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from api_protocol import  (
InitInterfaceRequest,
Interface
)
funtion_context = """

你的任务是根据***分隔符的历史对话沟通记录，理解聊天记录用户最后需求，并抽取值以结构化数据格式返回，取不到的值使用None代替，严格禁止生成聊天记录不存在的数据，
系统当前时间{current_time}，部分时间需要通过当前时间计算，
输出应该是严格按以下模式格式化的标记代码片段，必须包括开头和结尾的" ' ' ' json"和" ' ' ' ":
{format_instructions}

***
历史对话沟通记录：
    {user_input}
***

你的回答:
"""
def create_fun_prompt(param:Interface)->PromptTemplate:
    response_schemas = [ResponseSchema(name=p.name,type=p.type, description=f'{p.title}，抽取不到时使用"None"代替') for p in param.inputParams]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    # 获取响应格式化的指令
    format_instructions = output_parser.get_format_instructions(only_json=True)
    prompt = PromptTemplate(
        input_variables=["user_input","current_time"],
        partial_variables={"format_instructions": format_instructions},
        template=funtion_context
    )
    return param.id,prompt

def init_all_fun_prompt(parmas:InitInterfaceRequest):
    prompt_dict=dict()
    for param in parmas.params:
        if param.usableFlag:
            id,prompt=create_fun_prompt(param)
            prompt_dict[id]=prompt
    return prompt_dict



INTENT_FORMAT_INSTRUCTIONS: str = """
现在有一些意图，类别为：{intents}，
你扮演AI角色的任务是根据***分隔符的文本对话，来进行意图的识别`，对话中可能存在多轮对话意图，仅仅需要判断该对话Human最后一个问题属于哪一类别意图。
输出应该是严格按以下模式格式化的标记代码片段，必须包括开头和结尾的" ' ' ' json"和" ' ' ' ":
```json
{{
    "intention_name": string  // 意图类别，意图类别必须在提供的类别中
}}
```
备注意图详情描述：
    {intention_summary}
***
历史对话沟通记录：
    {user_input}
***
你的回答：
"""




if __name__ == '__main__':

    from MyOpenAI import myOpenAi

    llm = myOpenAi(temperature=0.8,max_tokens=2000)

    intents=['游戏角色信息查询', '演员信息查询', '其他意图', '用户购买订单信息查询', '店铺销量统计信息查询']
    intention_summary="""
    1.游戏角色信息查询: 存有一些角色和信息的工具，输入应该是对游戏角色的询问
    2.演员信息查询: 存有一些演员的工具，输入应该是对演员的询问
    3.其他意图: 用户随便询问的内容,当其他意图不匹配时请选择该意图
    4.用户购买订单信息查询: 根据订单id查询订单详情信息的工具，输入应该是对订单的询问
    5.店铺销量统计信息查询: 销量信息查询工具，主要是店铺总销量查询信息，输入是对指定店铺名称或店铺ID，查询某时间段的总销量
    """
    # from utils import load_interface_template
    #
    #
    # init_obj=load_interface_template("./data/")
    # prompt=get_fun_prompt('999',init_obj)
    # prompt = PromptTemplate(
    #     input_variables=["user_input"],
    #     partial_variables={"intention_summary": intention_summary,"intents":intents},
    #     template=intent_template
    # )

    # input=INTENT_FORMAT_INSTRUCTIONS.format(user_input="物理应该怎么学习",intention_summary=intention_summary,intents=intents)
    # print(input)
    # print("-------------------------------------------------------------------------------------")
    # res=llm.predict(input)
    # print(res)

    tmp="""
    你的任务是根据***分隔符的历史对话沟通记录，理解聊天记录用户最后需求，并抽取值以结构化数据格式返回，取不到的值使用None代替，严格禁止生成聊天记录不存在的数据，
输出应该是严格按以下模式格式化的标记代码片段，必须包括开头和结尾的" ' ' ' json"和" ' ' ' ":

```json
{
	"order_id": string  // 订单ID，抽取不到时使用None代替
	"datetime": string  // 订单时间，抽取不到时使用None代替
}
```

***
历史对话沟通记录：
    user:我想查询订单456的详情
***

你的回答:
            """

    res=llm.predict(tmp)
    print(res)