from pathlib import Path

from docling.document_converter import DocumentConverter

from app.connectors.base import BaseConnector
from app.ingestion.schemas import ExtractedDocument, ExtractedPage


class PDFConnector(BaseConnector):
    def __init__(self):
        self.converter = DocumentConverter()

    def extract(self, file_path: Path) -> ExtractedDocument:
        if not file_path.exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")

        if file_path.suffix.lower() != ".pdf":
            raise ValueError("Only PDF files are supported")

        result = self.converter.convert(str(file_path))
        doc = result.document

        pages = []

        for page_no in sorted(doc.pages):
            content = doc.export_to_markdown(page_no=page_no).strip()

            if content:
                pages.append(
                    ExtractedPage(
                        page_number=page_no,
                        content=content,
                        metadata={"source": "pdf"},
                    )
                )

        if not pages:
            raise ValueError("No text could be extracted from the PDF")

        return ExtractedDocument(
            title=file_path.stem,
            pages=pages,
            metadata={
                "source": "pdf",
                "file_name": file_path.name,
                "page_count": len(doc.pages),
            },
        )