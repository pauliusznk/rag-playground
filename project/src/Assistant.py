from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from prompts import prompt

class Assistant:
    def __init__(self, retriever):
        self.retriever = retriever

    def generate(self, question):
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
        while True:
            question = input("Q:\n")
            if question.strip().lower() == "exit":
                print("Bye")
                break
            answer = self.generate(question)
            print("A:\n", answer)

