import os
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document


class DocumentLoader:

    def load_pdf(self, file_path):

        text = ""

        pdf = PdfReader(file_path)

        for page in pdf.pages:

            content = page.extract_text()

            if content:
                text += content + "\n"

        return text

    def load_docx(self, file_path):

        doc = Document(file_path)

        text = "\n".join(
            para.text
            for para in doc.paragraphs
        )

        return text

    def load_txt(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            return f.read()

    def load_csv(self, file_path):

        df = pd.read_csv(file_path)

        return df.to_string()

    def load_xlsx(self, file_path):

        df = pd.read_excel(file_path)

        return df.to_string()

    def load_document(self, file_path):

        ext = os.path.splitext(
            file_path
        )[1].lower()

        if ext == ".pdf":
            return self.load_pdf(file_path)

        elif ext == ".docx":
            return self.load_docx(file_path)

        elif ext == ".txt":
            return self.load_txt(file_path)

        elif ext == ".csv":
            return self.load_csv(file_path)

        elif ext == ".xlsx":
            return self.load_xlsx(file_path)

        else:
            raise ValueError(
                f"Unsupported file type: {ext}"
            )