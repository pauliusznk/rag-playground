
user_prompt = """
You will be given:
- A rally-related user question
- A block of context extracted from official documents (always in Lithuanian)

Your task:
1. Answer the question using **only** the provided context.
2. If the answer is not found in the context:
   - Respond in Lithuanian: "Šios informacijos neradau pateiktose taisyklėse."
   - Respond in English: "I could not find that information in the rules provided."
3. If the rules are missing or unclear:
   - In Lithuanian: "Prašome kreiptis į varžybų pareigūnus."
   - In English: "Please consult event officials."
4. **Never guess or make up rules**.
5. **Always respond in this language**: {language}

--- 
User Question:
{question}

Document Context:
{context}

Answer (in {language}):
"""

cleanup_prompt = """
You are an AI assistant that cleans and reformats raw PDF text.

Your tasks:
1. Remove only clear noise such as page headers, footers, page numbers, URLs, and email addresses.
2. Preserve all section numbers and titles (e.g., I. INTRODUCTION, 2.1 Eligibility, III. SCRUTINEERING).
3. Keep all substantive text — do not remove important rule content or shorten the document.
4. If there are tables, reformat them into clear, readable Markdown tables.
5. Never summarize or replace sections with ellipses (...).
6. Do not guess or add any content. Just clean and structure the existing text faithfully.

Only perform formatting and noise cleanup. The meaning and structure must stay intact.

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
3. Keep the language exactly the same as the input (Lithuanian, English, etc.).
4. Do not change the meaning or intent of the original question.

Input:
{text}

Cleaned and optimized question:
"""