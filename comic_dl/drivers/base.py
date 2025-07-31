import cloudscraper
from abc import ABC, abstractmethod
from pathlib import Path
from typing   import List, Dict, Optional

class BaseDriver(ABC):
    """
    Driver interface:
      - download_series_content(url) -> raw_data
      - fetch_series_metadata(raw_data) -> { series_title: str, chapters: List[ {url, chapter_id, chapter, language} ] }
      - download_chapter_content(url) -> raw_data
      - fetch_chapter_metadata(raw_data) -> { series_title, chapter_id, pages: List[str] }
      - list_pages(chapter_meta) -> List[str]
      - get_chapter_title(chapter_meta) -> str
    """

    @abstractmethod
    def is_series_url(self, url: str) -> bool:
        ...

    @abstractmethod
    def download_series_content(self, title_url: str) -> object:
        """Fetch and return the raw response for a series page."""
        ...

    @abstractmethod
    def fetch_series_metadata(self, raw: object) -> Dict:
        """Parse raw series content to metadata."""
        ...

    @abstractmethod
    def download_chapter_content(self, chapter_url: str) -> object:
        """Fetch and return raw response for a chapter."""
        ...

    @abstractmethod
    def fetch_chapter_metadata(self, raw: object) -> Dict:
        """Parse raw chapter content to metadata."""
        ...

    def list_pages(self, metadata: Dict) -> List[str]:
        """By default, pages are in metadata['pages']."""
        return metadata.get("pages", [])

    def get_chapter_title(self, metadata: Dict) -> str:
        return metadata.get("chapter_id", "")

    def download_image(self,
                       page_url: str,
                       dest: Path,
                       proxy: Optional[str] = None) -> None:
        """Stream a single image to disk."""
        scraper = cloudscraper.create_scraper()
        if proxy:
            scraper.proxies = {"http": proxy, "https": proxy}
        resp = scraper.get(page_url, stream=True)
        resp.raise_for_status()
        with open(dest, "wb") as fp:
            for chunk in resp.iter_content(1024):
                fp.write(chunk)
