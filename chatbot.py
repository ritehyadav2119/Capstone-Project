import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()


class SmartDocumentAssistant:

    def __init__(
            self,
            vector_store):

        self.vector_store = (
            vector_store
        )

        self.chat_history = []

        self.llm = ChatGroq(

            model=
            "llama-3.3-70b-versatile",

            temperature=0.3,

            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

    # --------------------------------
    # CHAT HISTORY
    # --------------------------------

    def history_text(self):

        history = ""

        for item in (
            self.chat_history[-10:]
        ):

            history += f"""

User:
{item['question']}

Assistant:
{item['answer']}
"""

        return history

    # --------------------------------
    # DOCUMENT SEARCH
    # --------------------------------

    def retrieve_context(
            self,
            question):

        docs = (
            self.vector_store.search(
                question,
                k=4
            )
        )

        context = "\n\n".join(

            [
                doc.page_content
                for doc in docs
            ]
        )

        return context

    # --------------------------------
    # DOCUMENT ANSWER
    # --------------------------------

    def document_answer(
            self,
            question):

        context = (
            self.retrieve_context(
                question
            )
        )

        prompt = f"""
You are an AI document assistant.

Answer ONLY using
the provided document.

If answer is not found
say:

'Information not found
in uploaded document.'

DOCUMENT:

{context}

QUESTION:

{question}
"""

        response = (
            self.llm.invoke(
                prompt
            )
        )

        return (
            response.content
        )

    # --------------------------------
    # GENERAL CHAT
    # --------------------------------

    def general_chat(
            self,
            question):

        prompt = f"""
You are a helpful AI assistant.

Conversation:

{self.history_text()}

User:

{question}
"""

        response = (
            self.llm.invoke(
                prompt
            )
        )

        return (
            response.content
        )

    # --------------------------------
    # SMART DETECTION
    # --------------------------------

    def ask(
            self,
            question):

        keywords = [

            "document",

            "paper",

            "summary",

            "conclusion",

            "objective",

            "dataset",

            "methodology",

            "chapter",

            "report",

            "file"
        ]

        is_document_query = any(

            word in question.lower()

            for word in keywords
        )

        if is_document_query:

            answer = (
                self.document_answer(
                    question
                )
            )

        else:

            answer = (
                self.general_chat(
                    question
                )
            )

        self.chat_history.append(

            {
                "question":
                    question,

                "answer":
                    answer
            }
        )

        return answer

    # --------------------------------
    # NOTES GENERATOR
    # --------------------------------

    def generate_notes(self):

        prompt = """
Generate concise revision notes
from the uploaded document.

Include:

- Key Concepts
- Definitions
- Important Points
"""

        return (
            self.document_answer(
                prompt
            )
        )

    # --------------------------------
    # QUIZ GENERATOR
    # --------------------------------

    def generate_quiz(self):

        prompt = """
Generate 10 MCQs
from the uploaded document.

Include:

Question

4 Options

Correct Answer
"""

        return (
            self.document_answer(
                prompt
            )
        )

    # --------------------------------
    # FLASHCARDS
    # --------------------------------

    def generate_flashcards(
            self):

        prompt = """
Generate flashcards.

Format:

Q:
A:
"""

        return (
            self.document_answer(
                prompt
            )
        )

    # --------------------------------
    # SUGGESTED QUESTIONS
    # --------------------------------

    def suggested_questions(
            self):

        return [

            "What is the summary?",

            "What are the key findings?",

            "What is the conclusion?",

            "What methodology is used?",

            "What future work is suggested?"
        ]

    # --------------------------------
    # MEMORY
    # --------------------------------

    def clear_history(self):

        self.chat_history = []

    def get_history(self):

        return self.chat_history