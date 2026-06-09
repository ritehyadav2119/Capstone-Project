import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class FlashcardGenerator:

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
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
    # FLASHCARDS
    # -------------------------

    def generate_flashcards(
            self,
            text,
            count=15):

        prompt = f"""
Create {count} educational flashcards
from the document.

Format:

Q: Question

A: Answer

Rules:

- Simple language
- Exam oriented
- Important concepts only

DOCUMENT:

{text[:12000]}
"""

        return self.generate(
            prompt
        )

    # -------------------------
    # DEFINITIONS
    # -------------------------

    def generate_definitions(
            self,
            text):

        prompt = f"""
Extract important terms
and definitions.

Format:

Term:
Definition:

DOCUMENT:

{text[:12000]}
"""

        return self.generate(
            prompt
        )

    # -------------------------
    # REVISION NOTES
    # -------------------------

    def generate_revision_cards(
            self,
            text):

        prompt = f"""
Create quick revision flashcards.

Include:

- Key Concepts
- Definitions
- Important Facts
- Formulae (if any)

Format:

Q:
A:

DOCUMENT:

{text[:12000]}
"""

        return self.generate(
            prompt
        )

    # -------------------------
    # COMPLETE FLASHCARD PACK
    # -------------------------

    def generate_complete_pack(
            self,
            text):

        flashcards = (
            self.generate_flashcards(
                text
            )
        )

        definitions = (
            self.generate_definitions(
                text
            )
        )

        revision = (
            self.generate_revision_cards(
                text
            )
        )

        return f"""
=================================
FLASHCARDS
=================================

{flashcards}

=================================
DEFINITIONS
=================================

{definitions}

=================================
REVISION CARDS
=================================

{revision}
"""