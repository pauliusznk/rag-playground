from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langdetect import detect
import re
import os
from chromadb import PersistentClient
from prompts import cleanup_prompt

class DataLoader:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def load_documents(self):
            chroma_exists = os.path.exists("./vectordb") and os.listdir("./vectordb")
            embedding = OpenAIEmbeddings(model="text-embedding-3-small")
            sources_in_db = []
            client = PersistentClient(path="./vectordb")
            self.vectorstore = Chroma(
                client=client,
                collection_name="rally_regulations",
                embedding_function=embedding,
                persist_directory="./vectordb"
            )

            if chroma_exists:
                metadatas = self.vectorstore.get()["metadatas"]
                for meta in metadatas:
                    if "source" in meta:
                        sources_in_db.append(meta["source"])

            self.documents = []
            for path in self.file_paths:
                if not chroma_exists or path not in sources_in_db:
                    loader = PyPDFLoader(path)
                    pages = loader.load()
                    page_text = ""
                    for page in pages:
                        lithuanian_text = self.extract_lithuanian_text(page.page_content)
                        if lithuanian_text:
                            page_text += lithuanian_text
                    cleaned_text = self.clean_document(page_text)
                    self.documents.append(
                        Document(page_content=cleaned_text, metadata={"source": path})
                    )
            self.upsert_documents_to_chroma()

    def print_documents(self):
        for doc in self.documents:
            print(f"File: {doc.metadata['source']}")
            print("Content:")
            print(doc.page_content)
            print("=" * 40)

    def extract_lithuanian_text(self, text):
        parts = re.split(r'\n{2,}|\n', text)
        lithuanian_text = ""
        for part in parts:
            try:
                lang = detect(part.strip())
                if lang != "en":
                    lithuanian_text += part.strip() + "\n"
            except:
                continue
        return lithuanian_text.strip()

    def clean_document(self, text):
        llm = ChatOpenAI(model="o4-mini-2025-04-16")
        prompt = PromptTemplate(input_variables=["text"], template=cleanup_prompt)
        chain = prompt | llm
        cleaned_text = chain.invoke({"text": text})

        return cleaned_text.content

    def upsert_documents_to_chroma(self):
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

        for doc in self.documents:
            chunks = splitter.split_documents([doc])
            self.vectorstore.add_documents(chunks)
            print(f"Inserted document from {doc.metadata.get('source')} into Chroma DB.")


