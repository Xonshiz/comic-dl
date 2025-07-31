from typing import Dict
import re

from ..layouts.layout_html_generic import GenericHtmlDriver
from ..registry                     import register_driver

class BatoToDriver(GenericHtmlDriver):
    base_url            = "https://bato.to"
    series_url_pattern  = r"https?://(?:www\.)?bato\.to/series/\d+"

    series_selector     = "div.main div.item"
    link_selector       = "a.chapt"
    title_selector      = "a.chapt b"
    chapter_id_regex    = r"/chapter/(\d+)"
    img_array_regex     = r"const\s+imgHttps\s*=\s*(\[.*?\]);"
    series_title_regex = r'<a href="/series/\d+">(.*?)</a>'

    def get_chapter_title(self, metadata: Dict) -> str:
        return metadata["chapter_id"]

    def is_series_url(self, url: str) -> bool:
        return re.search(self.series_url_pattern, url) is not None

register_driver(
    BatoToDriver.series_url_pattern,
    BatoToDriver,
    layout_name="bato_html"
)
register_driver(
    r"https?://(?:www\.)?bato\.to/chapter/\d+",
    BatoToDriver,
    layout_name="bato_html"
)
