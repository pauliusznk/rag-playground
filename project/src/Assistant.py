from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langdetect import detect

class Assistant:
    def __init__(self, retriever, user_prompt, question_cleaning_prompt):
        self.retriever = retriever
        self.user_prompt = user_prompt
        self.question_cleaning_prompt = question_cleaning_prompt
        self.llm = ChatOpenAI(model="gpt-4.1-nano-2025-04-14", temperature=0.1)

    def generate(self, question):
        print("Original question:", question)
        
        language = detect(question)
        print("Detected language:", language)
        if language == "lt":
            language_code = "Lietuvių"
        else:
            language_code = "English"            

        question_cleaning_prompt = PromptTemplate(
            input_variables=["text"],
            template=self.question_cleaning_prompt
        )
        chain = question_cleaning_prompt | self.llm | StrOutputParser()
        cleaned_question = chain.invoke({"text": question})
        print("Cleaned question:", cleaned_question)

        documents = self.retriever.invoke(cleaned_question)
        context_text = ""
        for doc in documents:
            context_text += doc.page_content + "\n\n"
        print("Context text:", context_text)
        answer_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=self.user_prompt
        )
        answer_chain = answer_prompt | self.llm | StrOutputParser()
        answer = answer_chain.invoke({
            "context": context_text,
            "question": cleaned_question,
            "language": language_code
        })


        return answer

    def user_input(self):
        while True:
            question = input("Q:\n")
            if question.strip().lower() == "exit":
                print("Bye")
                break
            answer = self.generate(question)
            print("A:\n", answer)
