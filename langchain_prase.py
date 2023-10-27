from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from MyOpenAI import myOpenAi as OpenAI
from MyOpenAI import myOpenAi as ChatOpenAI
# from langchain.chat_models import ChatOpenAI
response_schemas = [
    ResponseSchema(name="answer", description="answer to the user's question"),
    ResponseSchema(name="source", description="source used to answer the user's question, should be a website.")
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()
prompt = PromptTemplate(
    template="answer the users question as best as possible.\n{format_instructions}\n{question}",
    input_variables=["question"],
    partial_variables={"format_instructions": format_instructions}
)


model = OpenAI(temperature=0.9)
_input = prompt.format_prompt(question="what's the capital of france?")
print(_input)
output = model.predict(_input.to_string())
res=output_parser.parse(output)
# print(res)

chat_model = ChatOpenAI(temperature=0)

prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template("answer the users question as best as possible.\n{format_instructions}\n{question}")
    ],
    input_variables=["question","format_instructions"],
    partial_variables={"format_instructions": format_instructions}
)
_input = prompt.format_prompt(question="what's the capital of france?",format_instructions=format_instructions)
output =  model(_input.to_messages())
print(output_parser.parse(output.content))
