from pathlib import Path

from app.connectors.pdf_connector import PDFConnector
from app.ingestion.normalizer import normalize_pdf

file_path = Path("sample_data/test.pdf")

extracted = PDFConnector().extract(file_path)
document = normalize_pdf(extracted, file_path)

print(document.model_dump_json(indent=2))
