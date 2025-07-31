import cloudscraper
import json
from typing import Dict, List
import re

from ..base import BaseDriver

class JsonApiDriver(BaseDriver):
    chapter_base_url: str
    get_series_details_api: str
    get_chapter_details_api: str
    image_url: str

    current_chapter_id = 0

    def download_series_content(self, title_url: str) -> str:
        manga_id = title_url.rstrip("/").split("/")[-2]
        scraper = cloudscraper.create_scraper()
        resp = scraper.get(self.get_series_details_api.format(id=manga_id, offset=0))
        resp.raise_for_status()
        return resp.text

    def fetch_series_metadata(self, raw: str) -> Dict:
        chapters = []
        offset = 0
        json_resp = json.loads(raw)
        data = json_resp.get("data", [])
        series_title = None
        for item in data:
            attr = item["attributes"]
            if not series_title and attr.get("title"):
                series_title = attr.get("title")
            chapters.append({
                "url": self.chapter_base_url.format(id=item['id']),
                "volume": f"Volume {attr.get('volume') or 'N/A'}",
                "chapter": float(attr.get("chapter") or 0),
                "title": attr.get("title") or "",
                "language": attr.get("translatedLanguage"),
            })
        offset += len(data)
        return {"series_title": series_title, "chapters": chapters}

    def download_chapter_content(self, chapter_url: str) -> str:
        chapter_id = chapter_url.rstrip("/").split("/")[-1]
        self.current_chapter_id = chapter_id
        scraper = cloudscraper.create_scraper()
        resp = scraper.get(self.get_chapter_details_api.format(id=chapter_id, offset=0))
        resp.raise_for_status()
        return resp.text

    def fetch_chapter_metadata(self, raw: str) -> Dict:
        data = json.loads(raw).get("chapter", {})
        images = [self.image_url.format(hash=data['hash'], id=p) for p in data["data"]]
        return {
            "chapter_id": self.current_chapter_id,
            "pages": images,
        }
