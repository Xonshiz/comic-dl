import re

from ..layouts.layout_json_api import JsonApiDriver
from ..registry                         import register_driver

class MangaDexDriver(JsonApiDriver):
    chapter_base_url = "https://mangadex.org/chapter/{id}"
    get_chapter_details_api = "https://api.mangadex.org/at-home/server/{id}"
    get_series_details_api = (
        "https://api.mangadex.org/manga/{id}/feed"
        "?limit=500&offset={offset}"
        "&includes[]=scanlation_group&includes[]=user"
        "&order[volume]=asc&order[chapter]=asc"
        "&contentRating[]=safe&contentRating[]=suggestive"
        "&contentRating[]=erotica&contentRating[]=pornographic"
        "&includeFutureUpdates=0"
    )
    image_url = "https://uploads.mangadex.org/data/{hash}/{id}"
    # "{self.image_base_url}/data/{data['hash']}/{p}"

    series_url_pattern = r"https?://(?:www\.)?mangadex\.org/title/[0-9a-f-]+"

    def is_series_url(self, url: str) -> bool:
        return re.search(self.series_url_pattern, url) is not None

register_driver(
    MangaDexDriver.series_url_pattern,
    MangaDexDriver,
    layout_name="mangadex_json"
)
register_driver(
    r"https?://(?:www\.)?mangadex\.org/chapter/[0-9a-f-]+",
    MangaDexDriver,
    layout_name="mangadex_json"
)