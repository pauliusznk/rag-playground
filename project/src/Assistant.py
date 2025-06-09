from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from prompts import prompt
from DataLoader import DataLoader

class Assistant:
    def __init__(self, file_paths):
        load_dotenv()
        self.files = file_paths

    def generate(self, question):
        self.dataloader = DataLoader(self.files, "utf-8")
        self.retriever = self.dataloader.get_retriever()

        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                f"{prompt}\n"
                "Context:{context}\n"
                "Question:{question}"
            )
        )
        self.llm = ChatOpenAI(temperature=0.1, model="gpt-4.1-nano-2025-04-14")
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": self.prompt_template}
        )

        response = self.qa_chain.invoke({"query": question})
        return response['result']

    def user_input(self):
        question = input("Q:\n")
        answer = self.generate(question)
        print("A:\n", answer)

