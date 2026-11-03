from app.ingestion.schemas import (
    DataSource,
    Document,
    DocumentType,
)


doc = Document(
    document_id="jira_PAY-1024",
    source=DataSource.JIRA,
    title="Payment Gateway Failure",
    content="Payment gateway returns 502 error.",
    document_type=DocumentType.TICKET,
    source_id="PAY-1024",
    metadata={
        "project": "Payment Infrastructure",
        "status": "Open",
    },
)

print(doc.model_dump_json(indent=2))