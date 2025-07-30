"""
Abstract BaseDriver for site-specific implementations.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing   import List, Dict

class BaseDriver(ABC):

    @abstractmethod
    def fetch_metadata(self, url: str) -> Dict:
        """Single‑chapter metadata (e.g., chapter_id)."""
        ...

    @abstractmethod
    def list_pages(self, metadata: Dict) -> List[str]:
        """List of image URLs for a single chapter."""
        ...

    @abstractmethod
    def download_image(self, page_url: str, dest: Path) -> None:
        """Download one image page to dest path."""
        ...

    @abstractmethod
    def list_chapters(self, title_url: str) -> List[Dict]:
        """
        For a series/title URL, return:
        [ { 'url': chapter_url,
            'volume': 'Volume X',
            'chapter': float,
            'title': 'subtitle' },
          ... ]
        """
        ...
