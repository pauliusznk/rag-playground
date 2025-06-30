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

1. Remove all page headers, footers, and standalone page numbers. These may appear as:
   - A single number like `1`, `2`, `3`
   - A page counter like `1/16`, `2 / 16`, ` 15 /16`, etc.
   - Remove lines that only contain these types of page numbers.
2. Keep all actual rule or regulation content. Do not remove meaningful paragraphs or numbered clauses.
3. Reformat any tables into clean Markdown syntax.
4. Never summarize, guess, or explain what you're doing.
5. If no cleaning is needed, return the input text exactly as it is — no explanation or changes.

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