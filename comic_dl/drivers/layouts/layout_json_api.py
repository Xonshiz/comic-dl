"""
Layout strategy: JSON API (MangaDex.org).
"""

import cloudscraper
from typing     import Dict, List, Optional
from pathlib    import Path
from ..base     import BaseDriver

class JsonApiDriver(BaseDriver):
    API_AT_HOME   = "https://api.mangadex.org/at-home/server/{id}"
    API_AGGREGATE = (
        "https://api.mangadex.org/manga/{id}/feed"
        "?limit=100&offset={offset}"
        "&includes[]=scanlation_group&includes[]=user"
        "&order[volume]=asc&order[chapter]=asc"
        "&contentRating[]=safe&contentRating[]=suggestive"
        "&contentRating[]=erotica&contentRating[]=pornographic"
        "&includeFutureUpdates=0"
    )

    def fetch_metadata(self, url: str) -> Dict:
        chapter_id = url.rstrip("/").split("/")[-1]
        scraper    = cloudscraper.create_scraper()
        resp       = scraper.get(self.API_AT_HOME.format(id=chapter_id))
        resp.raise_for_status()
        data       = resp.json()
        return {
            "chapter_id": chapter_id,
            "comic_hash": data["chapter"]["hash"],
            "base_url":   data["baseUrl"].rstrip("/"),
            "pages":      data["chapter"]["data"],
        }

    def list_pages(self, metadata: Dict) -> List[str]:
        base = "https://uploads.mangadex.org"
        return [f"{base}/data/{metadata['comic_hash']}/{p}" for p in metadata["pages"]]

    def download_image(self, page_url: str, dest: Path,
                       proxy: Optional[str] = None) -> None:
        scraper = cloudscraper.create_scraper()
        if proxy:
            scraper.proxies = {"http": proxy, "https": proxy}
        resp = scraper.get(page_url, stream=True)
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)

    def list_chapters(self, title_url: str) -> List[Dict]:
        manga_id = title_url.rstrip("/").split("/")[-2]
        scraper  = cloudscraper.create_scraper()
        chapters = []
        offset   = 0

        while True:
            resp = scraper.get(self.API_AGGREGATE.format(id=manga_id, offset=offset))
            resp.raise_for_status()
            data = resp.json().get("data", [])
            if not data:
                break
            for item in data:
                attr = item["attributes"]
                chapters.append({
                    "url":      f"https://mangadex.org/chapter/{item['id']}",
                    "volume":   f"Volume {attr.get('volume') or 'N/A'}",
                    "chapter":  float(attr.get("chapter") or 0),
                    "title":    attr.get("title") or "",
                    "language": attr.get("translatedLanguage"),
                })
            offset += len(data)

        return chapters
