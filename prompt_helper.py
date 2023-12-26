from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from api_protocol import (
    InitInterfaceRequest,
    Interface
)

FUNTION_FORMAT_INSTRUCTIONS = """
给你下面的系统背景、api参数文档说明以及聊天记录:
当前系统背景：
当前时间{current_time},今天的开始日期时间为{current_date} 00:00:00,今天的结束日期时间为{current_date} 23:59:59,今天的日期为{current_date}，
昨天的开始日期时间为{yesterday} 00:00:00,昨天的结束日期时间为{yesterday} 23:59:59,昨天的日期为{yesterday},
前天的开始日期时间为{before_yesterday} 00:00:00,前天的结束日期时间为{before_yesterday} 23:59:59,前天的日期为{before_yesterday},
api参数说明：
{format_instructions}
聊天记录：
{user_input}

请你结合当前系统背景、参数说明和聊天记录,完成user表达的api参数值的提取,其中时间相关字段根据系统背景推理，而其他字段不能根据时间推理比如订单号,严格禁止捏造user聊天未提到参数值,最终结果使用json格式返回参数说明的所需字段名称跟值,比如{{"a":"a","b":"b"}},未知参数请返回null,且不能构建新的字段名称
你的回答:
"""


def create_fun_prompt(param: Interface) -> PromptTemplate:
    response_schemas = [ResponseSchema(name=p.name, type=p.type, description=f'{p.title},抽取不到时使用null代替') for
                        p in param.inputParams]

    format_instructions=[f"{row.name} |{row.type} | {row.description},默认值为null,严格禁止捏造user问题无关参数值" for row in response_schemas]
    format_instructions="\n".join(format_instructions)
    prompt = PromptTemplate(
        input_variables=["user_input", "current_time", "current_date","yesterday","before_yesterday"],
        partial_variables={"format_instructions": format_instructions},
        template=FUNTION_FORMAT_INSTRUCTIONS
    )
    return param.id, prompt


def init_all_fun_prompt(parmas: InitInterfaceRequest):
    prompt_dict = dict()
    for param in parmas.params:
        if param.usableFlag:
            id, prompt = create_fun_prompt(param)
            prompt_dict[id] = prompt
    return prompt_dict


INTENT_FORMAT_MULTI_INSTRUCTIONS: str = """
给你下面幸福西饼的意图类别,意图类别详情描述，历史对话沟通记录,
幸福西饼的意图类别为：
{intents}
备注意图详情描述：
{intention_summary}

对话沟通记录：
{user_input}

请你结合备注意图详情描述和对话沟通记录录,识别user想表达一个或多个意图类别,意图必须从意图类别中选择,最终结果使用json格式返回,输出应该是严格按以下模式格式化的标记代码片段,必须包括开头和结尾的" ' ' ' json"和" ' ' ' ":
```json
{{
    "intention_name": list  // 意图类别,意图类别必须在提供的类别中,比如intention_name=["a","b","c"]
}}
你的回答:
"""




INTENT_FORMAT_INSTRUCTIONS: str = """
现在有一些意图,类别为：{intents},
你扮演AI角色的任务是根据***分隔符的文本对话,来进行意图的识别`,对话中可能存在多轮对话意图,仅仅需要判断该对话user最后一个问题属于哪一类别意图。
输出应该是严格按以下模式格式化的标记代码片段,必须包括开头和结尾的" ' ' ' json"和" ' ' ' ":
```json
{{
    "intention_name": string  // 意图类别,意图类别必须在提供的类别中
}}
```
备注意图详情描述：
{intention_summary}
***
历史对话沟通记录：
{user_input}
***
你的回答:
"""

FUNTION_CALLING_FORMAT_INSTRUCTIONS = """
幸福西饼业务主要分布在全国各个城市,请根据幸福西饼已知信息回答用户关于幸福西饼的问题，
幸福西饼已知信息：{content},
请结合幸福西饼已知信息组织语言只回复用户相关问题,可能存在幸福西饼已知信息与用户问题无关，当问题模糊时候，你可以回复相关已知信息的详情，
未能解答回复或跟幸福西饼无关问题请直接回复:未能理解你的问题，请尝试咨询其他业务,
举例：
用户问题：查询习近平是出生日期是多少和广东省的最高GDP是多少
你的回复：未查到信息，请尝试咨询其他业务

用户问题：幸福西饼每年的捐款多少钱和创始人是谁
你的回复：未查到信息，请尝试咨询其他业务

用户问题：苹果手机每年的销量多少
你的回复：未查到信息，请尝试咨询其他业务

用户问题：核销苹果账单
你的回复：未查到信息，请尝试咨询其他业务
你的回复:
"""


if __name__ == '__main__':
    from MyOpenAI import myOpenAi

    llm = myOpenAi(temperature=0.8, max_tokens=2000)