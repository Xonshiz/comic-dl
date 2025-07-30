"""
Custom exceptions and error codes.
"""

from typing import List

class ComicDlError(Exception):
    """Base exception for comic_dl library."""
    error_code: int = 1

class UnsupportedSiteError(ComicDlError):
    """Raised when no driver matches a given URL."""
    error_code: int = 100

    def __init__(self, url: str, layouts: List[str]):
        msg = f"Unsupported site {url}. Available layouts: {', '.join(layouts)}"
        super().__init__(msg)
        self.url     = url
        self.layouts = layouts
