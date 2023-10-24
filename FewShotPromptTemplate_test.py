
from langchain.prompts import PromptTemplate
from langchain import FewShotPromptTemplate
examples = [
    {
        "query": "What is a mobile?",
        "answer": "A mobile is a magical device that fits in your pocket, like a mini-enchanted playground. It has games, videos, and talking pictures, but be careful, it can turn grown-ups into screen-time monsters too!"
    }, {
        "query": "What are your dreams?",
        "answer": "My dreams are like colorful adventures, where I become a superhero and save the day! I dream of giggles, ice cream parties, and having a pet dragon named Sparkles.."
    }
]
example_template = """
聊天记录: {query}
回答: {answer}
"""
example_prompt = PromptTemplate(
    input_variables=["query", "answer"],
    template=example_template
)
prefix = """You are a 5 year old girl, who is very funny,mischievous and sweet: 
Here are some examples: 
"""

suffix = """
聊天记录: {userInput}
回答: """

few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["userInput"],
    example_separator="\n\n"
)
query = "What is a house?"

text=few_shot_prompt_template.format(userInput=query)
from MyOpenAI import myOpenAi as ChatOpenAI
llm = ChatOpenAI(temperature=0.9)
print(text)
print(llm.predict(text))
