import os

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)


class VectorStoreManager:

    def __init__(self):

        self.embedding_model = (
            HuggingFaceEmbeddings(
                model_name=
                "sentence-transformers/all-MiniLM-L6-v2"
            )
        )

        self.text_splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
        )

        self.vector_store = None

    # --------------------------
    # CREATE CHUNKS
    # --------------------------

    def create_chunks(
            self,
            text):

        chunks = (
            self.text_splitter
            .split_text(text)
        )

        return chunks

    # --------------------------
    # CREATE VECTOR STORE
    # --------------------------

    def create_vector_store(
            self,
            text):

        chunks = self.create_chunks(
            text
        )

        self.vector_store = (
            FAISS.from_texts(
                chunks,
                self.embedding_model
            )
        )

        return {

            "status":
                "success",

            "chunks":
                len(chunks)
        }

    # --------------------------
    # SEARCH
    # --------------------------

    def search(
            self,
            query,
            k=4):

        if not self.vector_store:

            raise ValueError(
                "Vector store not created."
            )

        docs = (
            self.vector_store
            .similarity_search(
                query,
                k=k
            )
        )

        return docs

    # --------------------------
    # SEARCH WITH SCORE
    # --------------------------

    def search_with_score(
            self,
            query,
            k=4):

        if not self.vector_store:

            raise ValueError(
                "Vector store not created."
            )

        docs = (
            self.vector_store
            .similarity_search_with_score(
                query,
                k=k
            )
        )

        return docs

    # --------------------------
    # SAVE INDEX
    # --------------------------

    def save_index(
            self,
            folder_path=
            "vector_db/faiss_index"):

        if self.vector_store:

            self.vector_store.save_local(
                folder_path
            )

            return True

        return False

    # --------------------------
    # LOAD INDEX
    # --------------------------

    def load_index(
            self,
            folder_path=
            "vector_db/faiss_index"):

        if not os.path.exists(
                folder_path):

            return False

        self.vector_store = (
            FAISS.load_local(
                folder_path,
                self.embedding_model,
                allow_dangerous_deserialization=True
            )
        )

        return True

    # --------------------------
    # STATISTICS
    # --------------------------

    def get_statistics(
            self,
            text):

        chunks = self.create_chunks(
            text
        )

        return {

            "characters":
                len(text),

            "words":
                len(
                    text.split()
                ),

            "chunks":
                len(chunks)
        }