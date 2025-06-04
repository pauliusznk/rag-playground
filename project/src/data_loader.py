from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def load():

    loader = TextLoader("../data/262ba704-1f02-45ea-9119-da7d33708d46_PN Rally Zemaitija 2025.md", encoding='utf-8')
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embedding = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(chunks, embedding)

    return vectorstore.as_retriever()
