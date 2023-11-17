
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from api_protocol import  (
InitInterfaceRequest,
Interface
)
FUNTION_FORMAT_INSTRUCTIONS = """
你的任务是根据***分隔符的历史对话沟通记录，从user和assistant聊天记录理解user需求，并从聊天记录抽取正确的结构值以结构化数据格式返回，取不到的值使用None代替,
部分时间直接从user聊天抽取不出来才结合系统当前时间推理,系统当前时间{current_time},比如则根据系统当前时间推理:今天的开始日期时间为{current_date} 00:00:00,今天的结束日期时间为{current_date} 23:59:59,严格禁止生成聊天记录不存在的数据,
输出应该是严格按以下模式格式化的标记代码片段，必须包括开头和结尾的" ' ' ' json"和" ' ' ' ":
{format_instructions}
历史对话沟通记录：
***
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
        input_variables=["user_input","current_time","current_date"],
        partial_variables={"format_instructions": format_instructions},
        template=FUNTION_FORMAT_INSTRUCTIONS
    )
    return param.id,prompt

def init_all_fun_prompt(parmas:InitInterfaceRequest):
    prompt_dict=dict()
    for param in parmas.params:
        if param.usableFlag:
            id,prompt=create_fun_prompt(param)
            prompt_dict[id]=prompt
    return prompt_dict


INTENT_FORMAT_MULTI_INSTRUCTIONS: str = """
现在有一些意图，类别为：{intents}，
你扮演AI角色的任务是根据***分隔符的文本对话，来进行意图的识别`，对话中可能存在一个或多个意图，使用列表方式返回,比如 intention_name:["a","b"]。
输出应该是严格按以下模式格式化的标记代码片段，必须包括开头和结尾的" ' ' ' json"和" ' ' ' ":
```json
{{
    "intention_name": list  // 意图类别，意图类别必须在提供的类别中
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


INTENT_FORMAT_INSTRUCTIONS: str = """
现在有一些意图，类别为：{intents}，
你扮演AI角色的任务是根据***分隔符的文本对话，来进行意图的识别`，对话中可能存在多轮对话意图，仅仅需要判断该对话user最后一个问题属于哪一类别意图。
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
你的回答:
"""




if __name__ == '__main__':

    from MyOpenAI import myOpenAi

    llm = myOpenAi(temperature=0.8,max_tokens=2000)
