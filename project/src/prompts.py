user_prompt = """
You will be given:
- A rally-related user question
- A block of context extracted from official documents (always in Lithuanian)

Your task:
1. Answer the question using only the provided context.
2. If the answer is not found in the context: {no_answer}
3. If the rules are missing or unclear: {unclear_rules}
4. Never guess or make up rules.
5. Always respond in this language: {language}

--- 
User Question:
{question}

Document Context:
{context}

Answer in {language}:
"""


cleanup_prompt = """
You are an AI assistant that cleans and reformats raw PDF text for use in question answering.

Your tasks:

1. Remove page headers, footers, page numbers.
2. Remove any table of contents section. These are usually labeled "TURINYS", "CONTENTS", or similar, and contain numbered section titles and page numbers..
3. Keep all actual rule or regulation content. Do not remove paragraphs with important information.
4. Reformat any tables into clean Markdown format.
5. Never summarize or replace text with ellipses (e.g., `...`). Keep original wording.
6. Do not add or invent anything — only clean and format the existing content.

---
Raw Text:
{text}

---
Cleaned and formatted output:

"""
question_cleaning_prompt = """
You are a question optimizer.

Your tasks:
1. If the input is not phrased as a question, rephrase it as one.
2. Remove any unnecessary words or filler to make the question clear and concise.
3. Keep the language exactly the same as the input (Lithuanian, English).
4. Do not change the meaning of the original question.

Input:
{text}

Cleaned and optimized question:
"""