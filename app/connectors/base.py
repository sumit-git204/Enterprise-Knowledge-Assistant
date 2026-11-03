from abc import ABC, abstractmethod
from pathlib import Path

from app.ingestion.schemas import ExtractedDocument

class BaseConnector(ABC):
    @abstractmethod
    def extract(self, file_path: Path) -> ExtractedDocument:
        pass
