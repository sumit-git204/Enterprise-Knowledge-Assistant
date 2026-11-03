from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class DataSource(str, Enum):
    PDF = "pdf"
    JIRA = "jira"
    CONFLUENCE = "confluence"
    SHAREPOINT = "sharepoint"
    RALLY = "rally"
    SERVICENOW = "servicenow"
    SQL = "sql"


class DocumentType(str, Enum):
    DOCUMENT = "document"
    TICKET = "ticket"
    INCIDENT = "incident"
    KNOWLEDGE_ARTICLE = "knowledge_article"
    DATABASE_RECORD = "database_record"


class Document(BaseModel):
    document_id: str
    source: DataSource
    title: str
    content: str
    document_type: DocumentType = DocumentType.DOCUMENT

    source_url: HttpUrl | None = None
    source_id: str | None = None

    version: str | None = None
    checksum: str | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None
    ingested_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    metadata: dict[str, Any] = Field(default_factory=dict)


class ExtractedPage(BaseModel):
    page_number: int
    content: str

    metadata: dict[str, Any] = Field(default_factory=dict)


class ExtractedDocument(BaseModel):
    title: str
    pages: list[ExtractedPage]

    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str

    content: str
    chunk_index: int

    page_number: int | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)