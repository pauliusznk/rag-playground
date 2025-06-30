from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb import PersistentClient
import os
import re
from prompts import cleanup_prompt

class DataLoader:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def load_documents(self):
        chroma_exists = os.path.exists("../vectordb") and os.listdir("../vectordb")
        embedding = OpenAIEmbeddings(model="text-embedding-3-large")
        sources_in_db = []
        client = PersistentClient(path="../vectordb")
        self.vectorstore = Chroma(
            client=client,
            collection_name="rally_regulations",
            embedding_function=embedding,
            persist_directory="../vectordb"
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
                cleaned_text = ""
                for page in pages:
                    if self.skip_page(page.page_content):
                        continue

                    page_cleaned = self.clean_page(page.page_content)
                    cleaned_text += page_cleaned + "\n"

                self.documents.append(
                    Document(page_content=cleaned_text.strip(), metadata={"source": path})
                )

        self.upsert_documents_to_chroma()
        self.save_cleaned_documents_txt()

    def skip_page(self, text):
        lines = text.splitlines()
        toc_matches = re.findall(r"^\s*.*?\.{5,}\s*\d+\s*$", text, re.MULTILINE)
        return len(lines) > 0 and len(toc_matches) / len(lines) > 0.5

    def clean_page(self, text):
        llm = ChatOpenAI(model="gpt-4.1-nano-2025-04-14")
        prompt = PromptTemplate(input_variables=["text"], template=cleanup_prompt)
        chain = prompt | llm
        result = chain.invoke({"text": text})
        return result.content

    def upsert_documents_to_chroma(self):
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        for doc in self.documents:
            chunks = splitter.split_documents([doc])
            self.vectorstore.add_documents(chunks)
            print(f"Inserted document from {doc.metadata.get('source')} into Chroma DB.")

    def save_cleaned_documents_txt(self):
        for doc in self.documents:
            filename = os.path.basename(doc.metadata.get("source", "output.txt"))
            filename = filename.replace(".pdf", ".txt")
            save_path = os.path.join("../cleaned_documents", filename)
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(doc.page_content)
