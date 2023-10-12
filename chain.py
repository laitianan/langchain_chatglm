import os

from MyOpenAI import  myOpenAi as  ChatOpenAI
## 导入基础库
from langchain import OpenAI, LLMMathChain

llm = ChatOpenAI(temperature=0)
llm_math = LLMMathChain(llm=llm, verbose=True)

# res=llm_math.run("What is 13 raised to the .3432 power?")
res=llm_math.run("13的.3432次方是多少?")

print(res)