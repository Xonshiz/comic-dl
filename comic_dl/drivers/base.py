"""
Abstract BaseDriver for site-specific implementations.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing   import List, Dict, Optional

class BaseDriver(ABC):

    @abstractmethod
    def fetch_metadata(self, url: str) -> Dict:
        """Single‑chapter metadata."""
        ...

    @abstractmethod
    def list_pages(self, metadata: Dict) -> List[str]:
        """List of image URLs for a single chapter."""
        ...

    @abstractmethod
    def download_image(self, page_url: str, dest: Path,
                       proxy: Optional[str] = None) -> None:
        """Download a single image to dest, optionally via proxy."""
        ...

    @abstractmethod
    def list_chapters(self, title_url: str) -> List[Dict]:
        """
        For a series URL, return:
        [ {'url': chapter_url,
           'volume': 'Volume X',
           'chapter': float,
           'title': str,
           'language': str}, ... ]
        """
        ...
