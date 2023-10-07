from langchain.chains import SimpleSequentialChain, SequentialChain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from ChatGLM2 import ChatGLM2 as ChatOpenAI
llm = ChatOpenAI(temperature=0.1)

# 第一条链，将评论翻译成英语。
first_prompt = ChatPromptTemplate.from_template(
    "Translate the following review to english:"
    "\n\n{Review}"
)
chain_one = LLMChain(llm=llm, prompt=first_prompt,
                     output_key="English_Review"
                     )

# 第二条链，用一句话总结该评论
second_prompt = ChatPromptTemplate.from_template(
    "Can you summarize the following review in 1 sentence:"
    "\n\n{English_Review}"
)
chain_two = LLMChain(llm=llm, prompt=second_prompt,
                     output_key="summary"
                     )

# 第三条链，检测原始评论的语言
third_prompt = ChatPromptTemplate.from_template(
    "What language is the following review:\n\n{Review}"
)
chain_three = LLMChain(llm=llm, prompt=third_prompt,
                       output_key="language"
                       )

# 第四条链，接收第二条链的摘要内容("summary"变量)，以及第三条链的语言类别("language"变量)，要求后续回复摘要内容时使用指定语言。
fourth_prompt = ChatPromptTemplate.from_template(
    "Write a follow up response to the following "
    "summary in the specified language:"
    "\n\nSummary: {summary}\n\nLanguage: {language}"
)
chain_four = LLMChain(llm=llm, prompt=fourth_prompt,
                      output_key="followup_message"
                      )

overall_chain = SequentialChain(
    chains=[chain_one, chain_two, chain_three, chain_four],
    input_variables=["Review"],
    output_variables=["English_Review", "summary","followup_message"],
    verbose=True
)

print(overall_chain("幸福西饼生日蛋糕挺好吃的，每年基本都有买给小孩子过生日，小孩子很喜欢"))