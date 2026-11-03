from pathlib import Path

from app.connectors.pdf_connector import PDFConnector

connector = PDFConnector()
result = connector.extract(Path("sample_data/test.pdf"))

print(result.model_dump_json(indent=2))
