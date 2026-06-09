import os
import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class DocumentSummarizer:

    def __init__(self):

        api_key = st.secrets.get(
            "GROQ_API_KEY",
            os.getenv("GROQ_API_KEY")
        )

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            api_key=api_key
        )

    # baaki methods yahan...

    # -----------------------------
    # GENERIC GENERATOR
    # -----------------------------

    def generate(
            self,
            prompt):

        response = self.llm.invoke(
            prompt
        )

        return response.content

    # -----------------------------
    # SHORT SUMMARY
    # -----------------------------

    def short_summary(
            self,
            text):

        prompt = f"""
Create a concise summary of the
following document.

Length:
100-150 words.

DOCUMENT:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # DETAILED SUMMARY
    # -----------------------------

    def detailed_summary(
            self,
            text):

        prompt = f"""
Create a detailed summary of the
following document.

Include:

- Main Ideas
- Important Points
- Conclusion

Length:
300-500 words.

DOCUMENT:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # BULLET SUMMARY
    # -----------------------------

    def bullet_summary(
            self,
            text):

        prompt = f"""
Summarize the document in bullet points.

Return 10 important points.

DOCUMENT:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # EXECUTIVE SUMMARY
    # -----------------------------

    def executive_summary(
            self,
            text):

        prompt = f"""
Create an executive summary for managers,
teachers and decision makers.

DOCUMENT:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # KEYWORDS
    # -----------------------------

    def extract_keywords(
            self,
            text):

        prompt = f"""
Extract the 15 most important keywords
from the document.

Return only keywords.

DOCUMENT:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # TOPICS
    # -----------------------------

    def extract_topics(
            self,
            text):

        prompt = f"""
Identify the main topics discussed
in the document.

Return as bullet points.

DOCUMENT:

{text}
"""

        return self.generate(
            prompt
        )

    # -----------------------------
    # COMPLETE SUMMARY PACK
    # -----------------------------

    def generate_all(
            self,
            text):

        return {

            "short_summary":
                self.short_summary(
                    text
                ),

            "detailed_summary":
                self.detailed_summary(
                    text
                ),

            "bullet_summary":
                self.bullet_summary(
                    text
                ),

            "executive_summary":
                self.executive_summary(
                    text
                ),

            "keywords":
                self.extract_keywords(
                    text
                ),

            "topics":
                self.extract_topics(
                    text
                )
        }
