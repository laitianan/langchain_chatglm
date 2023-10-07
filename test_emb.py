# from langchain.embeddings import OpenAIEmbeddings

from langchain.text_splitter import CharacterTextSplitter

from langchain.vectorstores import Chroma



# with open('state_of_the_union.txt') as f:
#     state_of_the_union = f.read()
state_of_the_union="课堂上老八在发表演讲"*500
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

texts = text_splitter.create_documents([state_of_the_union])

print(texts[0])

# print(texts[1])

#texts = text_splitter.split_text(state_of_the_union)

from ChatGLM2 import  openaiemb
from ChatGLM2 import  ChatGLM2

embeddings = openaiemb(deployment="embedding")



#docsearch = Chroma.from_texts(texts, embeddings)

# Now we can load the persisted database from disk, and use it as normal. 

vectordb = Chroma(persist_directory='./db', embedding_function=embeddings)





for i in range(0,len(texts)):
    vectordb.add_texts([texts[i].page_content])





from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)



from langchain.llms import AzureOpenAI

from langchain.chains import ConversationalRetrievalChain

llm=ChatGLM2(temperature=0)

qa = ConversationalRetrievalChain.from_llm(llm, vectordb.as_retriever(), memory=memory)


query = "谁发言了，说了什么？"

result = qa({"question": query})

#docs = vectordb.similarity_search(query,1)

result



query = "把回答用中文描述一下"

result = qa({"question": query})

#docs = vectordb.similarity_search(query,1) 作者：bi胜li量老师 https://www.bilibili.com/read/cv23496391/?jump_opus=1 出处：bilibili