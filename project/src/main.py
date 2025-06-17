from dotenv import load_dotenv
from Assistant import Assistant
from DataLoader import DataLoader
from TelegramBot import TelegramBot
import prompts

def main():
    load_dotenv()
    paths = [
            "../data/262ba704-1f02-45ea-9119-da7d33708d46_PN Rally Zemaitija 2025.pdf",
            "../data/2025-m.-Lietuvos-automobiliu-ralio-taisykles-T-2025.pdf"
             ]
    data_loader = DataLoader(paths)

    data_loader.load_documents()
    retriever = data_loader.vectorstore.as_retriever()
    assistant = Assistant(retriever, prompts.user_prompt, prompts.question_cleaning_prompt)
    bot = TelegramBot(assistant)
    bot.run()
if __name__ == "__main__":
    main()
