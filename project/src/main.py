from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

from data_loader import load

load_dotenv()

retriever = load()

llm = ChatOpenAI(temperature=0, model="gpt-4.1-nano-2025-04-14")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

question = input("Q:\n")
response = qa_chain.run(question)
print("A:\n", response)
