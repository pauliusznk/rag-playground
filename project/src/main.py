from dotenv import load_dotenv
from Assistant import Assistant
from DataLoader import DataLoader

def main():
    load_dotenv()
    paths = [
            "../data/262ba704-1f02-45ea-9119-da7d33708d46_PN Rally Zemaitija 2025.md",
            "../data/614cd4e6-4cbc-4512-85ea-acaf192c3f16_6 Ekipažų saugos įranga.md"
             ]
    data_loader = DataLoader(paths, encoding="utf-8")
    retriever = data_loader.get_retriever()
    assistant = Assistant(paths, retriever)
    assistant.user_input()
    

if __name__ == "__main__":
    main()
