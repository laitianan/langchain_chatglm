from langchain.chains.conversation.memory import ConversationBufferMemory
from MyOpenAI import  myOpenAi as OpenAI
from langchain.chains import ConversationChain

llm = OpenAI(temperature=0.9 )
memory = ConversationBufferMemory()

DEFAULT_TEMPLATE = """下面是一段Human和AI之间的友好对话。人工智能是健谈的，并根据其上下文提供许多具体细节,与Hunman沟通或者回答问题:
{history}
Human: {input}
AI:"""
from langchain.prompts.prompt import PromptTemplate
PROMPT = PromptTemplate(input_variables=["history", "input"], template=DEFAULT_TEMPLATE)

conversation = ConversationChain(
    llm=llm,
    verbose=False,
    memory=memory,
    prompt=PROMPT
)
res=conversation.predict(input="你好，我叫赖天安")
print(res)
res=conversation.predict(input="今天的天气挺不错的，非常适合运动")
print(res)
res=conversation.predict(input="你知道我叫什么名字吗")
print(res)