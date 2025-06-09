from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

class DataLoader:
    def __init__(
        self,
        file_paths,
        encoding
    ):
        self.file_paths = file_paths
        self.encoding = encoding

    def load_documents(self):
        documents = []
        for path in self.file_paths:
            print(f"Loading document: {path}")
            loader = TextLoader(path, encoding=self.encoding)
            documents.extend(loader.load())
        return documents

    def get_retriever(documents):
        documents = self.load_documents()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        chunks = splitter.split_documents(documents)
        embedding = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(chunks, embedding)
        return vectorstore.as_retriever()
