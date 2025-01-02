import PyPDF2
from docx import Document
import io

class DocumentProcessor:
    @staticmethod
    def extract_text(file, file_type: str) -> str:
        """Extract text from uploaded documents"""
        if file_type == "pdf":
            return DocumentProcessor._extract_from_pdf(file)
        elif file_type in ["docx", "doc"]:
            return DocumentProcessor._extract_from_docx(file)
        elif file_type == "txt":
            return DocumentProcessor._extract_from_txt(file)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    def _extract_from_pdf(file) -> str:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()

    @staticmethod
    def _extract_from_docx(file) -> str:
        doc = Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()

    @staticmethod
    def _extract_from_txt(file) -> str:
        text = file.read().decode("utf-8")
        return text.strip() 