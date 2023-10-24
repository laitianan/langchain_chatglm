# -*- coding: utf-8 -*-
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import pandas as pd
from MyOpenAI import myOpenAi


llm = myOpenAi(temperature=0.1,max_length=12)

# 告诉他我们生成的内容需要哪些字段，每个字段类型式啥
response_schemas = [
    ResponseSchema(type="array", name="time", description="文本中的日期时间列表"),
    ResponseSchema(type="array", name="people", description="文本中的人物列表"),
    ResponseSchema(type="array", name="place", description="文本中的地点列表"),
    ResponseSchema(type="array", name="org", description="文本中的组织机构列表"),
]

# 初始化解析器
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 生成的格式提示符
format_instructions = output_parser.get_format_instructions()
print(format_instructions)

template = """
给定下面的文本，找出特定的实体信息，并以结构化数据格式返回。

{format_instructions}

% USER INPUT:
{user_input}

YOUR RESPONSE:
"""

# prompt
prompt = PromptTemplate(
    input_variables=["user_input"],
    partial_variables={"format_instructions": format_instructions},
    template=template
)

promptValue = prompt.format(user_input="6月26日，广汽集团在科技日上首次公开展示飞行汽车项目，飞行汽车GOVE完成全球首飞。广汽研究院院长吴坚表示，GOVE可以垂直起降，并搭载双备份多旋翼飞行系统，保障飞行安全。")
# print(promptValue)
llm_output = llm(promptValue)
print(llm_output)

# 使用解析器进行解析生成的内容
print(output_parser.parse(llm_output))
