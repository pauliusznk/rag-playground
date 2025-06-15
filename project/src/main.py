from dotenv import load_dotenv
from Assistant import Assistant
from DataLoader import DataLoader
import tiktoken
import os
from prompts import prompt

def main():
    load_dotenv()
    paths = [
            "../data/262ba704-1f02-45ea-9119-da7d33708d46_PN Rally Zemaitija 2025.pdf",
            "../data/2025-m.-LARC-reglamentas-LT-EN-publikavimui.pdf",
            "../data/2025-m.-Lietuvos-automobiliu-ralio-taisykles-T-2025.pdf",
            "../data/2025-m.-Lithuanina-Rally4-Trophy-regulations-LT-EN.pdf",
            "../data/LASK 2025 05 22.pdf"
             ]
    data_loader = DataLoader(paths)

    data_loader.load_documents()
    retriever = data_loader.vectorstore.as_retriever(search_kwargs={"k":4})
    assistant = Assistant(retriever)
    assistant.user_input()
if __name__ == "__main__":
    main()
