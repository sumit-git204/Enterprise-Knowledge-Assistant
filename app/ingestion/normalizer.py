import hashlib
import json
from pathlib import Path
from uuid import uuid4

from app.ingestion.schemas import (
    DataSource,
    Document,
    DocumentType,
    ExtractedDocument,
)


def normalize_pdf(
    extracted: ExtractedDocument,
    file_path: Path,
) -> Document:
    content = "\n\n".join(
        page.content.strip()
        for page in extracted.pages
        if page.content.strip()
    )
    checksum = hashlib.sha256(content.encode("utf-8")).hexdigest()

    metadata = {
        **extracted.metadata,
        "page_count": len(extracted.pages),
        "pages": [
            {
                "page_number": page.page_number,
                "metadata": page.metadata,
            }
            for page in extracted.pages
        ],
    }

    return Document(
        document_id=str(uuid4()),
        source=DataSource.PDF,
        title=extracted.title,
        content=content,
        document_type=DocumentType.DOCUMENT,
        source_id=checksum,
        checksum=checksum,
        metadata=metadata,
    )