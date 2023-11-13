from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
# from langchain.llms import OpenAI
from MyOpenAI import myOpenAi as OpenAI
llm=OpenAI(temperature=0.7)

from langchain.prompts.prompt import PromptTemplate

_DEFAULT_SUMMARIZER_TEMPLATE = """逐步总结所提供的对话行，添加到先前的摘要上，返回一个新的摘要。
例子
目前总结:
人类问AI对人工智能的看法。人工智能认为人工智能是一种善的力量。
新的对话内容:
人类:为什么你认为人工智能是一种好的力量?
AI:因为人工智能将帮助人类充分发挥潜力。
新的概要:
人类问AI对人工智能的看法。人工智能认为人工智能是一种积极的力量，因为它将帮助人类充分发挥潜力。
示例结束
目前总结:
{summary}

新的对话:
{new_lines}

新的概要:"""
SUMMARY_PROMPT = PromptTemplate(
    input_variables=["summary", "new_lines"], template=_DEFAULT_SUMMARIZER_TEMPLATE
)

DEFAULT_TEMPLATE = """下面是一段人类和人工智能之间的友好对话。人工智能是健谈的，并根据其上下文提供许多具体细节。如果人工智能不知道一个问题的答案，它就会如实说它不知道
当前对话:
{history}
Human: {input}
AI:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=DEFAULT_TEMPLATE)

from langchain.chains import ConversationChain
conversation_with_summary = ConversationChain(
    llm=llm,
    prompt=PROMPT,
    memory=ConversationSummaryMemory(llm=llm,prompt=SUMMARY_PROMPT),
    verbose=True
)
res=conversation_with_summary.predict(input="你好, 警官，小明发生车祸了，我需要怎么办？")

print(1,res)
res=conversation_with_summary.predict(input="告诉我发生了什么")
print(2,res)