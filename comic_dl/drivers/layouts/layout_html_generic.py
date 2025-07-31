import re
from bs4 import BeautifulSoup
from typing import Dict, List

from ..base import BaseDriver

class GenericHtmlDriver(BaseDriver):
    base_url: str
    series_url_pattern: str
    series_selector: str
    link_selector: str
    title_selector: str
    chapter_id_regex: str
    img_array_regex: str
    series_title_regex: str

    def download_series_content(self, title_url: str) -> str:
        return __import__("cloudscraper").create_scraper().get(title_url).text

    def fetch_series_metadata(self, raw: str) -> Dict:
        soup = BeautifulSoup(raw, "html.parser")
        title_el = soup.select_one("title")
        series_title = title_el.get_text(strip=True)
        chapters = []
        for item in soup.select(self.series_selector):
            a = item.select_one(self.link_selector)
            href = a["href"]
            m    = re.search(self.chapter_id_regex, href)
            chap_id = m.group(1)
            chapters.append({
                "url":        self.base_url + href,
                "chapter_id": chap_id,
                "chapter":    chap_id,
                "language":   None
            })
        return {"series_title": series_title, "chapters": chapters}

    def download_chapter_content(self, chapter_url: str) -> str:
        return __import__("cloudscraper").create_scraper().get(chapter_url).text

    def fetch_chapter_metadata(self, raw: str) -> Dict:
        images = re.search(self.img_array_regex, raw, re.DOTALL)
        series_title = re.search(self.series_title_regex, raw, re.DOTALL).group(1)
        pages = __import__("json").loads(images.group(1))
        chap_id = re.search(self.chapter_id_regex, raw).group(1)
        return {"chapter_id": chap_id, "pages": pages, "series_title": series_title}
