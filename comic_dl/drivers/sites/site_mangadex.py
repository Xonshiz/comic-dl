"""
Adapter for MangaDex using JsonApiDriver.
"""

from ..layouts.layout_json_api import JsonApiDriver
from ..registry                import register_driver

register_driver(
    r"https?://(?:www\.)?mangadex\.org/(?:chapter|title)/[0-9a-f-]+",
    JsonApiDriver,
    layout_name="json_api"
)
