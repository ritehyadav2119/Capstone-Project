import os


os.makedirs("database", exist_ok=True)
os.makedirs("exports", exist_ok=True)
os.makedirs("vector_db", exist_ok=True)
os.makedirs("uploaded_documents", exist_ok=True)
import tempfile

import streamlit as st


from document_loader import DocumentLoader
from summarizer import DocumentSummarizer
from vector_store import VectorStoreManager
from chatbot import SmartDocumentAssistant
from analytics import DocumentAnalytics
from export_utils import ExportManager
from quiz_generator import QuizGenerator
from flashcard_generator import FlashcardGenerator
from ppt_generator import PPTGenerator


# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Intelligent Document Summarization System",
    page_icon="📚",
    layout="wide"
)


# ==================================
# CUSTOM CSS
# ==================================

st.markdown("""
<style>

.main .block-container{
    padding-top:1rem;
    max-width:1400px;
}

.hero{
    background:linear-gradient(135deg,#0d47a1,#1976d2);
    padding:25px;
    border-radius:15px;
    color:white;
    margin-bottom:20px;
}

.metric-card{
    background:#f5f9ff;
    padding:15px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)


# ==================================
# SESSION STATE
# ==================================

defaults = {

    "document_text": "",

    "summary_pack": None,

    "vector_db": None,

    "chatbot": None,

    "messages": [],

    "quiz": "",

    "flashcards": ""
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value





# ==================================
# HEADER
# ==================================

st.markdown(f"""
<div class="hero">

<h1>📚 Intelligent Document Summarization System</h1>


</div>
""", unsafe_allow_html=True)


# ==================================
# SIDEBAR
# ==================================

with st.sidebar:

    st.header(
        "📂 Upload Document"
    )

    uploaded_file = st.file_uploader(

        "Choose File",

        type=[
            "pdf",
            "docx",
            "txt",
            "csv",
            "xlsx"
        ]
    )



# ==================================
# DOCUMENT PROCESSING
# ==================================

if uploaded_file:

    with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(
                uploaded_file.name
            )[1]
    ) as tmp:

        tmp.write(
            uploaded_file.read()
        )

        temp_path = tmp.name

    loader = DocumentLoader()

    text = loader.load_document(
        temp_path
    )

    st.session_state.document_text = (
        text
    )

    summarizer = (
        DocumentSummarizer()
    )

    with st.spinner(
        "Generating Summary..."
    ):

        summary_pack = (
            summarizer.generate_all(
                text[:12000]
            )
        )

    st.session_state.summary_pack = (
        summary_pack
    )

    vector_db = (
        VectorStoreManager()
    )

    vector_db.create_vector_store(
        text
    )

    st.session_state.vector_db = (
        vector_db
    )

    st.session_state.chatbot = (
        SmartDocumentAssistant(
            vector_db
        )
    )

    st.success(
        "Document Processed Successfully"
    )


# ==================================
# DASHBOARD METRICS
# ==================================

if st.session_state.document_text:

    analytics = (
        DocumentAnalytics()
    )

    stats = (
        analytics.document_statistics(
            st.session_state.document_text
        )
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    col1.metric(
        "Words",
        stats["total_words"]
    )

    col2.metric(
        "Characters",
        stats["total_characters"]
    )

    col3.metric(
        "Reading Time",
        f"{stats['reading_time']} min"
    )

    col4.metric(
        "Complexity",
        analytics.complexity_score(
            st.session_state.document_text
        )
    )
# ==================================
# MAIN TABS
# ==================================

tabs = st.tabs(
    [
        "📄 Summary",
        "🤖 AI Assistant",
        "📊 Analytics"
    ]
)

# ==================================
# SUMMARY TAB
# ==================================

with tabs[0]:

    st.header(
        "📄 Document Summary"
    )

    if st.session_state.summary_pack:

        summary_pack = (
            st.session_state.summary_pack
        )

        summary_tabs = st.tabs(
            [
                "Short Summary",
                "Detailed Summary",
                "Bullet Summary",
                "Executive Summary",
                "Keywords",
                "Topics"
            ]
        )

        with summary_tabs[0]:

            st.write(
                summary_pack[
                    "short_summary"
                ]
            )

        with summary_tabs[1]:

            st.write(
                summary_pack[
                    "detailed_summary"
                ]
            )

        with summary_tabs[2]:

            st.write(
                summary_pack[
                    "bullet_summary"
                ]
            )

        with summary_tabs[3]:

            st.write(
                summary_pack[
                    "executive_summary"
                ]
            )

        with summary_tabs[4]:

            st.write(
                summary_pack[
                    "keywords"
                ]
            )

        with summary_tabs[5]:

            st.write(
                summary_pack[
                    "topics"
                ]
            )

    else:

        st.info(
            "Upload a document first."
        )


# ==================================
# AI ASSISTANT TAB
# ==================================

with tabs[1]:

    st.header(
        "🤖 Smart AI Assistant"
    )

    if st.session_state.chatbot:

        chatbot = (
            st.session_state.chatbot
        )

        st.subheader(
            "Suggested Questions"
        )

        for q in (
            chatbot.suggested_questions()
        ):

            st.write(
                "• " + q
            )

        st.markdown("---")

        user_question = (
            st.text_input(
                "Ask Anything"
            )
        )

        if st.button(
            "Send"
        ):

            with st.spinner(
                "Thinking..."
            ):

                answer = (
                    chatbot.ask(
                        user_question
                    )
                )

            st.session_state.messages.append(
                (
                    user_question,
                    answer
                )
            )

        st.subheader(
            "Conversation"
        )

        for q, a in (
            st.session_state.messages
        ):

            st.markdown(
                f"**You:** {q}"
            )

            st.markdown(
                f"**AI:** {a}"
            )

            st.markdown("---")

        col1, col2, col3 = (
            st.columns(3)
        )

        # Notes

        if col1.button(
            "📒 Generate Notes"
        ):

            notes = (
                chatbot.generate_notes()
            )

            st.text_area(
                "Notes",
                notes,
                height=250
            )

        # Quiz

        if col2.button(
            "📝 Generate Quiz"
        ):

            quiz = (
                chatbot.generate_quiz()
            )

            st.text_area(
                "Quiz",
                quiz,
                height=300
            )

        # Flashcards

        if col3.button(
            "🎓 Flashcards"
        ):

            cards = (
                chatbot.generate_flashcards()
            )

            st.text_area(
                "Flashcards",
                cards,
                height=300
            )

    else:

        st.info(
            "Upload document first."
        )


# ==================================
# ANALYTICS TAB
# ==================================

with tabs[2]:

    st.header(
        "📊 Analytics Dashboard"
    )

    if st.session_state.document_text:

        analytics = (
            DocumentAnalytics()
        )

        text = (
            st.session_state.document_text
        )

        stats = (
            analytics.document_statistics(
                text
            )
        )

        st.subheader(
            "Document Statistics"
        )

        st.json(
            stats
        )

        st.subheader(
            "Keyword Analysis"
        )

        keyword_df = (
            analytics.keyword_dataframe(
                text
            )
        )

        st.dataframe(
            keyword_df,
            use_container_width=True
        )

        st.subheader(
            "Keyword Frequency Chart"
        )

        fig = (
            analytics.plotly_frequency_chart(
                text
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader(
            "Complexity Score"
        )

        st.success(
            analytics.complexity_score(
                text
            )
        )

    else:

        st.info(
            "Upload a document first."
        )
# ==================================
# EXTRA FEATURE TABS
# ==================================

extra_tabs = st.tabs(
    [
        "📝 Quiz Generator",
        "🎓 Flashcards",
        "📊 PPT Generator",
        "📥 Export Center"
    ]
)

# ==================================
# QUIZ GENERATOR
# ==================================

with extra_tabs[0]:

    st.header(
        "📝 AI Quiz Generator"
    )

    if st.session_state.document_text:

        if st.button(
            "Generate Complete Quiz"
        ):

            quiz_gen = (
                QuizGenerator()
            )

            with st.spinner(
                "Generating Quiz..."
            ):

                quiz = (
                    quiz_gen.generate_complete_quiz(
                        st.session_state.document_text
                    )
                )

            st.session_state.quiz = quiz

            st.text_area(
                "Generated Quiz",
                quiz,
                height=500
            )

        if st.session_state.quiz:

            st.download_button(

                "⬇ Download Quiz",

                st.session_state.quiz,

                file_name="quiz.txt"
            )

    else:

        st.info(
            "Upload a document first."
        )


# ==================================
# FLASHCARDS
# ==================================

with extra_tabs[1]:

    st.header(
        "🎓 Flashcard Generator"
    )

    if st.session_state.document_text:

        if st.button(
            "Generate Flashcards"
        ):

            flash_gen = (
                FlashcardGenerator()
            )

            with st.spinner(
                "Generating Flashcards..."
            ):

                cards = (
                    flash_gen.generate_complete_pack(
                        st.session_state.document_text
                    )
                )

            st.session_state.flashcards = (
                cards
            )

            st.text_area(
                "Flashcards",
                cards,
                height=500
            )

        if st.session_state.flashcards:

            st.download_button(

                "⬇ Download Flashcards",

                st.session_state.flashcards,

                file_name=
                "flashcards.txt"
            )

    else:

        st.info(
            "Upload document first."
        )


# ==================================
# PPT GENERATOR
# ==================================

with extra_tabs[2]:

    st.header(
        "📊 AI PPT Generator"
    )

    if st.session_state.summary_pack:

        ppt_name = st.text_input(
            "Presentation Name",
            value="Research_Presentation"
        )

        if st.button(
            "Generate PPT"
        ):

            ppt_generator = (
                PPTGenerator()
            )

            ppt_file = (

                ppt_generator
                .generate_from_summary_pack(

                    ppt_name,

                    st.session_state
                    .summary_pack
                )
            )

            st.success(
                f"PPT Created:\n{ppt_file}"
            )

    else:

        st.info(
            "Upload document first."
        )


# ==================================
# EXPORT CENTER
# ==================================

with extra_tabs[3]:

    st.header(
        "📥 Export Center"
    )

    if st.session_state.summary_pack:

        exporter = (
            ExportManager()
        )

        summary = (

            st.session_state
            .summary_pack[
                "detailed_summary"
            ]
        )

        if st.button(
            "Export TXT"
        ):

            path = (
                exporter.export_txt(
                    summary,
                    "summary.txt"
                )
            )

            st.success(path)

        if st.button(
            "Export PDF"
        ):

            path = (
                exporter.export_pdf(

                    "Document Summary",

                    summary,

                    "summary.pdf"
                )
            )

            st.success(path)

        if st.button(
            "Export DOCX"
        ):

            path = (
                exporter.export_docx(

                    "Document Summary",

                    summary,

                    "summary.docx"
                )
            )

            st.success(path)

        if st.button(
            "Export Chat History"
        ):

            chatbot = (
                st.session_state.chatbot
            )

            path = (
                exporter.export_chat_history(
                    chatbot.get_history()
                )
            )

            st.success(path)

    else:

        st.info(
            "Upload document first."
        )