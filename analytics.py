import re

from collections import Counter

import pandas as pd

import plotly.express as px

from wordcloud import WordCloud


class DocumentAnalytics:

    def __init__(self):

        self.stop_words = {

            "the", "a", "an",

            "and", "or", "of",

            "to", "in", "on",

            "for", "with",

            "is", "are", "was",

            "were", "be", "been",

            "this", "that",

            "it", "its"
        }

    # ----------------------------
    # BASIC STATS
    # ----------------------------

    def document_statistics(
            self,
            text):

        words = text.split()

        sentences = re.split(
            r"[.!?]+",
            text
        )

        reading_time = round(
            len(words) / 200,
            2
        )

        return {

            "total_words":
                len(words),

            "total_characters":
                len(text),

            "total_sentences":
                len(sentences),

            "reading_time":
                reading_time,

            "average_word_length":
                round(

                    sum(
                        len(word)
                        for word in words
                    )

                    /

                    max(
                        len(words),
                        1
                    ),

                    2
                )
        }

    # ----------------------------
    # KEYWORDS
    # ----------------------------

    def extract_keywords(
            self,
            text,
            top_n=20):

        words = re.findall(
            r"\b[a-zA-Z]+\b",
            text.lower()
        )

        filtered_words = [

            word

            for word in words

            if word not in self.stop_words

            and len(word) > 2
        ]

        frequency = Counter(
            filtered_words
        )

        return frequency.most_common(
            top_n
        )

    # ----------------------------
    # DATAFRAME
    # ----------------------------

    def keyword_dataframe(
            self,
            text):

        keywords = (
            self.extract_keywords(
                text
            )
        )

        return pd.DataFrame(

            keywords,

            columns=[
                "Keyword",
                "Frequency"
            ]
        )

    # ----------------------------
    # BAR CHART
    # ----------------------------

    def plotly_frequency_chart(
            self,
            text):

        df = (
            self.keyword_dataframe(
                text
            )
        )

        fig = px.bar(

            df,

            x="Keyword",

            y="Frequency",

            title=
            "Top Keywords"
        )

        return fig

    # ----------------------------
    # WORD CLOUD
    # ----------------------------

    def generate_wordcloud(
            self,
            text):

        wc = WordCloud(

            width=1200,

            height=600,

            background_color=
            "white"

        ).generate(text)

        return wc

    # ----------------------------
    # COMPLEXITY SCORE
    # ----------------------------

    def complexity_score(
            self,
            text):

        words = text.split()

        avg_word_length = (

            sum(
                len(word)
                for word in words
            )

            /

            max(
                len(words),
                1
            )
        )

        if avg_word_length < 4:

            return "Easy"

        elif avg_word_length < 6:

            return "Medium"

        else:

            return "Advanced"

    # ----------------------------
    # INSIGHTS
    # ----------------------------

    def document_insights(
            self,
            text):

        return {

            "stats":
                self.document_statistics(
                    text
                ),

            "keywords":
                self.extract_keywords(
                    text
                ),

            "complexity":
                self.complexity_score(
                    text
                )
        }