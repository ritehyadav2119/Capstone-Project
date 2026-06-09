import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class QuizGenerator:

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.4,
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

    # -------------------------
    # GENERIC GENERATOR
    # -------------------------

    def generate(
            self,
            prompt):

        response = self.llm.invoke(
            prompt
        )

        return response.content

    # -------------------------
    # MCQ QUIZ
    # -------------------------

    def generate_mcq(
            self,
            text,
            questions=10):

        prompt = f"""
Create {questions}
multiple-choice questions
from the document.

Rules:

- 4 options per question
- Mention correct answer
- Professional format

DOCUMENT:

{text[:12000]}
"""

        return self.generate(
            prompt
        )

    # -------------------------
    # SHORT QUESTIONS
    # -------------------------

    def generate_short_questions(
            self,
            text,
            questions=5):

        prompt = f"""
Create {questions}
short-answer questions
from the document.

DOCUMENT:

{text[:12000]}
"""

        return self.generate(
            prompt
        )

    # -------------------------
    # LONG QUESTIONS
    # -------------------------

    def generate_long_questions(
            self,
            text,
            questions=5):

        prompt = f"""
Create {questions}
long-answer university level
questions from the document.

DOCUMENT:

{text[:12000]}
"""

        return self.generate(
            prompt
        )

    # -------------------------
    # COMPLETE QUIZ PACK
    # -------------------------

    def generate_complete_quiz(
            self,
            text):

        mcq = self.generate_mcq(
            text
        )

        short_q = (
            self.generate_short_questions(
                text
            )
        )

        long_q = (
            self.generate_long_questions(
                text
            )
        )

        return f"""

==========================
MCQ QUESTIONS
==========================

{mcq}

==========================
SHORT QUESTIONS
==========================

{short_q}

==========================
LONG QUESTIONS
==========================

{long_q}

"""